import re
import widgets

from kivy.animation import Animation
from kivy.clock import Clock
from twitter import Tweet


class TweetController(object):
    KEYS = {
        "gif_keys": ["media", 0, "video_info", "variants", 0, "url"],
        "vid_keys": ["media", 0, "video_info", "variants", 1, "url"],
        "img_keys": ["media", 0, "media_url_https"],
    }

    def __init__(self):
        tweet = Tweet()

        self.stream = tweet.start_stream(async=True)
        self.root = widgets.RootWidget()
        self.current_tweet = None
        self.next_tweet = None
        self.tweets = tweet.get_tweets(count=7)
        self.index = 0

        self.stream.add_watcher(self.on_update)

    def setup(self):
        try:
            tweets = self.tweets[:2]
        except IndexError:
            tweets = self.tweets

        [self.build_tweet() for _ in tweets]

        if len(self.tweets) > 1:
            Clock.schedule_interval(lambda dt: self.animate(), 10)

        return self.root

    def build_tweet(self, y_offset=-2000):
        if len(self.root.children) < 1:
            y_offset = 0

        tweet = self.tweets[self.index]
        box = widgets.BoxWidget(pos=(0, y_offset))
        label = widgets.LabelWidget(text=tweet["text"])
        box.add_widget(label)

        self.get_media(tweet, box)
        self.root.add_widget(box)
        self.set_current_next(box)
        self.index = self.index + 1

        return box

    def set_current_next(self, next_tweet):
        self.current_tweet = self.next_tweet
        self.next_tweet = next_tweet

    def get_media(self, tweet, box):
        tweet_ee = tweet.get("extended_entities")

        if tweet_ee is None:
            return

        widget = self.get_media_widget(tweet_ee)

        if widget is not None:
            box.add_widget(widget)

    def get_media_widget(self, tweet):
        for type_keys in self.KEYS:
            try:
                src = reduce(lambda d, k: d[k], self.KEYS[type_keys], tweet)
                key = type_keys
                break
            except (KeyError, IndexError):
                src = None

        if src is None:
            return src

        if not key.lower().startswith("img"):
            widget = widgets.VideoWidget(source=src)
        else:
            widget = widgets.ImageWidget(source=src)

        return widget

    def on_update(self, status):
        if status.get("text"):
            self.tweets.insert(0, status)
            self.index = self.index + 1
        elif status.get("delete"):
            self.on_delete(status)

    def on_delete(self, status):
        for tweet in self.tweets:
            if tweet["id"] == status["delete"]["status"]["id"]:
                self.tweets.remove(tweet)
                self.index = self.index - 1
                break

    def animate(self):
        if self.next_tweet.children[0].__class__.__name__ == "VideoWidget":
            self.next_tweet.children[0].state = "play"

        anim_current = Animation(x=-2000, y=0, d=1, t="in_cubic")
        anim_next = Animation(y=0, d=1, t="out_cubic")

        anim_current.start(self.current_tweet)
        anim_next.start(self.next_tweet)

        anim_current.bind(on_complete=self.loop)

    def loop(self, *args):
        self.root.remove_widget(self.current_tweet)

        if self.index >= len(self.tweets):
            self.index = 0

        self.build_tweet()
