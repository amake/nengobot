import tweepy
import json
import os

creds_file = 'credentials.json'

credentials = {}

if os.path.isfile(creds_file):
    with open(creds_file) as infile:
        credentials = json.load(infile)
else:
    print('Credentials not found. Run auth_setup.py first.')
    exit(1)

auth = tweepy.OAuthHandler(credentials['ConsumerKey'],
                           credentials['ConsumerSecret'])
auth.set_access_token(credentials['AccessToken'],
                      credentials['AccessSecret'])

api = tweepy.API(auth)


def iter_tweets():
    for status in tweepy.Cursor(api.user_timeline).items():
        yield status


def dump_tweets_digest():
    for tweet in iter_tweets():
        print(f'{int(tweet.created_at.timestamp())} {tweet.text}')


if __name__ == '__main__':
    try:
        dump_tweets_digest()
    except KeyboardInterrupt:
        pass
