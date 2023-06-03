# launchutil -  utility to create and run a simple launchd service

**NOTE: THIS IS WIP**

# Summary

**launchutil** is a helper utility to support creating and running a simple `launchd` service that is run daily. It is intended to make working with `launchd` more ergonomic by allowing a service to be specified by either its service name (aka label) or by its property list file name which is typically the same with a `.plist` extension. **launchutil** invokes `launchctl` commands to manage the service lifecycle. 

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

```Shell
$ launchutil install com.yummymelon.sayhello.plist -x 
```

## Start (aka bootstrap, start) the service

```Shell
$ launchutil bootstrap com.yummymelon.sayhello.plist -x 
```
Aliases for `bootstrap` are `s` and `start`.

##  Print (aka list, status) the service 

```Shell
$ launchutil print com.yummymelon.sayhello.plist 
```
Aliases for `print` are `p`, `list`, and `status`.

## Modify service and reload 

It is a common desire to modify the service schedule and reload the service. 

To update the schedule to run at 15:00 (3pm) and 15:20 (3:20pm):

```Shell
$ launchutil create -p /usr/bin/say -a hello there -d 15:00 15:20 -x com.yummymelon.sayhello.plist
```

Install the updated file `com.yummymelon.sayhello.plist` and reload the service:

```Shell
$ launchutil reload --install --execute com.yummymelon.sayhello.plist
```

## Stop (aka bootout, stop) the service

```Shell
$ launchutil bootout com.yummymelon.sayhello.plist -x 
```

Aliases for `bootout` are `t` and `stop`.

## Uninstall the service plist

```Shell
$ launchutil uninstall com.yummymelon.sayhello.plist -x 
```

# Usage

```Shell
usage: launchutil [-h] [-v]
                  {create,c,install,i,uninstall,u,bootstrap,s,start,bootout,t,stop,reload,r,restart,enable,e,disable,d,print,p,list,status}
                  ...

Utility to create and run a simple launchd service.

positional arguments:
  {create,c,install,i,uninstall,u,bootstrap,s,start,bootout,t,stop,reload,r,restart,enable,e,disable,d,print,p,list,status}
    create (c)          create launchd service plist file
    install (i)         install launchd service file
    uninstall (u)       uninstall launchd service file
    bootstrap (s, start)
                        bootstrap the launchd service
    bootout (t, stop)   bootout the launchd service
    reload (r, restart)
                        reload the launchd service
    enable (e)          enable the launchd service
    disable (d)         disable the launchd service
    print (p, list, status)
                        print the launchd service status

options:
  -h, --help            show this help message and exit
  -v, --version         print version information and exit

launchutil is a helper utility to support creating and running a simple
launchd service that is run daily. It is intended to make working with launchd
more ergonomic by allowing specification of the service be either by its
service name (aka label) or by plist file name defining the service.
```

# Install

Installation of `launchutil` is via a `Makefile` target `install`. It is invoked as shown below.

```Shell
$ make install
```

In the `Makefile` the `INSTALL_DIR` is set to `$(HOME)/bin` which will be created if it does not already exist. `$(HOME)/bin` should also be in your `PATH` environment variable. If you wish `INSTALL_DIR` to be different, the `INSTALL_DIR` in the `Makefile` to your preference before running `make install`.

# Running `launchutil`

TBD

```Shell
$ launchutil
```


# License

Copyright © Charles Y. Choi

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


<!--  LocalWords:  launchutil launchd
 -->
