import os
from twython import Twython, TwythonStreamer
from threading import Thread


class Tweet(object):
    SCREEN_NAME = os.getenv("TWITTER_SCREEN_NAME")
    CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    def __init__(self):
        self._thread = None

    def get_tweets(self, count):
        user = Twython(self.CONSUMER_KEY, self.CONSUMER_SECRET,
                       self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

        return user.get_user_timeline(screen_name=self.SCREEN_NAME, count=count)

    def start_stream(self, async=False):
        stream = StreamListener(self.CONSUMER_KEY, self.CONSUMER_SECRET,
                                self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

        if async is True:
            self._thread = Thread(target=stream.user)
            self._thread.daemon = True
            self._thread.start()
        else:
            stream.user()

        return stream


class StreamListener(TwythonStreamer):
    def __init__(self, *args):
        super(StreamListener, self).__init__(*args)

        self._watchers = []

    def add_watcher(self, callback):
        self._watchers.append(callback)

    def on_success(self, data):
        for callback in self._watchers:
            callback(data)
