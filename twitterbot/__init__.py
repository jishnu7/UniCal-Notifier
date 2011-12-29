#!/usr/bin/env python

import tweepy
from keys import *

class Twitter():
    """ to manage twitter related activities """

    def __init__(self, account):
        # OAuth authentication
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY[account], ACCESS_SECRET[account])
        self.api = tweepy.API(auth)

    def tweet(self, text):
        ''' tweet text'''
        self.api.update_status(text)

if __name__ == "__main__":
    ''' Incase this main thread, send a test tweet '''
    instance=Twitter()
    instance.tweet("testing !!")
