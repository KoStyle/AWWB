import datetime
import os
import pickle
import re
from os.path import isfile, join
from shutil import copyfile

from twython import Twython, TwythonError

from constants import ACCESS_TOKENS_DIC, TXT, TWEETLOG, COLOSSEUM, IMG, PNG, TOKENSFILE, QUEUEDIR


class InputKun:

    @staticmethod
    def read_file(file):
        lista = []
        try:
            f = open(file, 'r', encoding='latin1')
        except FileNotFoundError:
            f = open(file, 'w+', encoding='latin1')
        line = f.readline()
        while line:
            lista.append(line.strip())
            line = f.readline()
        return lista

    @staticmethod
    def list_files_in_dir(container):
        files = [f for f in os.listdir(container) if isfile(join(container, f))]
        return files

    @staticmethod
    def read_tokens(file):
        f = open(file, 'r', encoding='latin1')
        line = f.readline()
        while line:
            tokenized = line.split('=')
            if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is None and len(tokenized) == 2:
                ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
            line = f.readline()
        return

    @staticmethod
    def load_pickle(file):
        f = open(file, 'rb')
        thing = pickle.load(f)
        f.close()
        return thing

    @staticmethod
    def load_queued_tweet():
        if not os.path.isdir(QUEUEDIR):
            return ""
        regex = re.compile("^tweet([0-9]{8})\.txt$")
        queue = InputKun.list_files_in_dir(QUEUEDIR)
        if len(queue) < 1:
            return ""

        qtweets = [file for file in queue if regex.match(file.name)]

        for tmp_tweet in qtweets:
            date_extension = regex.match(tmp_tweet).group(1)
            if not os.path.isfile(QUEUEDIR + "/" + IMG + date_extension + TXT):
                return "No tweet image"


    # TODO Use exceptions in these methods instead of returning ""


class OutputChan:
    @staticmethod
    def save_pickle(file, obj):
        f = open(file, 'wb')
        pickle.dump(obj, f)
        f.close()

    @staticmethod
    def log_tweet(log_path, tweet, img_path, colosseum):
        now = datetime.datetime.now().strftime('%Y%m%d%H%M')
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        tweet_file = open(log_path + "/" + TWEETLOG + now + TXT, "w")
        tweet_file.write(tweet)

        OutputChan.save_pickle(COLOSSEUM + now + TXT, colosseum)
        copyfile(img_path, log_path + "/" + IMG + now + PNG)

    @staticmethod
    def queue_tweet(queue_path, tweet, img_path, colosseum):
        OutputChan.log_tweet(queue_path, tweet, img_path, colosseum)

    @staticmethod
    def tweet(tweet, image_path, colosseum):
        InputKun.read_tokens(TOKENSFILE)
        atd = ACCESS_TOKENS_DIC

        try:
            api = Twython(atd.CONSUMER_KEY, atd.CONSUMER_SECRET, atd.ACCESS_KEY, atd.ACCESS_SECRET)
            photo = open(image_path, 'rb')
            image_ids = api.upload_media(media=photo)
            api.update_status(status=tweet, media_ids=image_ids['media_id'])
        except TwythonError:
            OutputChan.queue_tweet(QUEUEDIR, tweet, image_path, colosseum)
