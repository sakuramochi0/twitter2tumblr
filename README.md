# twitter2tumblr
Simple command line tool to post images of specified tweets to Tumblr with caption, tags, and source_url.

## Requirement
You have to prepare your OAuth keys and secrets of
[twitter](https://apps.twitter.com/) and [tumblr](https://www.tumblr.com/oauth/apps).
And then, you have to write them in `.credentials`(for twitter API) and `.credentials-tumblr`(for tumblr API).
These .credentials should have 4 lines: `consumer_key`, `consumer_secret`, `token`, and `token_secret`.

Do not forget to edit `BLOG_URL` in `twitter2tumblr.py` to yours.

## Usage
    twitter2tumblr (tweet_url|tweet_id)+

where

    tweet_url == [https?://]twitter.com/{screen_name}/status/{tweet_id}
    tweet_id == \d+

