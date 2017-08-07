#!/anaconda/bin/python2.7 -tt

import tweepy
from tweepy import OAuthHandler
from emailreminder import emailReminder
from textreminder import textReminder

#use the Twitter API to get these
access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

def get_200_most_recent_tweets(screen_name):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    tweets = []
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    tweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    return tweets

if __name__ == '__main__':
    #log of tweet-IDs to prevent duplicate alerts
    with open('[path/gameTweetIDs-1]', 'r') as f:
        read_data = set(f.read().splitlines())
    weets = get_all_tweets('videogamedeals')
    # your search terms here, either individual terms or a list of terms
    search_terms = []
    #log of tweet-IDs to prevent duplicate alerts (same log as above)
    f2 = open('[path/gameTweetIDs-1]', 'a')
    allReminders = []
    for term in search_terms:
        if type(term) == list:
            results = tweets[:]
            for subterm in term:
                results = filter(lambda x: subterm in x.text.lower(), results)
            results = [(x.text, x.id) for x in results]
        else:
            results = [(x.text, x.id) for x in alltweets if term in x.text.lower()]
        for result in results:
            if str(result[1]) not in read_data:
                message = str(result[0].encode('utf-8'))
                textReminder(message)
                emailReminder(message)
                print message
                f2.write(str(result[1]) + "\n")
    f2.close()


