import datetime
import math
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import util

from colosseum import Colosseum


# TODO v2 ideas:
# Events structure
# Kills (Done)
# Coffees (Done)
# Suicides (Done)
# Draws (Done)
# Love affairs (possibility of magnetismn between player (makes them more likely to kill eachother))
# Defense teamups
# Revives (Done)
# Curses (Done)
# Event randomization (Done)

# TODO v3 ideas:
# Kill by popular demand (events that wait for user interaction. needs from IO_Sama)
# Support for mentions
# EasterEggs for certain combinations
### Neutral Manu
### Jeaggerbrothers
### Mon Amour
### Megazord

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
random.seed(datetime.datetime.now().second)
colosseum = Colosseum()
i = 1
while not colosseum.is_over():
    print("Ronda " + str(i) + ": " + colosseum.let_the_games_begin())
    i += 1
