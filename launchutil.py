#!/usr/bin/env python3
# 
# Copyright 2023 Charles Y. Choi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
import argparse
import subprocess
import json
import plistlib
import shutil
import re

VERSION = "0.2.0"

def create_hook(args):
    LaunchdCreate(args).run()

def install_hook(args):
    LaunchdInstall(args).run()

def uninstall_hook(args):
    LaunchdUninstall(args).run()

def bootstrap_hook(args):
    LaunchdBootstrap(args).run()

def bootout_hook(args):
    LaunchdBootout(args).run()

def reload_hook(args):
    LaunchdReload(args).run()

def enable_hook(args):
    LaunchdEnable(args).run()

def disable_hook(args):
    LaunchdDisable(args).run()

def print_hook(args):
    LaunchdPrint(args).run()

def dir_hook(args):
    LaunchdDir(args).run()

def base_hook(args):
    print('wat')

class CommandLineParser:
    def __init__(self,
                 prog="<program name>",
                 description="<description>",
                 epilog="<epilog>",
                 version=VERSION):
        self.parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            epilog=epilog
        )

        self.parser.add_argument('-v', '--version',
                                 action='version',
                                 version=version,
                                 help='print version information and exit')
        
        tempList = []

        # TODO: add epilog

        tempList.append({
            'prog': 'create',
            'description': """Create launchd service plist file to run a job
            on a daily basis. The file name is the same as the `service` argument
            with a .plist extension.
            """,
            'help': 'create launchd service plist file',
            'hook': create_hook,
            'aliases': ['c']
        })
        
        tempList.append({
            'prog': 'install',
            'description': """Install launchd service plist file in
            ~/Library/LaunchAgents. 
            """,
            'help': 'install launchd service file',
            'hook': install_hook,
            'aliases': ['i']            
        })


        tempList.append({
            'prog': 'uninstall',
            'description': """Uninstall launchd service plist file in
            ~/Library/LaunchAgents.""",
            'help': 'uninstall launchd service file',
            'hook': uninstall_hook,
            'aliases': ['u']
        })

        tempList.append({
            'prog': 'bootstrap',
            'description': """Bootstrap (aka load) launchd service.""",
            'help': 'bootstrap the launchd service',
            'hook': bootstrap_hook,
            'aliases': ['s', 'start', 'load'] 
        })

        tempList.append({
            'prog': 'bootout',
            'description': """Bootout (aka unload) launchd service.""",
            'help': 'bootout the launchd service',
            'hook': bootout_hook,
            'aliases': ['t', 'stop', 'unload']
        })

        tempList.append({
            'prog': 'reload',
            'description': """Reload (aka restart) launchd service. Optionally
            install launchd service plist file in current directory before
            reloading.""",
            'help': 'reload the launchd service',
            'hook': reload_hook,
            'aliases': ['r', 'restart']
        })
        
        tempList.append({
            'prog': 'enable',
            'description': 'Enable launchd service.',
            'help': 'enable the launchd service',
            'hook': enable_hook,
            'aliases': ['e']            
        })
        
        tempList.append({
            'prog': 'disable',
            'description': 'Disable launchd service.',
            'help': 'disable the launchd service',
            'hook': disable_hook,
            'aliases': ['d']
        })

        tempList.append({
            'prog': 'print',
            'description': 'Print launchd service information/status.',
            'help': 'print the launchd service status',
            'hook': print_hook,
            'aliases': ['p', 'list', 'status']
        })

        tempList.append({
            'prog': 'dir',
            'description': 'List service directory.',
            'help': 'print the launchd service status',
            'hook': dir_hook,
            'aliases': []
        })
        
        subparsers = self.parser.add_subparsers()

        subparserDB = {}
        
        for cmdDict in tempList:
            subparserDB[cmdDict['prog']] = self.configureSubcommand(subparsers, cmdDict)

        self.addCreateArgs(subparserDB['create'])
        self.addReloadArgs(subparserDB['reload'])
        
        
        self.parser.set_defaults(func=base_hook)

    def configureSubcommand(self, subparsers, cmdDict):
        # TODO: add epilog
        subparser = subparsers.add_parser(
            cmdDict['prog'],
            description=cmdDict['description'],
            help=cmdDict['help'],
            aliases=cmdDict['aliases']
        )

        add_argument = subparser.add_argument
        
        add_argument('-o', '--output',
                     action='store',
                     default='-',
                     help='output file (- for stdout)')
        
        add_argument('-x', '--execute',
                     action='store_true',
                     help='execute command')

        if cmdDict['prog'] != 'dir':
            add_argument('service',
                         action='store',
                         help='service name or its plist file (typically in form of com.domain.servicename)')
        
        subparser.set_defaults(func=cmdDict['hook'])
        return subparser
        
    def addReloadArgs(self, subparser):
        add_argument = subparser.add_argument
        installPath = '~/Library/LaunchAgents'
        
        add_argument('-i', '--install',
                     action='store_true',
                     help='install service plist to {0}'.format(installPath))

    def addCreateArgs(self, subparser):
        add_argument = subparser.add_argument

        add_argument('-p', '--program',
                     action='store',
                     required=True,
                     help='full path to launchd job program')

        add_argument('-a', '--program-arguments',
                     action='store',
                     nargs='+',
                     help="""arguments to launchd job program;
                     do not use this argument before the `service` argument""")

        add_argument('-d', '--daily',
                     nargs='+',
                     action='store',
                     help="""configure StartCalendarInterval for daily behavior with a 
                     24-hour time stamp (HH:MM);
                     multiple times in a day are space separated; do not use this
                     argument before the `service` argument
                     """)
        
        add_argument('-w','--working-directory',
                     action='store',
                     help='specify a directory to chdir to before running the launchd job')

        add_argument('-O', '--standard-out-path',
                     action='store',
                     help='file to write the launchd job stdout to')

        add_argument('-E', '--standard-error-path',
                     action='store',
                     help='file to write the launchd job stderr to')
        
    def run(self):
        return self.parser.parse_args()


class LaunchdBase:
    def __init__(self, args):
        self.stdout = sys.stdout
        self.stdin = sys.stdin
        self.stderr = sys.stderr
        self.args = args

        hasService = 'service' in args

        if args.output != '-':
            outfile = open('{0}'.format(args.output), 'w')
            self.stdout = outfile

        if hasService:
            # Coerce service if it ends in ".plist"
            pat = re.compile(r'([\w\.]*).plist$')
            matchObj = pat.match(self.args.service)
            if matchObj:
                # print(matchObj.group(1))
                self.args.service = matchObj.group(1)

    def run(self):
        if 'service' in self.args:
            print(self.args.service)
            

class LaunchdInstall(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service

        source = '{0}.plist'.format(service)
        target = '{0}/Library/LaunchAgents/{1}.plist'.format(os.environ['HOME'],
                                                             service)
        if not os.path.exists(source):
            self.stderr.write('ERROR: "{0}" does not exist.\n'.format(source))
            sys.exit(os.EX_NOINPUT)

        if os.path.exists(target):
            self.stderr.write('WARNING: overwriting "{0}".\n'.format(target))

        if self.args.execute:
            shutil.copyfile(source, target)
        else:
            self.stderr.write('command: cp {0} {1}\n'.format(source, target))
            self.stderr.write('add -x or --execute flag to execute command.\n')


class LaunchdUninstall(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service

        target = '{0}/Library/LaunchAgents/{1}.plist'.format(os.environ['HOME'],
                                                             service)

        if not os.path.exists(target):
            self.stderr.write('ERROR: "{0}" does not exist.\n'.format(target))

        if self.args.execute:
            if os.path.exists(target):
                os.unlink(target)
        else:
            self.stderr.write('command: rm {0}\n'.format(target))
            self.stderr.write('add -x or --execute flag to execute command.\n')           


class LaunchdBootstrap(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service
        uid = os.getuid()

        target = '{0}/Library/LaunchAgents/{1}.plist'.format(os.environ['HOME'],
                                                             service)
        
        cmdList = ['launchctl',
                   'bootstrap',
                   'gui/{0}'.format(uid),
                   target]

        if self.args.execute:
            self.stderr.write('Bootstrap "{0}"\n'.format(service))            
            subprocess.call(cmdList, stdout=self.stdout)
        else:
            self.stderr.write('command: {0}\n'.format(' '.join(cmdList)))
            self.stderr.write('add -x or --execute flag to execute command.\n')           

class LaunchdBootout(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service
        uid = os.getuid()

        target = '{0}/Library/LaunchAgents/{1}.plist'.format(os.environ['HOME'],
                                                             service)

        cmdList = ['launchctl',
                   'bootout',
                   'gui/{0}'.format(uid),
                   target]

        if self.args.execute:
            self.stderr.write('Bootout "{0}"\n'.format(service))
            subprocess.call(cmdList, stdout=self.stdout)
        else:
            self.stderr.write('command: {0}\n'.format(' '.join(cmdList)))
            self.stderr.write('add -x or --execute flag to execute command.\n')

class LaunchdReload(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)
        
    def run(self):
        service = self.args.service
        uid = os.getuid()

        source = '{0}.plist'.format(service)
        target = '{0}/Library/LaunchAgents/{1}.plist'.format(os.environ['HOME'],
                                                             service)
        
        if self.args.install:
            if not os.path.exists(source):
                self.stderr.write('ERROR: "{0}" does not exist.\n'.format(source))
                sys.exit(os.EX_NOINPUT)

        stopList = ['launchctl',
                    'bootout',
                    'gui/{0}'.format(uid),
                    target]

        startList = ['launchctl',
                     'bootstrap',
                     'gui/{0}'.format(uid),
                     target]

        if self.args.execute:
            if self.args.install:
                if os.path.exists(target):
                    self.stderr.write('WARNING: overwriting "{0}".\n'.format(target))
                shutil.copyfile(source, target)
            
            self.stderr.write('Stopping "{0}"\n'.format(service))
            subprocess.call(stopList, stdout=self.stdout)
            self.stderr.write('Starting "{0}"\n'.format(service))            
            subprocess.call(startList, stdout=self.stdout)            
        else:
            if self.args.install:
                if os.path.exists(target):
                    self.stderr.write('WARNING: this command will overwrite "{0}".\n'.format(target))
                self.stderr.write('command: cp {0} {1}\n'.format(source, target))                    
            
            self.stderr.write('command: {0}\n'.format(' '.join(stopList)))
            self.stderr.write('command: {0}\n'.format(' '.join(startList)))            
            self.stderr.write('add -x or --execute flag to execute commands.\n')

class LaunchdDisable(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service
        uid = os.getuid()

        loginSpecifier = 'gui/{uid}/{service}'.format(uid=uid, service=service)

        cmdList = ['launchctl',
                   'disable',
                   loginSpecifier]

        if self.args.execute:
            subprocess.call(cmdList, stdout=self.stdout)
        else:
            self.stderr.write('command: {0}\n'.format(' '.join(cmdList)))
            self.stderr.write('add -x or --execute flag to execute command.\n')


class LaunchdEnable(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service
        uid = os.getuid()

        loginSpecifier = 'gui/{uid}/{service}'.format(uid=uid, service=service)

        cmdList = ['launchctl',
                   'enable',
                   loginSpecifier]

        if self.args.execute:
            subprocess.call(cmdList, stdout=self.stdout)
        else:
            self.stderr.write('command: {0}\n'.format(' '.join(cmdList)))
            self.stderr.write('add -x or --execute flag to execute command.\n')
            
            
class LaunchdPrint(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        service = self.args.service
        uid = os.getuid()
        
        loginSpecifier = 'gui/{uid}/{service}'.format(uid=uid, service=service)
        cmdList = ['launchctl',
                   'print',
                   loginSpecifier]

        subprocess.call(cmdList, stdout=self.stdout)

class LaunchdDir(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)

    def run(self):
        target = '{0}/Library/LaunchAgents/'.format(os.environ['HOME'])
        
        cmdList = [
            'ls',
            '-l',
            target
            ]
            
        subprocess.call(cmdList, stdout=self.stdout)
        

class LaunchdCreate(LaunchdBase):
    def __init__(self, args):
        super().__init__(args)
        
    
    def run(self):
        def parseTimestamp(buf):
            bufList = buf.split(':')
            hour = int(bufList[0])
            minutes = int(bufList[1])
            return { 'Hour': hour, 'Minute': minutes }

        args = self.args

        plistDict = {}

        if args.program:
            program = os.path.abspath(args.program)
            if program[0] != '/':
                self.stderr.write('WARNING: program "{0}" is not a full path.\n'.format(program))
            plistDict['Program'] = program

            if args.program_arguments:
                plistDict['ProgramArguments'] = [program] + args.program_arguments

        if args.daily:
            timestamps = list(map(parseTimestamp, args.daily))
            plistDict['StartCalendarInterval'] = timestamps

        if args.service:
            plistDict['Label'] = args.service

        if args.working_directory:
            plistDict['WorkingDirectory'] = os.path.abspath(args.working_directory)

        if args.standard_out_path:
            plistDict['StandardOutPath'] = os.path.abspath(args.standard_out_path)
            
        if args.standard_error_path:
            plistDict['StandardErrorPath'] = os.path.abspath(args.standard_error_path)
            
        if args.execute:
            self.stdout.write(json.dumps(plistDict, indent=4))            
            outfileName = '{}.plist'.format(args.service)
            with open(outfileName, 'wb') as outfile:
                plistlib.dump(plistDict, outfile)

        else:
            self.stderr.write(json.dumps(plistDict, indent=4))                        
  
            
        # wrap up 
        if self.stdout != sys.stdout:
            self.stdout.close()

if __name__ == '__main__':
    prog = 'launchutil'
    description = """Utility to create and run a simple launchd service."""
    epilog = """launchutil is a helper utility to support creating and running a
    simple launchd service that is run daily. It is intended to make working
    with launchd more ergonomic by allowing specification of the service
    be either by its service name (aka label) or by plist file name
    defining the service.
    """
    cmdParser = CommandLineParser(
        prog=prog,
        description=description,
        epilog=epilog,
        version=VERSION
    )

    args = cmdParser.run()

    if len(sys.argv) < 2:
        cmdParser.parser.print_help()
    else:
        args.func(args)
