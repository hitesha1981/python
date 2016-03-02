#!/usr/bin/python
### Interacting with twitter , without using twitter module
#### Author: Hitesh Agrawal
import oauth2 as oauth
import json
import sys
import config
import urllib
"""
https://apps.twitter.com/app/12035694/keys
sudo pip install oauth2
We get the authentication keys from config.py , hence config.py above
"""

# Put following in config.py
# CONSUMER_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
# CONSUMER_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXX"
# ACCESS_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
# ACCESS_SECRET = "XXXXXXXXXXXXXXXXXXXXXXXXX"

#Setting output encoding to utf8
reload(sys)
sys.setdefaultencoding('utf-8')

### setup a secure connection to twitter using oauth2
consumer = oauth.Consumer(key=config.CONSUMER_KEY, secret=config.CONSUMER_SECRET)
access_token = oauth.Token(key=config.ACCESS_KEY, secret=config.ACCESS_SECRET)
client = oauth.Client(consumer, access_token)

### Check the tweets on our timeline , we used encoding to utf-8 , so that we can print the tweets on console.
timeline_endpoint = "https://api.twitter.com/1.1/statuses/home_timeline.json"
response, data = client.request(timeline_endpoint,method='GET')

## Load the tweets in json format
tweets = json.loads(data)
#print json.dumps(tweets, indent=4)
#print tweets
### write the data and header response to a local file , so that we can use that later on
# with open('/Users/hitesha/twitter/data.json','w') as data_json:
# 	data_json.write(json.dumps(tweets, indent=4))
# #Write the header response to a local file
# with open('/Users/hitesha/twitter/response.json','w') as response_json:
# 	response_json.write(json.dumps(response, indent=4))

# Now print the tweets.
count = 0
for tweet in tweets:
	count += 1
	print "%d tweet is :%s" %(count,tweet['text'])

## Response contains the header and the rate-limit remaining
print "The available number of calls left", response['x-rate-limit-remaining']	

## Now to post a status message
post_endpoint = "https://api.twitter.com/1.1/statuses/update.json"
message = "Hi, how r u, this is using python"
encode_message =  urllib.urlencode({'status':message})
## Now actual posting to twitter
response, data = client.request(post_endpoint,'POST', encode_message)

# print "Printing header"
# print json.dumps(response, indent=4)

# print "Printing update data"
# update = json.loads(data)
# print json.dumps(update,indent=4)

