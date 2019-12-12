# simplecal.py

I love the unix "cal" feature, but I find myself normally only caring about the current month and the month after it. "cal -y" normally does the trick, but is slight overkill. It also doesn't work well near the end of the year, when I want to look at dates across December and January.

simplecal.py looks up the current month and prints the succeeding "n" months (default 3).

Usage (as of 12/12/2019): python3 simplecal.py 2

Yields:

   December 2019          January 2020
Mo Tu We Th Fr Sa Su  Mo Tu We Th Fr Sa Su
                   1         1  2  3  4  5
 2  3  4  5  6  7  8   6  7  8  9 10 11 12
 9 10 11 12 13 14 15  13 14 15 16 17 18 19
16 17 18 19 20 21 22  20 21 22 23 24 25 26
23 24 25 26 27 28 29  27 28 29 30 31
30 31
