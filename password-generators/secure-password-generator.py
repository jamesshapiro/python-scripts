#!/usr/bin/env python3 -tt

import argparse
import random

def parse_args():
    p = argparse.ArgumentParser(description='Secure password generator')
    p.add_argument('--nolower', action='store_true', help="exclude lowercase letters")
    p.add_argument('--noupper', action='store_true', help="exclude uppercase letters")
    p.add_argument('--nonumber', action='store_true', help="exclude numbers")
    p.add_argument('--nosymbol', action='store_true', help="exclude all symbols")
    p.add_argument('--nosymbolambi', action='store_true', help="exclude '{}[]()~,;:.<>'")
    p.add_argument('--yesalphaambi', action='store_true', help="include 'loIO01' (excluded by default)")
    p.add_argument('--length', type=int, default=16, metavar='LENGTH', help='password length')
    p.add_argument('--numpasswords', type=int, default=1, metavar='NUM', help='number of passwords')
    p.add_argument('--annoyingreqs', action='store_true', help='add 1+ uppercase, lowercase, number, & symbol to password')
    ns = p.parse_args()
    return {
        '--nolower': ns.nolower, '--noupper': ns.noupper, '--nonumber': ns.nonumber,
        '--nosymbol': ns.nosymbol, '--nosymbolambi': ns.nosymbolambi, '--yesalphaambi': ns.yesalphaambi,
        '--length': str(ns.length), '--numpasswords': str(ns.numpasswords), '--annoyingreqs': ns.annoyingreqs,
    }

arguments = parse_args()
    
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
number = '0123456789'
loIO01 = 'loIO01'
symbol = '!@#$%^&*_+?-='
ambiguous_symbols = '{}[]()~,;:.<>'

def exclude(characters, alphabet):
    return "".join(list(set(alphabet) - set(characters)))

def get_alphabet(arguments):
    alphabet = ''.join([lower, upper, number, symbol, ambiguous_symbols])
    if not arguments['--yesalphaambi']:
        alphabet = exclude(loIO01, alphabet)
    if arguments['--nolower']:
        alphabet = exclude(lower, alphabet)
    if arguments['--noupper']:
        alphabet = exclude(upper, alphabet)
    if arguments['--nonumber']:
        alphabet = exclude(number, alphabet)
    if arguments['--nosymbolambi']:
        alphabet = exclude(ambiguous_symbols, alphabet)
    if arguments['--nosymbol']:
        alphabet = exclude(ambiguous_symbols, alphabet)
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

if __name__ == "__main__":
    generate_passwords(arguments)
