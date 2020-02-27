import datetime
import random

import sys

from colosseum import Colosseum
from constants import COLOSSEUM, LOGDIR, QUEUEDIR, PNG, IMG, PICK, FILES
from io_sama import InputKun, OutputChan


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

# random.seed(datetime.datetime.now().second)
# colosseum = Colosseum()
# i = 1
# while not colosseum.is_over():
#     print("Ronda " + str(i) + ": " + colosseum.let_the_games_begin())
#     i += 1


# def sensoo_wa_kawatta():
#     colosseum=None
#     try:
#         InputKun.load_pickle(COLOSSEUM)
#     except:
#         return


def stateful_call(tweet_for_real=True):
    colosseum = InputKun.load_pickle(FILES + COLOSSEUM + PICK)
    if colosseum is None:
        colosseum = Colosseum()

    ruta_img = IMG + PNG
    if not colosseum.is_over():
        tweet = colosseum.let_the_games_begin()
        colosseum.generateStatusImage(ruta_img)
        OutputChan.log_tweet(LOGDIR, tweet, ruta_img, colosseum)
        OutputChan.queue_tweet(QUEUEDIR, tweet, ruta_img, colosseum)
        OutputChan.process_queue(QUEUEDIR, tweet_for_real)
        OutputChan.save_pickle(FILES + COLOSSEUM + PICK, colosseum)

        # TODO Make this func so it sends all tweets in the queue directory (if successfully sent, deletes crom queue)
        if colosseum.is_over():
            # TODO Congratulations message (method in colosseum)
            print(str(colosseum.stats.winner) + " ha ganado")
            # colosseum.congratulations()
    else:
        print("Owarida")


def stateful_dequeue():
    colosseum = InputKun.load_pickle(COLOSSEUM)
    if colosseum is None:
        raise Exception("Wrong pickle")
    OutputChan.process_queue(QUEUEDIR)
    # TODO Make this func so it sends all tweets in the queue directory (if successfully sent, deletes crom queue)


def test_tweet_api():
    OutputChan.tweet_text("*...generating minimal aliveness scenarios**[2356E]", True)


if __name__ == "__main__":
    print(sys.argv[1])

    mode = sys.argv[1]
    if mode == "test_tweet":
        test_tweet_api()
    elif mode == "test_state":
        stateful_call(False)
    else:
        print("I did nuthing")
