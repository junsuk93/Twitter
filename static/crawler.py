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
    city = ''
    cnt = 0

    @staticmethod
    def set_city(city):
        Listener.city = city

    def on_status(self, status):
        Listener.cnt += 1
        print(Listener.cnt, " : ", status.text)
        if status.truncated:
            txt = status.extended_tweet['full_text']
        else:
            txt = status.text
        print(status.place.bounding_box.coordinates)
        # geo = status.place
        # city = status.place['full_name']
        # post = {'text': txt, 'city':city, 'geo':geo }
        # collection.insert(post)

    def on_error(self, status_code):
        print(Listener.city, " ", sys.stderr, "Encountered error with status code:", status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, "Timeout")
        return True


def sentiment(data, city):
    twit_json = json.loads(data)
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(twit_json['text'])
    print(city, " : ", twit_json['text'], '\n', ss)


# def listener(index):
#     city = location_list[index][0]
#     coordinate = location_list[index][1]
#     Listener.set_city(city)
#     ct = tweepy.streaming.Stream(auth, Listener())
#     ct.filter(locations=coordinate)


if __name__ == '__main__':
    ct = tweepy.streaming.Stream(auth, Listener())
    ct.filter(locations=[-123.915252, 31.991705, -67.665251, 49.068417])
    # pool = Pool(processes=5)
    # pool.map(listener, range(0, 6))
