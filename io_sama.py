import datetime
import os
import pickle
import re
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
    def list_files_in_dir(dir):
        files = [f for f in listdir(dir) if isfile(join(dir, f))]
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
    def load_pickle(file_str):
        f = open(file_str, 'rb')
        listaObj = pickle.load(f)
        f.close()
        return listaObj

    @staticmethod
    def load_queued_tweets(directory):
        if not os.path.isdir(directory):
            return ""
        regex = re.compile("^tweet([0-9]{8})\.txt$")
        queue= InputChan.list_files_in_dir(directory)
        if len(queue)<1:
            return ""
        else:
            qtweets=[file for file in queue if regex.match(file.name)]

            for tmp_tweet in qtweets:
                date_extension= regex.match(tmp_tweet).group(1)
                if not os.path.isfile(directory + "/" + IMG + date_extension + TXT):
                    return "No tweet image"





    # TODO load_queued tweets to be used by ¿Outputchan? YESSSS! CORRECT!!


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
    def tweet(tweet, image_path, colosseum_str=None, live=True):
        if not live:
            return

        InputKun.read_tokens(TOKENSFILE)
        atd = ACCESS_TOKENS_DIC

        try:
            api = Twython(atd.CONSUMER_KEY, atd.CONSUMER_SECRET, atd.ACCESS_KEY, atd.ACCESS_SECRET)
            photo = open(image_path, 'rb')
            image_ids = api.upload_media(media=photo)
            api.update_status(status=tweet, media_ids=image_ids['media_id'])
        except TwythonError:
            #OutputChan.queue_tweet(QUEUEDIR, tweet, image_path, colosseum_str)
            raise TwythonError("Failed to tweet. Queued tweet")

    def delete_queued_tweet(tweet_file, img_file, colosseum_file):
        os.remove(tweet_file)
        os.remove(img_file)
        os.remove(colosseum_file)

    def process_queue(directory, live=False):
        #TODO change this so tweets have ID instead of timestamp and I just give an ID to delete
        #This is a list of lists. Each sublist contains the filenames for the tweet, the image and the colosseum pickle (the last one is not used in this case)
        almighty_tweet_queue= InputKun.load_queued_tweets(directory)
        for tweet_element in almighty_tweet_queue:
            tweet_text= open(tweet_element[0], "r").readline
            try:
                tweet(tweet_text, tweet_element[1], tweet_element[2], live)
                delete_queued_tweet(tweet_element[0], tweet_element[1], tweet_element[2])
            except TwythonError as e:
                print(str(e))

