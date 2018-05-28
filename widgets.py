from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.video import Video
from kivy.uix.label import Label


class LabelWidget(Label):
    pass


class ImageWidget(AsyncImage):
    pass


class VideoWidget(Video):
    pass


class RootWidget(FloatLayout):
    pass


class BoxWidget(BoxLayout):
    pass
