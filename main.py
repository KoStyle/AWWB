import sys
from time import sleep

from colosseum import Colosseum
from constants import COLOSSEUM, LOGDIR, QUEUEDIR, PNG, IMG, PICK, FILES
from io_sama import InputKun, OutputChan


# TODO v3 ideas:
# Kill by popular demand (events that wait for user interaction. needs from IO_Sama)
# Log and queue as pickle class instead of folders
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
            tweet = colosseum.omedetoo()
            OutputChan.tweet_text(tweet, tweet_for_real)
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
    OutputChan.tweet_text(
        "Buenas noches a todos. En caso de emergencia, recuerden: Todas las salidas han sido selladas. Seguiremos informando [BIP BOOP]",
        True)


def test_tweet_api_img():
    OutputChan.tweet_image("Getting ready for you <3", "files/terminator.jpg", True)


def reload_files():
    colosseum = InputKun.load_pickle(FILES + COLOSSEUM + PICK)
    if colosseum is None:
        colosseum = Colosseum()
    colosseum.refresh_flavours()
    OutputChan.save_pickle(FILES + COLOSSEUM + PICK, colosseum)


def presentation(live=False):
    colosseum = InputKun.load_pickle(FILES + COLOSSEUM + PICK)
    if colosseum is None:
        colosseum = Colosseum()
        OutputChan.save_pickle(FILES + COLOSSEUM + PICK, colosseum)

    presentations = colosseum.get_presentations()

    OutputChan.tweet_text(
        "Hoy empieza la batalla por la supervivencia. Ya sabéis como funciona. Cada día a las 12:00 me encargaré de "
        "actualizaros. Pero antes de empezar, demos la bienvenida a los participantes!!", live)

    for present in presentations:
        OutputChan.tweet_text(present, live)
        sleep(1)


if __name__ == "__main__":
    print(sys.argv[1])

    mode = sys.argv[1]
    if mode == "test_tweet":
        test_tweet_api()
    elif mode == "test_image":
        test_tweet_api_img()
    elif mode == "test_intro":
        presentation()
    elif mode == "test_state":
        stateful_call(False)
    elif mode == "run_state":
        stateful_call(True)
    elif mode == "run_intro":
        presentation(True)
    elif mode == "reload_files":
        reload_files()
    else:
        print("I did nuthing")
