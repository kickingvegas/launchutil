# launchutil Example

This directory contains an example of using **launchutil** to create a `launchd` service that announces the time at the top of the hour from 9am to 5pm daily.

Various **launchutil** targets are captured in the `Makefile`. Before running any targets, make sure **launchutil** is installed.

To create, install, and start the example `launchd` service:

```
$ make install_and_load_saytime
```

To stop and uninstall the example `launchd` service:

```
$ make uninstall_saytime 
```



