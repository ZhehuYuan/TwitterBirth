from itertools import islice
import json
from http.client import BadStatusLine
from urllib.error import URLError
import time
import sys
from sys import maxsize as maxint
from functools import partial
import twitter
import networkx as nx
import matplotlib.pyplot as pltscr

#let us get some data

screen_name = "etaglic"
#screen_name = "notdarron"

def oauth_login():

    APP = 'Mario'
    CONSUMER_KEY = 'MFgug6whPGqaf98DvZqbnD4JW'
    CONSUMER_SECRET = 'N4elfLvuJ8SkcUyRkf9uRvLvxlRfIMf9GWNJJHEePJDNPcnrSR'


    oauth_token, oauth_sec = twitter.oauth_dance(
        APP, CONSUMER_KEY, CONSUMER_SECRET)

    auth = twitter.oauth.OAuth(oauth_token, oauth_sec,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)

    return twitter_api


twitter_api = oauth_login()


def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):

    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600:  # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e

        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes

        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized) aka YOU ARE F**KED', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found) aka YOU ARE F**KED', file=sys.stderr)
            return None
        elif e.e.code == 429:
            print('Encountered 429 Error (Rate Limit Exceeded)... aka YOU ARE F**KED', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ... aka YOU ARE F**KED!!", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again aka YOU ARE F**KED!!', file=sys.stderr)
                return 2
            else:
                raise e  # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'                  .format(
                e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing. oh yea we cooking now", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out. how does this happen?", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing. Bad What? Must be on StackOverflow", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out. Stop dumping these problems I got other work to do", file=sys.stderr)
                raise


def get_friends_followers_ids(twitter_api, screen_name=None,
                              friends_limit=maxint, followers_limit=maxint):


    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids,
                              count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids,
                                count=5000)


    friends_ids, followers_ids = [], []

    for twitter_api_func, limit, ids, label in [
        [get_friends_ids, friends_limit, friends_ids, "friends"],
        [get_followers_ids, followers_limit, followers_ids, "followers"]
    ]:

        if limit == 0:
            continue

        cursor = -1
        while cursor != 0:
            if screen_name:
                response = twitter_api_func(
                    screen_name=screen_name, cursor=cursor)
            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
            print('Fetched {0} total {1} ids for {2}'.format(
                len(ids),                  label, (screen_name)), file=sys.stderr)


            if len(ids) >= limit or response is None:
                break
    return friends_ids[:friends_limit], followers_ids[:followers_limit]


def get_user_profile(twitter_api, user_ids=None):

    items_to_info = {}

    items = user_ids

    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See http://bit.ly/2Gcjfzr for details.

        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if user_ids:  # user_ids
            response = make_twitter_request(twitter_api.users.lookup,
                                            user_id=items_str)

        for user_info in response:
            if user_ids:  # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info





#core code
x = get_friends_followers_ids(twitter_api, screen_name)
profiles = get_user_profile(twitter_api, user_ids=x[1])
for k, v in profiles.items():
    x = v.get("screen_name")
    y = v.get ("name")
    z = v.get("description")
    print("Screen Name: " + str(x) + "\n" +  "Name: " + str(y) + " \n" + "Bio: " + str(z))
