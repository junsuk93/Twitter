import sys
import tweepy
import json
consumer_key ='cMlGmUqVEl0LHsURqmg3KFJ06'
consumer_secret = 'pY5AFjmpSt9u511H8Pg6n7bh0njFxIaSzxONwXqqXtzmJGBXQv'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
access_token = "954173457851273216-4o9v5zh8yeEeRTXOGI9kcPv24fUQ7rz"
access_token_secret = "3Lre0L0kppXvuZ9tvLco4z0eN6GoJHNkpeqHt0EFOH4Kx"
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)dssdfsd


class Listener(tweepy.StreamListener):
    cnt = 0

    def on_status(self, status):
        Listener.cnt += 1
        if(status.truncated == True):
            print(status.extended_tweet)
        print(Listener.cnt,  " : ", status)

    def on_error(self, status_code):
        print(sys.stderr, "Encountered error with status code:", status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, "Timeout")
        return True


sapi = tweepy.streaming.Stream(auth, Listener())
sapi.filter(track=["korean restaurant", "korean food"])
sapi.filter(locations=[-126.430036, 26.254652, -66.562787, 49.158560])
sapi.filter(languages=['en'])

