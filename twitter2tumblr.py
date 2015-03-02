#!/usr/bin/env python3
import re
import sys
from os import path
import requests
from twython import Twython
from tumblpy import Tumblpy

BLOG_URL = 'sakuramochimochi.tumblr.com'

## fetch a tweet

# check arguments
if len(sys.argv) == 1:
    sys.exit('Usage: {} (tweet_url|tweet_id)+'.format(sys.argv[0]))

# parse ids
ids = []
for arg in sys.argv[1:]:
    # tweet_id
    match = re.search(r'^(\d+)$', arg)
    if match:
        id = match.group(1)
        ids.append(id)
    # tweet_url
    match = re.search(r'twitter.com/.+/status/(\d+)', arg)
    if match:
        id = match.group(1)
        ids.append(id)    

# in case there is no id
if not ids:
    sys.exit('Cannot find any tweet ids in args: ' + ' '.join(sys.argv[1:]))

# prepare api
with open('.credentials') as f:
    api, api_secret, token, token_secret = f.read().strip().split()
t = Twython(api, api_secret, token, token_secret)

# get the tweet
tw = t.show_status(id=id)

# rebuild the tweet url
tweet_url = 'https://twitter.com/{screen_name}/status/{id}'.format(screen_name=tw['user']['screen_name'], id=tw['id'])

# download images
imgs = []
img_urls = [media['media_url'] + ':orig' for media in tw['extended_entities']['media']]
for img_url in img_urls:
    r = requests.get(img_url)
    img = 'img/' + path.basename(img_url.replace(':orig', ''))
    with open(img, 'wb') as f:
        f.write(r.content)
        print('Downloaded:', img_url)
    imgs.append(img)

## post to tumblr

# prepare api
with open('.credentials_tumblr') as f:
    api, api_secret, token, token_secret = f.read().strip().split()
t = Tumblpy(api, api_secret, token, token_secret)

# ask caption
caption = input('Caption: ')
tags = input('Tags(comma-separated): ')

# make paramaters
params = {
    'type': 'photo',
    'caption': caption,
    'tags': tags,
    'source_url': tweet_url,
}
    
# attach images
for i, img in enumerate(imgs, 1):
    params['data[{}]'.format(i)] = open(img, 'rb')
    
# post to tumblr
post = t.post('post', blog_url=BLOG_URL, params=params)
print('Post to Tumblr:', '{blog_url}/post/{id}'.format(blog_url=BLOG_URL, id=post['id']))
