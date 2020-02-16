import pickle
import os
import random
import math

from pip._internal.utils.deprecation import deprecated

import util
from classes import Colosseum
from util import read_file
import twython
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from twython import Twython
from shutil import copyfile


# TODO ideas:
# Events structure
# Kills (Done)
# Coffees (Done)
# Suicides (Done)
# Draws
# Love affairs (possibility of magnetismn between player (makes them more likely to kill eachother))
# Missed hits/defense teamups
# Revives (Done)
# Curses (Done)

# Event randomization (in progress)

# EasterEggs for certain combinations
# Neutral Manu

# Support for mentions


def generateStatusImage(lista):
    pic = Image.open(util.IMG + util.PNG)
    width, height = pic.size
    col = width / 3.0
    rows = math.ceil(len(lista) / 3.0)
    row = height / rows
    draw = ImageDraw.Draw(pic)
    font = ImageFont.truetype(util.FONT, 20)
    draw.rectangle((0, 0, width, height), (255, 255, 255))

    for i in range(len(lista)):
        x = math.floor(i / rows) * col + 20
        y = i % rows * row + 20
        xl, yl = font.getsize(lista[i].name)

        draw.text((x, y), lista[i].name + ' (' + str(lista[i].kills) + ' kills)', (0, 0, 0), font=font)
        if not lista[i].isAlive:
            draw.line((x, y, x + xl, y + yl), (255, 0, 0), 5)
    pic.save(util.IMG + util.PNG)


##script

colosseum = Colosseum()
while not colosseum.is_over():
    colosseum.let_the_games_begin()

