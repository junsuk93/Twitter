import sys
import tweepy
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk

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
        try:
            txt = status.extended_tweet['full_text']
        except:
            txt = status.text
        if 'https' in txt:
            res = txt.split('https')
            txt = res[0]

        if status.lang == 'en':
            try:
               city = status.place.name
               coordinate = status.place.bounding_box.coordinates[0][0]
               created_at = status.created_at
               sentiment_val = sentiment(txt)
               namedentity = nechunker(txt)
               post = {"text":txt.lower(), "city":city, "coordinate":coordinate, "created_at":created_at, "sentiment":sentiment_val, "NE":namedentity}
               collection.insert(post)
            except:
                print("DB Error")
                return True

    def on_error(self, status_code):
        print(sys.stderr, "Encountered error with status code:", status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, "Timeout")
        return True


def sentiment(text):
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)
    return ss


def nechunker(text):
    tokenized_sentence = nltk.word_tokenize(text)
    tagged_sentence = nltk.pos_tag(tokenized_sentence)
    chunked_sentence = nltk.ne_chunk(tagged_sentence, binary = True)
    result = []

    for t in chunked_sentence.subtrees():
        neword = ""
        if t.label() == 'NE':
            for word in t:
                neword += word[0]
            result.append(neword.lower())

    return result

if __name__ == '__main__':
    ct = tweepy.streaming.Stream(auth, Listener())
    ct.filter(locations=[-123.915252, 31.991705, -67.665251, 49.068417])
