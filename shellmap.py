#!/usr/bin/env python

'''
Script to generate and chain/sequence shell commands
using placeholder substitution.

Pranav Ravichandran <me@onloop.net>
'''

import argparse
import subprocess as sp
import sys
import re

class PosArgMap:
    def __init__(self, commands, paramlists):
        self.commands = commands
        self.paramlists = paramlists

    def map_interpolate(self, command, params, position):
        ''' Take a command, a list of parameters, and a placeholder position,
        and map string interpolation of the placeholder over the parameters. '''
        return map(lambda param: command.replace('$' + str(position) + '@', param), params)

    def map_across_commands(self, commands, params, position):
        ''' Map map_interpolate across multiple commands and return a flat result list. '''
        flatlist = []
        map(lambda command:
            flatlist.extend(self.map_interpolate(command, params, position)),
            commands)
        return flatlist

    def fold_interpolate(self, commands, paramlists, position=1):
        ''' Recursive function to replace placeholders until none exist. '''
        if not re.search('\$\d+\@', commands[0]):
            return commands
        else:
            return self.fold_interpolate(self.map_across_commands(
                commands, paramlists[0], position),
                paramlists[1:], position + 1)

    def resolve(self):
        ''' Wrapper function to resolve the class object using fold_interpolate. '''
        return self.fold_interpolate(self.commands, self.paramlists)

def PosArg(value):
    ''' Custom argparse type to check if input is a command, and if it is,
    return the result of the command, else return a list. '''
    if value[0] == '%':
        return sp.check_output(value[1:], shell=True, stderr=sp.STDOUT).splitlines()
    else:
        return value.split(',')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chain/sequence shell scripts.')

    parser.add_argument('command', metavar="N", type=PosArg, nargs="+",
                       help="Command string with placeholders, followed by arguments.")
    parser.add_argument('--print', dest='printout',
                        help="Print the output commands", action="store_true")
    parser.add_argument('--run', dest='run',
                        help="Run the output commands", action="store_true")
    args = parser.parse_args()

    final_commands = PosArgMap(args.command[0], args.command[1:])
    to_run = final_commands.resolve()

    if args.printout:
        print '\n'.join(to_run)

    if args.run:
        for each_command in to_run:
            sp.call(to_run, shell=True)

