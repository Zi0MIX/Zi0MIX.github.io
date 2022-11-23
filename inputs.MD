# Schematic for main() func argument input
```
arguments: {
    "rounds": int,
    "players": int,
    "map_code": str,
    "arguments": bool,
    "args": {
        "range": bool,
        "perfect_round": bool,
        "clear_output": bool,
        "break": bool,
        "detailed": bool,
        "nodecimal": bool,
        "speedrun_time": bool,
        "lower_time": bool,
        "all_results": bool,
        "teleport_time": bool
    },
    "mods": array
}
```
| Key | Type | Desc |
| --- | --- | --- |
| rounds | int | Mandatory input, number of rounds for the calculator |
| players | int | Mandatory input, number of players for the calculator |
| map_code | str | Mandatory with arg `perfect_round`, defines which map is used for perfect round prediction |
| arguments | bool | Should be true if any of the args is changed from default |
| args | dict | Contains calculator arguments `key`: `bool`, all arguments have to be passed, even if none are changed |
| mods | list | Contains mods for calculator, pass empty array if none mods are activated |

Refer to [this](https://github.com/Zi0MIX/ZM-RoundCalculator/blob/main/ARGUMENTS.MD) document for argument explanation.