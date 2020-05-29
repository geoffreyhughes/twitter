# sentiment.py
# Demonstrates connecting to the twitter API and doing sentiment analysis on 2 key words, then comparing the results
# Author: Geoffrey Hughes
# Email: ghughes@chapman.edu
# Professor: Dr. Michael Fahy
# Course: CPSC 353
# Assignment: PA02 Sentiment Analysis
# Version 1.0
# Date: October 6, 2019

import twitter
import json
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Using hughes_geoffrey twitter API keys
CONSUMER_KEY = 'z3KW52H8TSmHllGEcrynwVKhE'
CONSUMER_SECRET = 'XLUcSuK1TxVYEU5OpgEToqvGaPUkXvllmwmtICCaGaaDwmS5CT'
OAUTH_TOKEN = '429588869-qwlHYYTc1XgGJH52t0myG9FaTngJK0TRWaThFzxY'
OAUTH_TOKEN_SECRET = 'aIZ2BFbMoaFyXcS8rv5ICMHVocKpYuF4k51GksFy2qNj6'

# Authenitcate twitter API request with hughes_geoffrey keys
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

# Set twitter API with authentication
twitter_api = twitter.Twitter(auth=auth)

# XXX: Set these 2 variables to a trending topic,
# or anything else for that matter
q = input('Enter a search term: ')
q2 = input('Enter another search term: ')

# Print the two input variables for the user
print(q)
print(q2)

# Set count as number of tweets to search relating to the words
count = 1000

# See https://dev.twitter.com/docs/api/1.1/get/search/tweets
search_results = twitter_api.search.tweets(q=q, count=count)
search_results2 = twitter_api.search.tweets(q=q2, count=count)

# Get search result statuses and store them
statuses = search_results['statuses']
statuses2 = search_results2['statuses']

# Iterate through 5 more batches of results by following the cursor for word 1
for _ in range(5):
    try:
        next_results = search_results['search_metadata']['next_results']
    # except KeyError, e:  # No more results when next_results doesn't exist
    except KeyError:
        break

    # Create a dictionary from next_results
    kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

# Iterate through 5 more batches of results by following the cursor for word 2
for _ in range(5):
    try:
        next_results2 = search_results2['search_metadata']['next_results']
    # except KeyError, e:  # No more results when next_results2 doesn't exist
    except KeyError:
        break

    # Create a dictionary from next_results2
    kwargs2 = dict([kv.split('=') for kv in next_results2[1:].split("&")])

    search_results2 = twitter_api.search.tweets(**kwargs2)
    statuses2 += search_results2['statuses']

# Store the statuses' text for word 1
status_texts = [status['text']
                for status in statuses]

# Store the statuses' text for word 2
status_texts2 = [status['text']
                for status in statuses2]

# Compute a collection of all words from all tweets with word 1
words = [w
         for t in status_texts
         for w in t.split()]

# Compute a collection of all words from all tweets with word 2
words2 = [w2
         for t in status_texts2
         for w2 in t.split()]

# SENTIMENT ANALYSIS FOR WORD 1
print("---------------------------------------------------------------------")
print('Sentiment Analysis on word 1, ', q, ': ')
sent_file = open('AFINN-111.txt')

scores = {}  # initialize an empty dictionary
for line in sent_file:
    term, score = line.split("\t")
    # The file is tab-delimited.
    # "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

score = 0
for word in words:
    uword = word.encode('utf-8')
    if word in scores.keys():
        score = score + scores[word]
print(float(score))

# SENTIMENT ANALYSIS FOR WORD 2
print("---------------------------------------------------------------------")
print('Sentiment Analysis on word 2, ', q2, ': ')
sent_file = open('AFINN-111.txt')

scores2 = {}  # initialize an empty dictionary
for line in sent_file:
    term2, score2 = line.split("\t")
    # The file is tab-delimited.
    # "\t" means "tab character"
    scores2[term2] = int(score2)  # Convert the score to an integer.

score2 = 0
for word in words2:
    uword = word.encode('utf-8')
    if word in scores2.keys():
        score2 = score2 + scores2[word]
print(float(score2))

# Determine which term has a better sentiment score
print("---------------------------------------------------------------------")
if (score > score2):
    print(q, " has a better sentiment score than ", q2)

elif (score < score2):
    print(q2, " has a better sentiment score than ", q)

else:
    print(q, " and ", q2, " have equal sentiment scores")
print("---------------------------------------------------------------------")
