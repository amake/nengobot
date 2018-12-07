from __future__ import print_function
import os
import io
import tweepy
import json
import nengo
import announce
import random

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


def tiny_chance():
    return random.random() < 0.01


def get_announce_emoji_img(num):
    import boto3
    s3 = boto3.client('s3')
    emoji_file = io.BytesIO()
    s3.download_fileobj('nengobot', f'160x160/{num}.png', emoji_file)
    return announce.generate_emoji(emoji_file)


def to_png(img):
    buf = io.BytesIO()
    img.save(buf, format='png')
    return buf


def do_tweet(event, context):
    if tiny_chance():
        status = u'???'
        emoji_num = random.randint(1, 2514)
        img = get_announce_emoji_img(emoji_num)
    else:
        ng, reading = nengo.generate()
        status = u'%s（%s）' % (ng, reading)
        img = announce.generate(*ng)
    imagefile = to_png(img)
    result = api.update_with_media(
        'announce.png', status=status, file=imagefile)
    return result
