# Schematic for main() func argument output
```
arguments: {
    "type": str,
    "arguments": list,
    "round": int,
    "players": int,
    "zombies": int,
    "raw_time": float,
    "time_output": str,
    "spawnrate": float,
    "raw_spawnrate": float,
    "network_frame": float,
    "map_name": str,
    "class_content": dict,
}
```
| Key | Type | Data range | Desc |
| --- | --- | --- | --- |
| type | str | `round_time`, `perfect_times`, `mod`, `error` | Which calculation mode is used. |
| message | str | any | Used only if error is raised, passes error message. |
| arguments | list | available mods | Which mods are used (to know what to output). |
| round | int | 1-255 | Round number. |
| players | int | 1-4 | Player number. |
| zombies | int | 0+ | Zombies number. |
| raw_time | float | any | Raw time value. |
| time_output | str | any | Time value to be print out. |
| spawnrate | float | any | Spawnrate in seconds. |
| raw_spawnrate | float | any | Raw spawnrate in seconds. |
| network_frame | float | `0.05` / `0.10` | Network frame value. |
| map_name | str | func `map_translator()` | Returns name of the map. |
| class_content | dict | all class vars | Dump of all values in the class (debugger). |

Refer to [this](https://github.com/Zi0MIX/ZM-RoundCalculator/blob/main/ARGUMENTS.MD) document for argument explanation.

## Output variants:
- Round time
| Arguments | Structure |
| --- | --- |
| - | Round <round> will spawn in <time_output> and has <zombies> zombies. Spawnrate: <spawnrate> Network frame: <network_frame>. |
| `-c` | <time_output> |

- Perfect times
| Arguments | Structure |
| --- | --- |
| - | Perfect time to round <round> is <time_output> on <map_name>. |
| `-c` | <time_output> |

- Mods
| Arguments | Structure |
| --- | --- |
| `-rs` | <raw_spawnrate> |
| `-ps` | <spawnrate> |
| `-zc` | <zombies> |
| `-db` | <class_content> |
| `-ddb` | <class_content> |