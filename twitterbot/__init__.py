#!/usr/bin/env python2

# Add your keys here. Use access key generation script to get access permissions on account.
CONSUMER_KEY    = ' '
CONSUMER_SECRET = ' '
ACCESS_KEY      = ' '
ACCESS_SECRET   = ' '


import tweepy

class Twitter():
    """ to manage twitter related activities """

    def __init__(self):
        # OAuth authentication
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def tweet(self, text):
        ''' tweet text'''
        self.api.update_status(text)

if __name__ == "__main__":
    instance=Twitter()
    instance.tweet("testing again")
