#!/usr/bin/env python3 -tt
"""Example of program which uses [options] shortcut in pattern.

Usage:
  options_shortcut_example.py [options]

Options:
  -h --help                show this help message and exit
  --version                show version and exit
  --nolower                Exclude lowercase letters, included by default
  --noupper                Exclude uppercase letters, included by default
  --nonumber               Exclude numbers, included by default
  --nosymbol               Exclude all symbols, included by default
  --nosymbolambi           Exclude "{}[]()/\`~,;:.<>", included by default
  --yesalphaambi           Include "loIO01", excluded by default
  --length LENGTH          Password length [default: 16]
  --numpasswords NUM       Number of passwords [default: 1]
  --annoyingreqs           1+ uppercase, lowercase, number and symbol
  --justpasswords          Do not display any prompts
"""
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='2.0')
    print(arguments)
