Two password generators written in Python3.

(1.) Secure Password Generator:

This offline script attempts to replicate the functionality of the password generator at (http://passwordsgenerator.net/). I use it to generate secure passwords locally, without having to trust any website or network!

![alt text](https://raw.githubusercontent.com/jamesshapiro/python-scripts/master/assets/images/secure-password-simple-use.png)

![alt text](https://raw.githubusercontent.com/jamesshapiro/python-scripts/master/assets/images/secure-password-use-case.png)

You can exclude symbols, numbers, lowercase letters, and/or uppercase letters from your passwords using flags. Similar letters/numbers (i.e. "lI1oO0") are excluded by default but can be included with the "--yesalphaambi" flag. secure-password-generator.py also has some additional functionality (i.e. the ability to require one uppercase, one lowercase, one number, and one symbol, for websites that require that):

![alt text](https://raw.githubusercontent.com/jamesshapiro/python-scripts/master/assets/images/secure-password-help.png)

(2.) XKCD Password Generator

I'm not a fan of the web comic XKCD, but the author came up with an interesting secure password proposal (https://xkcd.com/936/) that I've implemented here.

I used the built-in words dictionary provided on Mac and Unix systems. If you're a Windows user, you can download it here: https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt, or use your own.

By default, the script generates a single password with four random words, followed by four random characters:

![alt text](https://raw.githubusercontent.com/jamesshapiro/python-scripts/master/assets/images/xkcd-simple-usage.png)

The number of passwords can be tweaked with the "--numpasswords=x" flag. The number of words can be tweaked with the "--numwords=y" flag. The number of random characters can be tweaked with the "--numcharacters=z" flag:

![alt text](https://raw.githubusercontent.com/jamesshapiro/python-scripts/master/assets/images/xkcd-usage.png)



