#!/usr/bin/env python3 -tt

import sys
import random
import re

lower = "abcdefghijklmnopqrstuvwxyz"
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number = "0123456789"
loIO01 = "loIO01"
symbol = "!@#$%^&*_+?-="
symbolAmbiguous = "{}[]()/\\`~,;:.<>"

def generatePassword(alphabet, length, numPasswords=1, annoyingReqs = False):
    for _ in range(numPasswords):
        password = "".join([random.choice(alphabet) for _ in range(length)])
        if annoyingReqs:
            lower_set = ''.join(list(set(lower) - set(loIO01)))
            upper_set = ''.join(list(set(upper) - set(loIO01)))
            number_set = ''.join(list(set(number) - set(loIO01)))
            password = password[4:]
            password += random.choice(lower_set) + random.choice(upper_set)
            password += random.choice(number_set) + random.choice(symbol)
            password_list = list(password)
            random.shuffle(password_list)
            password = ''.join(password_list)
        print(password)

firstLine  = '[options] = {} (exclude {}, included by default)'
includeStr = '            {} (exclude {}, included by default)'
excludeStr = '            {} (include {}, excluded by default)'
numArg =     '            {} ({} by default)'

def __main__():
    kwargs = {}
    kwargs['length']=16
    if not "--justpasswords" in sys.argv:
        print("Welcome to the secure password generator!")
    if "--help" in sys.argv:
        print("Usage: ./secure-password-generator.py [options]")
        print(firstLine.format("--nolower", "lowercase letters"))
        print(includeStr.format("--noupper", "uppercase letters"))
        print(includeStr.format("--nonumber", "numbers"))
        print(includeStr.format("--nosymbol", "all symbols"))
        print(includeStr.format("--nosymbolambi", '"' + symbolAmbiguous + '"'))
        print(excludeStr.format("--yesalphaambi", '"' + loIO01 + '"'))
        print(numArg.format("--length=[password_length]", "password length is 16"))
        print(numArg.format("--numpasswords=[num_passwords]",
                            "generates 1 password"))
        print("            --annoyingreqs (1+ uppercase, lowercase, number and symbol)")
        print("            --justpasswords (do not display any prompts)")
        print("\nEx:    ./secure-password-generator.py --nosymbolambi --length=20"
              + " --numpasswords=10\n")
        return
    if not "--justpasswords" in sys.argv:
        print("  (For help, try: ./secure-password-generator.py --help)\n")
    args = [lower, upper, number, symbol, symbolAmbiguous]
    lengthRE = re.compile("--length=(\d+)")
    numPasswordsRE = re.compile("--numpasswords=(\d+)")
    if any([lengthRE.match(arg) for arg in sys.argv]):
        kwargs["length"] = int(next(lengthRE.match(arg).group(1)
                                    for arg in sys.argv if lengthRE.match(arg)))
    if any([numPasswordsRE.match(arg) for arg in sys.argv]):
        kwargs["numPasswords"] = int(next(numPasswordsRE.match(arg).group(1)
                                    for arg in sys.argv if numPasswordsRE.match(arg)))
    if "--annoyingreqs" in sys.argv:
        kwargs["annoyingReqs"] = True
    if not "--justpasswords" in sys.argv:
        print("password(s):")
    
    alphabet = "".join(args)
    if "--yesalphaambi" not in sys.argv:
        alphabet = exclude(loIO01, alphabet)
    if "--nolower" in sys.argv:
        alphabet = exclude(lower, alphabet)
    if "--noupper" in sys.argv:
        alphabet = exclude(upper, alphabet)
    if "--nonumber" in sys.argv:
        alphabet = exclude(number, alphabet)
    if "--nosymbolambi" in sys.argv and symbolAmbiguous in args:
        alphabet = exclude(symbolAmbiguous, alphabet)
    if "--nosymbol" in sys.argv:
        alphabet = exclude(symbolAmbiguous, alphabet)
        alphabet = exclude(symbol, alphabet)
    generatePassword(alphabet, **kwargs)

def exclude(characters, alphabet):
    return "".join(list(set(alphabet) - set(characters)))

__main__()
