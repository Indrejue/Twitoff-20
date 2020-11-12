"""Importing and retriving tweets and puttin into a DB"""

from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

API_KEY = getenv("API_KEY")
SECRET = getenv("SECRET")
TWITTER_AUTH = tweepy.OAuthHandler(API_KEY, SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)


nlp = spacy.load('my_model')


def vec_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_user(username):
    try:
        t_user = TWITTER.get_user(username)
        db_user = (User.query.get(t_user.id)) or User(
            id=t_user.id, name=username)
        DB.session.add(db_user)
        tweets = t_user.timeline(
            count=500, exclude_replies=True, include_rts=False,
            tweet_mode="extended", since_id=db_user.new_t_id
        )

        if tweets:
            db_user.new_t_id = tweets[0].id

        for tweet in tweets:
            v_tweet = vec_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text,
                             vect=v_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print('Error processing{}: {}'.format(username, e))
        raise e

    else:
        DB.session.commit()


def update_all_users():
    """Update all Tweets for all Users in the User table."""
    for user in User.query.all():
        add_user(user.name)
