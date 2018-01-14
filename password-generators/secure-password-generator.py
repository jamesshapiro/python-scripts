#!/usr/bin/env python3 -tt

"""Usage:
  secure-password-generator.py [options]

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
"""
import random
from docopt import docopt

arguments = docopt(__doc__, version='2.0')
    
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
number = '0123456789'
loIO01 = 'loIO01'
symbol = '!@#$%^&*_+?-='
symbolAmbiguous = '{}[]()/\\~,;:.<>'

def exclude(characters, alphabet):
    return "".join(list(set(alphabet) - set(characters)))

def get_alphabet(arguments):
    alphabet = ''.join([lower, upper, number, symbol, symbolAmbiguous])
    if not arguments['--yesalphaambi']:
        alphabet = exclude(loIO01, alphabet)
    if arguments['--nolower']:
        alphabet = exclude(lower, alphabet)
    if arguments['--noupper']:
        alphabet = exclude(upper, alphabet)
    if arguments['--nonumber']:
        alphabet = exclude(number, alphabet)
    if arguments['--nosymbolambi'] and symbolAmbiguous in args:
        alphabet = exclude(symbolAmbiguous, alphabet)
    if arguments['--nosymbol']:
        alphabet = exclude(symbolAmbiguous, alphabet)
        alphabet = exclude(symbol, alphabet)
    return alphabet

def generate_passwords(arguments):
    alphabet = get_alphabet(arguments)
    num_passwords = int(arguments['--numpasswords'])
    for _ in range(num_passwords):
        length = int(arguments['--length'])
        password = "".join([random.choice(alphabet) for _ in range(length)])
        if arguments['--annoyingreqs']:
            lower_set = ''.join(list(set(lower) - set(loIO01)))
            upper_set = ''.join(list(set(upper) - set(loIO01)))
            number_set = ''.join(list(set(number) - set(loIO01)))
            special_char_sets = [lower_set, upper_set, number_set, symbol]
            password = password[4:]
            password += ''.join([random.choice(char_set) for char_set in special_char_sets])
            password_list = list(password)
            random.shuffle(password_list)
            password = ''.join(password_list)
        print(password)

def __main__():
    args = [lower, upper, number, symbol, symbolAmbiguous]
    generate_passwords(arguments)

__main__()
