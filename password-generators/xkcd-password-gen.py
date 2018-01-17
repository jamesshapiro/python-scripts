#!/usr/bin/env python3 -tt

"""Usage:
  xkcd-password-gen.py [options]

Options:
  -h --help            show this help message and exit
  --numwords NUM       number of words [default: 4]
  --numcharacters NUM  number of passwords [default: 4]
  --numpasswords NUM   number of passwords [default: 1]
"""
import random
from docopt import docopt

loIO01 = 'loIO01'
lower = ''.join(list(set('abcdefghijklmnopqrstuvwxyz') - set(loIO01)))
upper = ''.join(list(set('ABCDEFGHIJKLMNOPQRSTUVWXYZ') - set(loIO01)))
number = ''.join(list(set('0123456789') - set(loIO01)))
symbol = '!@#$%^&*_+?-='
symbol_ambiguous = '{}[]()~,;:.<>'

with open('/usr/share/dict/words', 'r') as f:
    lines = f.readlines()
    words = [word.strip() for word in lines]

def generate_passwords():
    num_words = int(arguments['--numwords'])
    num_characters = int(arguments['--numcharacters'])
    num_passwords = int(arguments['--numpasswords'])
    characters = lower + upper + number + symbol + symbol_ambiguous
    characters_list = list(set(characters) - set(loIO01))
    characters = ''.join(characters_list)
    for _ in range(num_passwords):
        password = ''
        for _ in range(num_words):
            password += words[random.randrange(len(words))]
        for _ in range(num_characters):
            password += random.choice(characters)
        print(password)

if __name__ == "__main__":
    arguments = docopt(__doc__)
    generate_passwords()
