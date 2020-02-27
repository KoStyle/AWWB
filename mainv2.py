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



##script
random.seed(datetime.datetime.now().second)
colosseum = Colosseum()
i = 1
while not colosseum.is_over():
    print("Ronda " + str(i) + ": " + colosseum.let_the_games_begin())
    i += 1


def stateful_call(tweet_for_real=True):
    colosseum=InputKun.load_pickle(COLOSSEUM)
    if colosseum==None :
        colosseum=Colosseum()


    tweet=""
    ruta_img= IMG + PNG
    if not colosseum.is_over():
        tweet=colosseum.let_the_games_begin()
        colosseum.generateStatusImage(ruta_img)
        OutputChan.log_tweet(LOGDIR, tweet, ruta_img, colosseum)
        OutputChan.queue_tweet(QUEUEDIR ,tweet, ruta_img, colosseum)
        OutputChan.process_queue(QUEUEDIR, tweet_for_real)  #TODO Make this func so it sends all tweets in the queue directory (if successfully sent, deletes crom queue)
        
        if colosseum.is_over():
            #TODO Congratulations message (method in colosseum)
            colosseum.congratulations()

def stateful_dequeue():
    colosseum=InputKun.load_pickle(COLOSSEUM)
    if colosseum==None :
        raise Exception("Wrong pickle")
    OutputChan.process_queue(QUEUEDIR)  #TODO Make this func so it sends all tweets in the queue directory (if successfully sent, deletes crom queue)




