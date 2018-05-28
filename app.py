import logging
import settings

from kivy.app import App
from kivy.core.window import Window

from controller import TweetController

class TweetApp(App):
    def __init__(self, **kwargs):
        super(TweetApp, self).__init__(**kwargs)
        self.controller = TweetController()

    def build(self):
        Window.clearcolor = (1, .75, .25, 1)
        return self.controller.setup()

    def on_stop(self):
        logging.info("App: Closing twitter stream")
        self.controller.stream.disconnect()

if __name__ == "__main__":
    TweetApp().run()
