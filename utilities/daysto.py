#!/usr/bin/env python3 -tt

"""Usage:
  daysto.py DATE

Options:
  -h --help           show this HELP message and exit
"""

from datetime import date
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Reminders 0.1')
    today = date.today()
    target_date = arguments['DATE']
    month, day, year = map(int, target_date.split('-'))
    target_date = date(year, month, day)
    delta = str(target_date - today).split(' ')
    print(delta[0])
