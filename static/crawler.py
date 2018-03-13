import json
import sys
import tweepy
from nltk.sentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient

consumer_key = 'cMlGmUqVEl0LHsURqmg3KFJ06'
consumer_secret = 'pY5AFjmpSt9u511H8Pg6n7bh0njFxIaSzxONwXqqXtzmJGBXQv'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
access_token = "954173457851273216-4o9v5zh8yeEeRTXOGI9kcPv24fUQ7rz"
access_token_secret = "3Lre0L0kppXvuZ9tvLco4z0eN6GoJHNkpeqHt0EFOH4Kx"
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
client = MongoClient()
db = client['tw_db']
collection = db.tweet


class Listener(tweepy.StreamListener):

    def on_status(self, status):
        txt = ''
        try:
            txt = status.extended_tweet['full_text']
        except:
            txt = status.text

        if 'music' in txt or 'song' in txt or 'sing' in txt or 'concert' in txt or 'sound' in txt or 'pop' in txt or 'audio' in txt or 'album' in txt:
            city = status.place.name
            coordinates = status.place.bounding_box.coordinates
            created_at = status.created_at

            print(txt, " ", city, " ", coordinates, " ", created_at)

    def on_error(self, status_code):
        print(sys.stderr, "Encountered error with status code:", status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, "Timeout")
        return True


def sentiment(data, city):
    twit_json = json.loads(data)
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(twit_json['text'])
    print(city, " : ", twit_json['text'], '\n', ss)


if __name__ == '__main__':
    ct = tweepy.streaming.Stream(auth, Listener())
    ct.filter(locations=[-123.915252, 31.991705, -67.665251, 49.068417])

