#!/bin/env python

import argparse
import subprocess as sp
import sys

class PosArgMap:
    def __init__(self, commands, paramlists):
        self.commands = commands
        self.paramlists = paramlists

    def map_interpolate(self, command, params):
        return map(lambda param: command.replace('$@', param, 1), params)

    def map_across_commands(self, commands, params):
        flatlist = []
        map(lambda command:
            flatlist.extend(self.map_interpolate(command, params)),
            commands)
        return flatlist

    def fold_interpolate(self, commands, paramlists):
        if not paramlists:
            return commands
        else:
            return self.fold_interpolate(self.map_across_commands(commands,
                                                                  paramlists[0]),
                                         paramlists[1:])

    def resolve(self):
        return self.fold_interpolate(self.commands, self.paramlists)

def PosArg(value):
    if value[0] == '%':
        return sp.check_output(value[1:], shell=True, stderr=sp.STDOUT).splitlines()
    else:
        return value.split(',')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chain scripts.')
    parser.add_argument('command', type=PosArg, nargs="+")
    parser.add_argument('--run', dest='run', action="store_true")

    args = parser.parse_args()

    final_commands = PosArgMap(args.command[0], args.command[1:])
    to_run = final_commands.resolve()

    if args.run:
        for each_command in to_run:
            sp.call(to_run, shell=True)

