#!/bin/env python

import argparse
import subprocess

class ShellMap:
    def __init__(self, command, *args):
        self.commands = [command]
        self.paramlists = args

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

