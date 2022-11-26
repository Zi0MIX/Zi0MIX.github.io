from dataclasses import dataclass

DEC = 3

# Time from "initial_blackscreen_passed" to "start_of_round" triggers
RND_WAIT_INITIAL = 8.25
# Time from "end_of_round" to "start_of_round"
RND_WAIT_END = 12.50
# Time from "end_of_round" to "between_round_over"
RND_WAIT_BETWEEN = RND_WAIT_END - 2.5
# Time difference between "start_of_round" trigger and new round number appearing
RND_BETWEEN_NUMBER_FLAG = 4.0

ZOMBIE_MAX_AI = 24
ZOMBIE_AI_PER_PLAYER = 6

# Perfect dog rounds, r5 then all 4 rounders
DOGS_PERFECT = [int(x) for x in range(256) if x % 4 == 1 and x > 4]
DOGS_WAIT_START = 7.05      # 0.05 from ingame timing, code says 7 dot
DOGS_WAIT_END = 8
# Time between dog spawning to dog appearing on the map
DOGS_WAIT_TELEPORT = 1.5

MAP_LIST = ("zm_prototype", "zm_asylum", "zm_sumpf", "zm_factory", "zm_theater", "zm_pentagon", "zm_cosmodrome", "zm_coast", "zm_temple", "zm_moon", "zm_transit", "zm_nuked", "zm_highrise", "zm_prison", "zm_buried", "zm_tomb")


@dataclass
class ZombieRound:
    number: int
    players: int


    def __post_init__(self):
        self.get_network_frame()
        self.get_zombies()
        self.get_spawn_delay()
        self.get_round_time()


    def get_network_frame(self):
        self.network_frame = 0.05
        if self.players == 1:
            self.network_frame = 0.10

        return


    def get_round_spawn_delay(self, raw_delay: float) -> float:
        self.raw_spawn_delay = raw_delay

        if raw_delay < 0.01:
            raw_delay = 0.01

        inside = str(raw_delay).split(".")

        if not len(inside[1]):
            real_decimals = ["0", "0"]
        elif len(inside[1]) == 1:
            real_decimals = [inside[1], "0"]
        else:
            real_decimals = [str(x) for x in inside[1]][:2]

            if len(inside[1]) > 2:
                # Round decimals outside of the scope in a normal way
                dec = reversed([int(x) for x in inside[1]][2:])
                # decimals = []
                remember = 0

                for x in dec:
                    x += remember
                    remember = 0

                    if x >= 5:
                        # decimals.append("0")
                        remember = 1
                    # else:
                    #     decimals.append("0")

                if remember:
                    real_decimals[1] = str(int(real_decimals[1]) + 1)
                    if real_decimals[1] == "10":
                        real_decimals[0] = str(int(real_decimals[0]) + 1)
                        real_decimals[1] = "0"

        # Round decimals in the scope to 0.05 following GSC way
        if real_decimals[1] in ("0", "1", "2"):
            real_decimals[1] = "0"
        elif real_decimals[1] in ("3", "4", "5", "6", "7"):
            real_decimals[1] = "5"
        else:
            real_decimals[1] = "0"
            real_decimals[0] = str(int(real_decimals[0]) + 1)

            if real_decimals[0] == "10":
                real_decimals[0] = "0"
                inside[0] = str(int(inside[0]) + 1)

        inside[1] = "".join(real_decimals)
        # print(f"{inside} / original: {str(self.raw_spawn_delay).split('.')}")

        return float(".".join(inside))


    def get_spawn_delay(self):
        self.zombie_spawn_delay = 2.0
        self.raw_spawn_delay = 2.0

        if self.number > 1:
            for _ in range(1, self.number):
                self.zombie_spawn_delay *= 0.95

            self.zombie_spawn_delay = self.get_round_spawn_delay(self.zombie_spawn_delay)

            if self.zombie_spawn_delay < 0.1:
                self.zombie_spawn_delay = 0.1

        self.zombie_spawn_delay = round(self.zombie_spawn_delay, 2)

        return


    def get_zombies(self):
        multiplier = self.number / 5
        if multiplier < 1:
            multiplier = 1.0
        elif self.number >= 10:
            multiplier *= (self.number * 0.15)

        if self.players == 1:
            temp = int(ZOMBIE_MAX_AI + (0.5 * ZOMBIE_AI_PER_PLAYER * multiplier))
        else:
            temp = int(ZOMBIE_MAX_AI + ((self.players - 1) * ZOMBIE_AI_PER_PLAYER * multiplier))

        self.zombies = temp
        if self.number < 2:
            self.zombies = int(temp * 0.25)
        elif self.number < 3:
            self.zombies = int(temp * 0.3)
        elif self.number < 4:
            self.zombies = int(temp * 0.5)
        elif self.number < 5:
            self.zombies = int(temp * 0.7)
        elif self.number < 6:
            self.zombies = int(temp * 0.9)

        return


    def extract_decimals(self):
        dec = "0"
        # '> 0' could result in 00000001 triggering the expression
        if int(str(self.raw_time).split(".")[1]) >= 1:
            dec = str(self.raw_time).split(".")[1][:3]

        while len(dec) < DEC:
            dec += "0"
        self.decimals = dec

        return


    def get_round_time(self):
        delay = self.zombie_spawn_delay + self.network_frame
        self.raw_time = (self.zombies * delay) - delay
        self.round_time = round(self.raw_time, 2)

        # self.extract_decimals()

        return


@dataclass
class DogRound(ZombieRound):
    special_rounds: int


    def __post_init__(self):
        self.get_network_frame()
        self.get_dogs()
        self.get_teleport_time()
        self.get_dog_spawn_delay()
        self.get_total_delay()
        self.round_up()


    def get_dogs(self):
        self.dogs = self.players * 8

        if self.special_rounds < 3:
            self.dogs = self.players * 6

        return


    def get_teleport_time(self):
        # Seems to be the best indication of representing spawncap accurately, at least in case of solo when comparing to actual gameplay
        self.teleport_time = DOGS_WAIT_TELEPORT * (self.dogs / (2 * self.players))
        return


    def get_dog_spawn_delay(self):
        self.dog_spawn_delay = 1.50

        if self.special_rounds == 1:
            self.dog_spawn_delay = 3.00
        elif self.special_rounds == 2:
            self.dog_spawn_delay = 2.50
        elif self.special_rounds == 3:
            self.dog_spawn_delay = 2.00

        return


    def get_total_delay(self):
        self.raw_time = 0
        self.delays = []
        for i in range(1, self.dogs):
            delay = self.get_round_spawn_delay(self.dog_spawn_delay - (i / self.dogs))

            self.raw_time += delay
            self.delays.append(delay)

        self.raw_time = round(self.raw_time, 2)


    def add_teleport_time(self):
        # Call if dog teleport time should be added for each dog on class level
        self.raw_time += self.teleport_time
        return


    def round_up(self):
        # round_wait() function clocks every .5 seconds
        time_in_ms = round(self.raw_time * 1000)
        if not time_in_ms % 500:
            self.round_time = self.raw_time
            return

        self.round_time = ((time_in_ms - (time_in_ms % 500)) + 500) / 1000
        return


def get_answer_blueprint() -> dict:
    """Check outputs.MD for reference"""
    return {
        "type": "mod",
        "arguments": [],
        "round": 0,
        "players": 0,
        "zombies": 0,
        "time": "00:00",
        "spawnrate": 0.0,
        "raw_spawnrate": 0.0,
        "network_frame": 0.0,
        "class_content": {},
    }


def get_arguments() -> dict:
    return {
        "all_results": {
            "use_in_web": False,
            "readable_name": "All results",
            "shortcode": "-a",
            "default_state": False,
            "exp": "Display all numeric results leading to the output. Debug argument."
        },
        "break": {
            "use_in_web": True,
            "readable_name": "Break",
            "shortcode": "-b",
            "default_state": True,
            "exp": "Display an empty line between results."
        },
        "clear": {
            "use_in_web": True,
            "readable_name": "Clear output",
            "shortcode": "-c",
            "default_state": False,
            "exp": "Show only numeric output as oppose to complete sentences. Use for datasets."
        },
        "detailed": {
            "use_in_web": True,
            "readable_name": "Detailed",
            "shortcode": "-d",
            "default_state": False,
            "exp": "Show time in miliseconds instead of formatted string."
        },
        "lower_time": {
            "use_in_web": True,
            "readable_name": "Lower Time",
            "shortcode": "-l",
            "default_state": False,
            "exp": "Change seconds rounding to go down instead of up."
        },
        "nodecimal": {
            "use_in_web": True,
            "readable_name": "Nodecimal",
            "shortcode": "-n",
            "default_state": True,
            "exp": "Show time without decimals."
        },
        "perfect_times": {
            "use_in_web": True,
            "readable_name": "Perfect times",
            "shortcode": "-p",
            "default_state": False,
            "exp": "Instead of perfect round times, display perfect split times for choosen map."
        },
        "range": {
            "use_in_web": True,
            "readable_name": "Range",
            "shortcode": "-r",
            "default_state": False,
            "exp": "Show results for all rounds leading to selected number."
        },
        "speedrun_time": {
            "use_in_web": True,
            "readable_name": "Speedrun time",
            "shortcode": "-s",
            "default_state": False,
            "exp": "Show times accordingly to speedrun rules, round end is on number transition instead of when zombies start spawning."
        },
        "teleport_time": {
            "use_in_web": True,
            "readable_name": "Teleport time",
            "shortcode": "-t",
            "default_state": True,
            "exp": "Adds dog appearance time to perfect dog rounds accordingly to the pattern: 't * dogs / (2 * players))'"
        },
    }


def map_translator(map_code: str) -> str:
    if map_code == "zm_prototype":
        return "Nacht Der Untoten"
    if map_code == "zm_asylum":
        return "Verruckt"
    if map_code == "zm_sumpf":
        return "Shi No Numa"
    if map_code == "zm_factory":
        return "Der Riese"
    if map_code == "zm_theater":
        return "Kino Der Toten"
    if map_code == "zm_pentagon":
        return "FIVE"
    if map_code == "zm_cosmodrome":
        return "Ascension"
    if map_code == "zm_coast":
        return "Call of the Dead"
    if map_code == "zm_temple":
        return "Shangri-La"
    if map_code == "zm_moon":
        return "Moon"
    if map_code == "zm_transit":
        return "Tranzit"
    if map_code == "zm_nuked":
        return "Nuketown"
    if map_code == "zm_highrise":
        return "Die Rise"
    if map_code == "zm_prison":
        return "Mob of the Dead"
    if map_code == "zm_buried":
        return "Buried"
    if map_code == "zm_tomb":
        return "Origins"

    return map_code


def get_readable_time(round_time: float) -> str:
    h, m, s, ms = 0, 0, 0, int(round_time * 1000)

    while ms > 999:
        s += 1
        ms -= 1000
    while s > 59:
        m += 1
        s -= 60
    while m > 59:
        h += 1
        m -= 60

    dec = f".{str(ms).zfill(3)}"
    if args["nodecimal"] and not args["lower_time"]:
        dec = ""
        s += 1
        if s > 59:
            m += 1
            s -= 60
            if m > 59:
                h += 1
                m -= 60
    elif args["nodecimal"]:
        dec = ""

    if not h and not m:
        new_time = f"{s}{dec} seconds"
    elif not h:
        new_time = f"{str(m).zfill(2)}:{str(s).zfill(2)}{dec}"
    else:
        new_time = f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}{dec}"

    return new_time


def get_perfect_times(time_total: float, rnd: int, map_code: str) -> dict:

    a = get_answer_blueprint()
    a["type"] = "perfect_time"
    a["round"] = rnd
    a["raw_time"] = time_total
    a["map_name"] = map_translator(map_code)

    split_adj = 0.0
    if args["speedrun_time"]:
        split_adj = RND_BETWEEN_NUMBER_FLAG

    if args["detailed"]:
        a["readable_time"] = str(time_total * 1000)
    else:
        a["readable_time"] = get_readable_time(time_total - split_adj)

    return a


def get_round_times(rnd: ZombieRound) -> dict:

    a = get_answer_blueprint()
    a["type"] = "round_time"
    a["round"] = rnd.number
    a["players"] = rnd.players
    a["zombies"] = rnd.zombies
    a["raw_time"] = rnd.raw_time
    a["spawnrate"] = rnd.zombie_spawn_delay
    a["raw_spawnrate"] = rnd.raw_spawn_delay
    a["network_frame"] = rnd.network_frame
    a["class_content"] = vars(rnd)

    split_adj = 0
    if args["speedrun_time"]:
        split_adj = RND_BETWEEN_NUMBER_FLAG

    if args["detailed"]:
        a["time_output"] = str(rnd.round_time * 1000)
    else:
        a["time_output"] = get_readable_time(rnd.round_time - split_adj)

    return a


def calculator_custom(rnd: int, players: int, mods: list) -> list[dict]:
    answer = []

    for r in range(1, rnd + 1):
        a = get_answer_blueprint()

        zomb = ZombieRound(r, players)
        dog = DogRound(r, players, r)

        a["type"] = "mod"
        a["round"] = r
        a["players"] = players

        if "-rs" in mods:
            a["arguments"].append("-rs")
            a["raw_spawnrate"] = zomb.raw_spawn_delay
        elif "-ps" in mods:
            a["arguments"].append("-ps")
            a["spawnrate"] = zomb.zombie_spawn_delay
        elif "-zc" in mods:
            a["arguments"].append("-zc")
            a["zombies"] = zomb.zombies
        elif "-db" in mods:
            a["arguments"].append("-db")
            a["class_content"] = vars(zomb)
        elif "-ddb" in mods:
            a["arguments"].append("-ddb")
            a["class_content"] = vars(dog)

        answer.append(a)

    return answer


def calculator_handler(inputs: dict) -> list[str]:
    rnd, players, map_code, args_used = int(inputs["rounds"]), int(inputs["players"]), str(inputs["map_code"]), bool(inputs["arguments"])

    global args
    args = inputs["args"]
    mods = inputs["mods"]
    all_results = []

    if len(mods):
        return calculator_custom(rnd, players, mods)

    result = ZombieRound(rnd, players)

    if not args_used:
        return [get_round_times(result)]

    if args["perfect_round"]:
        time_total = RND_WAIT_INITIAL

        match map_code:
            case "zm_prototype" | "zm_asylum" | "zm_coast" | "zm_temple" | "zm_transit" | "zm_nuked" | "zm_prison" | "zm_buried" | "zm_tomb":

                for r in range(1, rnd):
                    result = ZombieRound(r, players)
                    round_duration = result.round_time + RND_WAIT_END
                    time_total += round_duration

                    if args["range"]:
                        res = get_perfect_times(time_total, result.number + 1, map_code)
                        res["class_content"] = vars(result)
                        all_results.append(res)

                if not args["range"]:
                    res = get_perfect_times(time_total, result.number, map_code)
                    res["class_content"] = vars(result)
                    all_results.append(res)


            case "zm_sumpf" | "zm_factory" | "zm_theater":
                dog_rounds = 0
                for r in range(1, rnd):

                    if r in DOGS_PERFECT:
                        result = DogRound(r, players, dog_rounds)
                        if args["teleport_time"]:
                            result.add_teleport_time()
                        dog_rounds += 1
                        round_duration = DOGS_WAIT_START + DOGS_WAIT_TELEPORT + result.round_time + DOGS_WAIT_END + RND_WAIT_END
                        time_total += round_duration
                    else:
                        result = ZombieRound(r, players)
                        round_duration = result.round_time + RND_WAIT_END
                        time_total += round_duration


                    if args["range"]:
                        res = get_perfect_times(time_total, result.number + 1, map_code)
                        res["class_content"] = vars(result)
                        all_results.append(res)

                if not args["range"]:
                    res = get_perfect_times(time_total, result.number, map_code)
                    res["class_content"] = vars(result)
                    all_results.append(res)


            case _:
                return [{"type": "error", "message": f"'{map_code}' not supported."}]

        return all_results

    if args["range"]:
        return [get_round_times(ZombieRound(r, players)) for r in range (1, rnd)]

    return [get_round_times(ZombieRound(rnd, players))]


def process_arguments(args: dict) -> dict:
    if args["detailed"] and args["nodecimal"]:
        args["detailed"] = False

    return args


def main(arguments: dict) -> list[str]:
    try:
        arguments["args"] = process_arguments(arguments["args"])
        return calculator_handler(arguments)
    except Exception as err:
        return [{"type": "error", "message": str(err)}]
