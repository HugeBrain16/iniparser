# iniparser

[**iniparser**](https://github.com/HugeBrain16/iniparser) is a minimalist (?) and simple ini parser. this is the first iniparser version before [**iniparser2**](https://github.com/HugeBrain16/iniparser2).  
this project was deleted for some reason, and I decided to restore the project and improve some stuff.  

## Features
|Name|Support|
|:---|:-----:|
|Read|✅|
|Write|✅|
|Comments|✅|
|Sections|❌|
|Multi-Line|❌|

## Examples

basic example
```py
import iniparser

text = """
name = chad broski
age = 55
"""

# get values as string
name = iniparser.get(text, "name")
age = iniparser.get(text, "age")

print("name: " + name)
print("age: " + age)
```
  
read and convert value with specific types
```py
import iniparser

text = """
rat = 3
size = 8.0
cockroach = false
"""

rat = iniparser.getint(text, "rat")
size = iniparser.getfloat(text, "size")
cockroach = iniparser.getbool(text, "cockroach")
```

get all options
```py
import iniparser

text = """
joe = amogus
who = joe
amogus = sus
no_more = amogus
"""

data = iniparser.getall(text)
```