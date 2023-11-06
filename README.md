# launchutil -  utility to create and run a simple launchd service

# Summary

**launchutil** is a command line utility to support creating and running a simple `launchd` service that is run daily. It is intended to make working with `launchd` more ergonomic by allowing a service to be specified by either its service name (aka label) or by its property list file (`<service name>.plist`). **launchutil** invokes `launchctl` commands to manage the service's lifecycle. 

# Install

Installation of **launchutil** is via the `Makefile` target `install`. It is invoked as shown below:

```
$ make install
```

The `install` target will install **launchutil** in `INSTALL_DIR`, which by default is set to `$(HOME)/bin`. If `INSTALL_DIR` does not exist, the `install` target will create it. `$(HOME)/bin` should also be in your `PATH` environment variable. 

If you wish `INSTALL_DIR` to be different, edit the `Makefile` to your preference before running `make install`.

# Example

Objective: Invoke the `say` command to say "hello there" at 14:00 (2pm) and 15:15 (3:15 pm) everyday. 

## Create the service plist

Invoke the following command to create the launchd service `com.yummymelon.sayhello` that is stored in the plist file named the same (`com.yummymelon.sayhello.plist`).

```Shell
$ launchutil create --program /usr/bin/say --program-arguments hello there --daily 14:00 15:15 --execute com.yummymelon.sayhello
```

Alternately, you can use short arguments to achieve the same result.

```Shell
$ launchutil create -p /usr/bin/say -a hello there -d 14:00 15:15 -x com.yummymelon.sayhello
```

Note that all commands that change state *must* have the `--execute` or `-x` argument provided. If not, then a message saying what the command would do is sent to `stderr`.

## Install the service plist
The following command installs the launchd service plist file into `~/Library/LaunchAgents`.

```
$ launchutil install com.yummymelon.sayhello.plist -x 
```

## Start (aka bootstrap, start) the service

```
$ launchutil bootstrap com.yummymelon.sayhello.plist -x 
```
Aliases for `bootstrap` are `s` and `start`.

##  Print (aka list, status) the service 

```
$ launchutil print com.yummymelon.sayhello.plist 
```
Aliases for `print` are `p`, `list`, and `status`.

## Modify service and reload 

It is a common desire to modify the service schedule and reload the service. 

To update the schedule to run at 15:00 (3pm) and 15:20 (3:20pm):

```
$ launchutil create -p /usr/bin/say -a hello there -d 15:00 15:20 -x com.yummymelon.sayhello.plist
```
Install the updated file `com.yummymelon.sayhello.plist` and reload the service:

```
$ launchutil reload --install --execute com.yummymelon.sayhello.plist
```

## Stop (aka bootout, stop) the service

```
$ launchutil bootout com.yummymelon.sayhello.plist -x 
```

Aliases for `bootout` are `t` and `stop`.

## Uninstall the service plist

```
$ launchutil uninstall com.yummymelon.sayhello.plist -x 
```

# Usage

## Top Level Commands

```
usage: launchutil [-h] [-v]
                  {create,c,install,i,uninstall,u,bootstrap,s,start,load,bootout,t,stop,unload,reload,r,restart,enable,e,disable,d,print,p,list,status,dir}
                  ...

Utility to create and run a simple launchd service.

positional arguments:
  {create,c,install,i,uninstall,u,bootstrap,s,start,load,bootout,t,stop,unload,reload,r,restart,enable,e,disable,d,print,p,list,status,dir}
    create (c)          create launchd service plist file
    install (i)         install launchd service file
    uninstall (u)       uninstall launchd service file
    bootstrap (s, start, load)
                        bootstrap the launchd service
    bootout (t, stop, unload)
                        bootout the launchd service
    reload (r, restart)
                        reload the launchd service
    enable (e)          enable the launchd service
    disable (d)         disable the launchd service
    print (p, list, status)
                        print the launchd service status
    dir                 list the service directory

options:
  -h, --help            show this help message and exit
  -v, --version         print version information and exit

launchutil is a helper utility to support creating and running a simple
launchd service that is run daily. It is intended to make working with launchd
more ergonomic by allowing specification of the service be either by its
service name (aka label) or by plist file name defining the service.
```

Note that command aliases are supported, for example, `s` and `start` are aliases for `bootstrap`.

## Create Command

```
usage: launchutil create [-h] [-o OUTPUT] [-x] -p PROGRAM
                         [-a PROGRAM_ARGUMENTS [PROGRAM_ARGUMENTS ...]]
                         [-d DAILY [DAILY ...]] [-w WORKING_DIRECTORY]
                         [-O STANDARD_OUT_PATH] [-E STANDARD_ERROR_PATH]
                         service

Create launchd service plist file to run a job on a daily basis. The file name
is the same as the `service` argument with a .plist extension.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
  -p PROGRAM, --program PROGRAM
                        full path to launchd job program
  -a PROGRAM_ARGUMENTS [PROGRAM_ARGUMENTS ...], --program-arguments PROGRAM_ARGUMENTS [PROGRAM_ARGUMENTS ...]
                        arguments to launchd job program; do not use this
                        argument before the `service` argument
  -d DAILY [DAILY ...], --daily DAILY [DAILY ...]
                        configure StartCalendarInterval for daily behavior
                        with a 24-hour time stamp (HH:MM); multiple times in a
                        day are space separated; do not use this argument
                        before the `service` argument
  -w WORKING_DIRECTORY, --working-directory WORKING_DIRECTORY
                        specify a directory to chdir to before running the
                        launchd job
  -O STANDARD_OUT_PATH, --standard-out-path STANDARD_OUT_PATH
                        file to write the launchd job stdout to
  -E STANDARD_ERROR_PATH, --standard-error-path STANDARD_ERROR_PATH
                        file to write the launchd job stderr to
```

## Install Command

```
usage: launchutil install [-h] [-o OUTPUT] [-x] [-p PATH] service

Install launchd service plist file in --path.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
  -p PATH, --path PATH  launchd script directory (default:
                        ~/Library/LaunchAgents)
```

## Bootstrap Command

```
usage: launchutil bootstrap [-h] [-o OUTPUT] [-x] [-p PATH] service

Bootstrap (aka load) launchd service.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
  -p PATH, --path PATH  launchd script directory (default:
                        ~/Library/LaunchAgents)
```

## Print Command

```
usage: launchutil print [-h] [-o OUTPUT] [-x] service

Print launchd service information/status.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
```

Note that because `print` is a read-only operation, the `--execute` argument is optional.

## Bootout Command

```
usage: launchutil bootout [-h] [-o OUTPUT] [-x] [-p PATH] service

Bootout (aka unload) launchd service.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
  -p PATH, --path PATH  launchd script directory (default:
                        ~/Library/LaunchAgents)
```

## Reload Command

```
usage: launchutil reload [-h] [-o OUTPUT] [-x] [-p PATH] [-i] service

Reload (aka restart) launchd service. Optionally install launchd service plist
file in current directory before reloading.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
  -p PATH, --path PATH  launchd script directory (default:
                        ~/Library/LaunchAgents)
  -i, --install         install service plist to --path
```

## Enable Command

```
usage: launchutil enable [-h] [-o OUTPUT] [-x] service

Enable launchd service.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
```

## Disable Command

```
usage: launchutil disable [-h] [-o OUTPUT] [-x] service

Disable launchd service.

positional arguments:
  service               service name or its plist file (typically in form of
                        com.domain.servicename)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (- for stdout)
  -x, --execute         execute command
```

# Environment 

- Tested on macOS Ventura 13.4. 
- Python 3.9+

# License

Copyright © Charles Y. Choi

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


<!--  LocalWords:  launchutil launchd
 -->
