# batd.py
A simple minimalistic battery daemon, which observes the battery,
and collects interesting data about it.

it is just one python script and one class for the daemon functionality,
all written in python, the code base is easy to get, for further questions
look into the code.

# configuration
batd generates an ini-file where you can set a few configurations.
```
[batd]
scan_rate = [int] 
;in sec; how often the daemon fetches battery info
notify_factor = [int] 
;facotor of scan_rate; determines how often notifications get send  
log_file = [path] 
;the file where the daemon should log the information
battery_warn_trashhold = 
;trashhold for warning notifications
battery_critical_trashhold = 
;trashhold for critical notifications(in red)
```

# dependencies
due to various system calls this daemon is not cross-platform yet, it just works on unix systems

Dependency on nlsg-programs:
so far the "query" option is dependent on the bat c-program, this is going to be fixed soon.
The notification system is dependent on the "nls_util.py" library

# installation
no installation is required, but a python3.x.x interpreter

# usage
after the battery daemon is in the path,
type batd.py help, to get all available argument

# todo
 - adding expire time setting
 - extend pandas capability
