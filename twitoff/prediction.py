"""Prediction of user models"""

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from .models import User
from .twitter import vec_tweet


def predict_user(user0_name, user1_name, hypo_tweet):
    """
    Determin which user is more likely to say a tweet.
    returns either a 0 for user0 or 1 for user1.
    """

    user0 = User.query.filter(User.name == user0_name).one()
    user1 = User.query.filter(User.name == user1_name).one()
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])
    vects = np.vstack([user0_vects, user1_vects])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])
    hypo_tweet = vec_tweet(hypo_tweet)

    gb_reg = GradientBoostingClassifier().fit(vects, labels)

    return gb_reg.predict(hypo_tweet.reshape(1, -1))
