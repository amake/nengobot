from __future__ import print_function
import os
import io
import tweepy
import json
import nengo
import announce

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


def do_tweet(event, context):
    ng, reading = nengo.generate()
    status = u'%s（%s）' % (ng, reading)
    imagefile = io.BytesIO()
    announce_img = announce.generate(*ng)
    announce_img.save(imagefile, format='png')
    api.update_with_media('announce.png', status=status, file=imagefile)
    return ng, reading
