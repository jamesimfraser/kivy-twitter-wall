An experiment with kivy to display a twitter feed in python

### Setup

* Run `pip install -r requirements.txt`
* Follow instructions at the [kivy website](https://kivy.org/docs/installation/installation.html) for dependencies not covered by pip
* Create a new twitter app [here](|https://apps.twitter.com/)
* Add a .env file to the project root directory with the following parameters:
  `TWITTER_CONSUMER_KEY={{ your consumer key }} 
TWITTER_CONSUMER_SECRET={{ your consumer secret }}  
TWITTER_ACCESS_TOKEN={{ your access token }}  
TWITTER_ACCESS_TOKEN_SECRET={{ your access token secret }}
TWITTER_SCREEN_NAME={{ username of feed to display }}`
* Run `python app.py` 