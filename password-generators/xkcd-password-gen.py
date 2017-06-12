#!/usr/bin/env python3 -tt
import random
import re
import sys

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number = "0123456789"
loIO01 = "loIO01"
symbol = "!@#$%^&*_+?-="
symbolAmbiguous = "{}[]()/\'\"`~,;:.<>"

with open('/usr/share/dict/words', 'r') as f:
    lines = f.readlines()
    words = [word.strip() for word in lines]

def generatePassword(numPasswords=1, numWords=4, numRandomCharacters=4):
    characters = lower + upper + number + symbol + symbolAmbiguous
    charactersList = list(set(characters) - set(loIO01))
    characters = ''.join(charactersList)
    for _ in range(numPasswords):
        password = ""
        suffix = ""
        for _ in range(numWords):
            password += words[random.randrange(len(words))]
        for _ in range(numRandomCharacters):
            password += random.choice(characters)
        print(password)

def __main__():
    kwargs = {}
    numWordsRE = re.compile("--numwords=(\d+)")
    numPasswordsRE = re.compile("--numpasswords=(\d+)")
    numCharactersRE = re.compile("--numcharacters=(\d+)")
    if any([numWordsRE.match(arg) for arg in sys.argv]):
        kwargs["numWords"] = int(next(numWordsRE.match(arg).group(1)
                                    for arg in sys.argv if numWordsRE.match(arg)))
    if any([numPasswordsRE.match(arg) for arg in sys.argv]):
        kwargs["numPasswords"] = int(next(numPasswordsRE.match(arg).group(1)
                                    for arg in sys.argv if numPasswordsRE.match(arg)))
    if any([numCharactersRE.match(arg) for arg in sys.argv]):
        kwargs["numRandomCharacters"] = int(next(numCharactersRE.match(arg).group(1)
                                    for arg in sys.argv if numCharactersRE.match(arg)))
    generatePassword(**kwargs)

__main__()
