#!/usr/bin/env python3 -tt
import random

characters = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*():;+=~|?"
password = ""
suffix = ""
with open('/usr/share/dict/words', 'r') as f:
    lines = f.readlines()
words = [word.strip() for word in lines]
    
for _ in range(4):
    password += words[random.randrange(len(words))]
    suffix += characters[random.randrange(len(characters))]

password = password + suffix
print(password)
