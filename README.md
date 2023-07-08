# iniparser

[**iniparser**](https://github.com/HugeBrain16/iniparser) is a minimalist (?) and simple ini parser. this is the first iniparser version before [**iniparser2**](https://github.com/HugeBrain16/iniparser2).  
this project was deleted for some reason, and I decided to restore the project and improve some stuff.

## Features

| Name            | Support |
| :-------------- | :-----: |
| Read            |   ✅    |
| Write           |   ✅    |
| Comments        |   ✅    |
| Inline Comments |   ✅    |
| Sections        |   ✅    |
| Multi-Line      |   ✅    |

## Examples

basic example

```py
import iniparser

text = """
[player]
x = 10
y = 5
health = 100.0
"""

data = iniparser.read(text)

print("[Player]")
print(f"<X: {data['player']['x']}, Y: {data['player']['y']}>")
print("Health: " + data["player"]["health"])
```
