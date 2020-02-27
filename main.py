import datetime
import random

from colosseum import Colosseum
from constants import COLOSSEUM
from io_sama import InputKun

# TODO v2 ideas:
# Events structure (Done)
# Kills (Done)
# Coffees (Done)
# Suicides (Done)
# Draws (Done)
# Revives (Done)
# Curses (Done)
# Event randomization (Done)
# TODO v3 ideas:
# Kill by popular demand (events that wait for user interaction. needs from IO_Sama)
# Rewrite access to the print name of Arpies
# Love affairs (possibility of magnetismn between player (makes them more likely to kill eachother))
# Support for mentions
# Defense teamups
# EasterEggs for certain combinations
### Neutral Manu
### Jeaggerbrothers
### Mon Amour
### Megazord

random.seed(datetime.datetime.now().second)
colosseum = Colosseum()
i = 1
while not colosseum.is_over():
    print("Ronda " + str(i) + ": " + colosseum.let_the_games_begin())
    i += 1


def sensoo_wa_kawatta():
    colosseum=None
    try:
        InputKun.load_pickle(COLOSSEUM)
    except:
        return