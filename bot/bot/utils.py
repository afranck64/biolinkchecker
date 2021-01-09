from __future__ import unicode_literals
import datetime

import time
import requests
from sqlalchemy import func
import tweepy
import os
from typing import List, Generator, Iterable

import tweepy
from tweepy import OAuthHandler
from tweepy.models import User

from dotenv import load_dotenv
import joblib
load_dotenv()
from .config import LINKS_TTL, REQUEST_HEADERS, RETRY_WITH_GET_STATUS_CODES, VALID_STATUS_CODES, get_api
from .models import Account, Link, get_session



def limit_handled(cursor: tweepy.Cursor) -> Generator[tweepy.User, None, None]:
    while True:
        try:
            item: tweepy.User = next(cursor)
            yield item
        except StopIteration:
            return
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

def get_followers_generator(screen_name:str=None) -> Generator[tweepy.User, None, None]:
    api = get_api()
    for follower in limit_handled(tweepy.Cursor(api.followers, screen_name=screen_name).items()):
        yield follower

def get_followers(screen_name:str=None) -> List[User]:
    followers = list(get_followers_generator(screen_name=screen_name))
    return followers

def _get_user_urls(entities:dict, urls:List[str]=None) -> List[str]:
    if urls is None:
        urls = []
    if 'urls' in entities:
        urls.extend(item['expanded_url'] for item in entities['urls'])

    if entities:
        if 'url' in entities:
            _get_user_urls(entities['url'], urls=urls)
        if 'description' in entities:
            _get_user_urls(entities['description'], urls=urls)
    
    return urls

def get_user_urls(user:tweepy.User) -> List[str]:
    return _get_user_urls(user.entities)


def fetch_accounts_and_links(followers:Iterable[User]):
    session = get_session()
    for user in followers:
        account = session.query(Account).get(user.id)
        if account is None:
            account = Account()
            account.id = user.id
            account.active = True
        elif not account.active:
            continue
        for url in get_user_urls(user):
            link = session.query(Link).get({Link.url.name: url, Link.account_id.name:user.id})
            if link is None:
                link = Link()
            link.url = url
            link.active = True
            link.account_id = user.id
            link.last_set_from_account_on = datetime.datetime.now()
            session.add(link)
        session.add(account)
    session.commit()



def is_url_online(url:str) -> bool:
    timeout_secs=5
    try:
        status_code = requests.head(url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=timeout_secs).status_code
        if status_code in RETRY_WITH_GET_STATUS_CODES:
            status_code = requests.get(url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=timeout_secs).status_code
    except requests.exceptions.MissingSchema:
        url = "http://" + url
        try:
            status_code = requests.head(url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=timeout_secs).status_code
            if status_code in RETRY_WITH_GET_STATUS_CODES:
                status_code = requests.get(url, allow_redirects=True, headers=REQUEST_HEADERS, timeout=timeout_secs).status_code
        except requests.ConnectionError:
            status_code = -1

    except requests.ConnectionError:
        status_code = -1
    return status_code in VALID_STATUS_CODES

def check_links_and_update():
    session = get_session()
    link:Link
    for link in session.query(Link).filter().yield_per(1000):
        now = datetime.datetime.utcnow()
        was_online = link.is_online
        link.is_online = is_url_online(link.url)
        link.last_checked_on = now
        if was_online != link.is_online:
            link.online_status_changed = True
        if link.is_online:
            link.last_online_on = now
        session.add(link)
    session.commit()


def send_offline_links_notifications_single():
    session = get_session()
    api = get_api()
    link:Link
    for link in session.query(Link).filter(Link.is_online==False, Link.online_status_changed==True):
        text = f"""
        Hello, the following link on your bio seems to be offline:
        {link.url}
        Best regards"""
        api.send_direct_message(link.account_id, text)
        link.online_status_changed = False
        session.add(link)
    session.commit()

def send_offline_links_notifications():
    """
    Gather all links down for a given user and send them per Direct message.
    """
    session = get_session()
    api = get_api()
    res = session.query(
        Link.account_id,
        func.group_concat(Link.url, "\n"),
    ).filter(Link.is_online==False, Link.online_status_changed==True).group_by(Link.account_id).yield_per(100)
    for account_id, account_offline_urls in res:
        message = f"""Hello, the following link(s) on your bio seem(s) to be offline:\n{account_offline_urls}\nBest regards"""
        api.send_direct_message(account_id, message)
        session.query(Link).filter(Link.account_id==account_id).update(
            {Link.online_status_changed.name:False},
            synchronize_session=False
        )
    session.commit()

def prune_orphan_links(orphan_delay=LINKS_TTL):
    session = get_session()
    threshold = datetime.datetime.now() - datetime.timedelta(seconds=LINKS_TTL)
    session.query(Link).filter(Link.last_set_from_account_on<=threshold).delete()
    session.commit()