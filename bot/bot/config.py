from __future__ import unicode_literals

import tweepy
import os
import random

import tweepy
from tweepy import OAuthHandler
from dotenv import load_dotenv
load_dotenv()


VALID_STATUS_CODES = set(range(200, 300)) | {429}
RETRY_WITH_GET_STATUS_CODES = set(range(400, 500))
REQUEST_HEADERS = {'User-agent': 'biolinkchecker 0.0.1dev'}

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite://")


FAKE_FOLLOWERS_IDS = os.getenv('FAKE_FOLLOWERS_IDS')

def check_config():
    assert TWITTER_CONSUMER_KEY, "TWITTER_CONSUMER_KEY not set"
    assert TWITTER_CONSUMER_SECRET, "TWITTER_CONSUMER_SECRET not set"
    assert TWITTER_ACCESS_TOKEN, "TWITTER_ACCESS_TOKEN not set"
    assert TWITTER_ACCESS_SECRET, "TWITTER_ACCESS_SECRET not set"
    assert SQLALCHEMY_DATABASE_URI, "SQLALCHEMY_DATABASE_URI not set"


def get_api():
    auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

    return tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class FakeFollower(object):
    def __init__(self, id, urls=None) -> None:
        super().__init__()
        self.id = id
        self.id_str = str(id)
        self.entities = {'url':{'urls':[]}, 'description':{'urls':[]}}
        if urls:
            for url in urls:
                if random.random() > 0.5:
                    lst = self.entities['url']['urls']
                else:
                    lst = self.entities['description']['urls']
                lst.append({'url': url, 'expanded_url': url, 'display_url': url, 'indices': url})



def get_fake_followers():
    followers = []
    if FAKE_FOLLOWERS_IDS:
        ffids = FAKE_FOLLOWERS_IDS.strip().split(',')
        ffids = [fid.strip() for fid in ffids if fid.strip()]
        urls = ["https://abcdefghijklmnopqrstuvw.xyz/does/not/exists", "https://example.com"]
        followers = [FakeFollower(fid, urls) for fid in ffids]
    return followers
