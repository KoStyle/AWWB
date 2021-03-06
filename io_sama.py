import datetime
import ntpath
import os
import pickle
import re
from os.path import isfile, join
from shutil import copyfile

from twython import Twython, TwythonError

import util
from constants import ACCESS_TOKENS_DIC, TXT, COLOSSEUM, PNG, TOKENSFILE, IMGPREFIX, TWEETPREFIX


class InputKun:

    @staticmethod
    def read_file(file):
        lista = []
        try:
            f = open(file, 'r', encoding='UTF-16')
        except FileNotFoundError:
            f = open(file, 'w+', encoding='UTF-16')
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
        f = open(file, 'r', encoding='UTF-16')
        line = f.readline()
        while line:
            tokenized = line.split('=')
            if ACCESS_TOKENS_DIC.get(tokenized[0].strip()) is not None and len(tokenized) == 2:
                ACCESS_TOKENS_DIC[tokenized[0].strip()] = tokenized[1].strip()
            line = f.readline()
        return

    @staticmethod
    def load_pickle(file_str):
        try:
            f = open(file_str, 'rb')
        except FileNotFoundError:
            return None
        thing = pickle.load(f)
        f.close()
        return thing

    # TODO v3: create a tweet bean that keeps all. Binary img, colloseum reference and tweet text. All in a pickle.
    @staticmethod
    def load_queued_tweets(directory):
        if not os.path.isdir(directory):
            return ""
        regex = re.compile("^tweet([0-9]{12})\.txt$")
        queue = InputKun.list_files_in_dir(directory)
        if len(queue) < 1:
            return ""

        sweet_tweet_info = []
        qtweets = [file for file in queue if regex.match(file)]

        for tmp_tweet in qtweets:
            single_tweet = []
            date_extension = regex.match(tmp_tweet).group(1)
            if os.path.isfile(directory + IMGPREFIX + date_extension + PNG):
                single_tweet.append(directory + tmp_tweet)
                single_tweet.append(directory + IMGPREFIX + date_extension + PNG)
                sweet_tweet_info.append(single_tweet)

        return sweet_tweet_info

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
        img_filename = ntpath.basename(img_path)
        if not os.path.isdir(log_path):
            os.mkdir(log_path)

        tweet_file = open(log_path + TWEETPREFIX + now + TXT, "w+", encoding='UTF-16')
        tweet_file.write(tweet)
        tweet_file.close()
        OutputChan.save_pickle(log_path + COLOSSEUM + now + TXT, colosseum)
        copyfile(img_path, log_path + img_filename.split(".")[0] + now + PNG)

    @staticmethod
    def queue_tweet(queue_path, tweet, img_path, colosseum):
        OutputChan.log_tweet(queue_path, tweet, img_path, colosseum)

    @staticmethod
    def tweet_image(tweet, image_path, live=False):

        InputKun.read_tokens(TOKENSFILE)
        atd = ACCESS_TOKENS_DIC

        try:
            api = Twython(atd['CONSUMER_KEY'], atd['CONSUMER_SECRET'], atd['ACCESS_KEY'], atd['ACCESS_SECRET'])
            photo = open(image_path, 'rb')
            image_ids = api.upload_media(media=photo)
            if not live:
                # Only for testing
                print(tweet)
            else:
                api.update_status(status=tweet, media_ids=image_ids['media_id'])
        except TwythonError:
            raise TwythonError("Failed to tweet. Queued tweet")

    @staticmethod
    def tweet_text(tweet, live=False):

        InputKun.read_tokens(TOKENSFILE)
        atd = ACCESS_TOKENS_DIC
        try:
            api = Twython(atd['CONSUMER_KEY'], atd['CONSUMER_SECRET'], atd['ACCESS_KEY'], atd['ACCESS_SECRET'])
            if not live:
                if len(tweet) > 270:
                    halves = util.split_tweet(tweet)
                    print(halves[0])
                    print(halves[1])
                else:
                    print(tweet)
            else:
                if len(tweet) > 270:
                    halves = util.split_tweet(tweet)
                    api.update_status(status=halves[0])
                    api.update_status(status=halves[1])
                else:
                    api.update_status(status=tweet)
        except TwythonError as e:
            print(str(e))
            # OutputChan.queue_tweet(QUEUEDIR, tweet, image_path, colosseum_str)
            raise TwythonError("Failed to tweet. Queued tweet")

    # TODO change this so tweets have ID instead of timestamp and I just give an ID to delete

    @staticmethod
    def delete_queued_tweet(tweet_file, img_file):
        os.remove(tweet_file)
        os.remove(img_file)

    @staticmethod
    def process_queue(directory, live=False):
        # This is a list of lists. Each sublist contains the filenames for the tweet, the image and the colosseum pickle (the last one is not used in this case)
        almighty_tweet_queue = InputKun.load_queued_tweets(directory)
        for tweet_element in almighty_tweet_queue:
            tweet_text = open(tweet_element[0], "r", encoding='UTF-16').readline()
            try:
                OutputChan.tweet_image(tweet_text, tweet_element[1], live)
                OutputChan.delete_queued_tweet(tweet_element[0], tweet_element[1])
            except TwythonError as e:
                print(str(e))
