#!/usr/bin/python
## Twitter api implementation using oauth2
## Hitesh Agrawal
import oauth2 as oauth
import json
import sys
import config
import urllib
"""
1) Install python oauth2 module
#sudo pip install oauth2
2) Get your consumer/access key and secret from https://apps.twitter.com/
3) Put your consumer/access key and secret in config.py
4) Check output in twitter-response.log, which i have saved for a test run
"""

#Setting output encoding to utf8, for displaying tweets with unicode characters on console
reload(sys)
sys.setdefaultencoding('utf-8')

## Defining a twitter class 
class Twitter():
	def __init__(self,consumerkey,consumersecret,accesskey,accesssecret):
		access_token = oauth.Token(key=accesskey, secret=accesssecret)
		consumer = oauth.Consumer(key=consumerkey, secret=consumersecret)
		self.my_tweets = 0  ## This will avoid repeatable calls to the twitter api
		self.connect = oauth.Client(consumer, access_token)
		## We need to check whether the oauth credentials were successful or not
		## https://dev.twitter.com/rest/reference/get/account/verify_credentials
		credential_endpoint = "https://api.twitter.com/1.1/account/verify_credentials.json"
		response, data = self.connect.request(credential_endpoint)
		# response is <class 'httplib2.Response'>
		#print response['status']
		#print type(response['status'])
		if int(response['status']) != 200: ## Means our oauth authentication failed , we should not even create the object
			print "You oauth tokens are not correct, please recheck"
			raise Exception()
		else:
			# While data is a str  dict, lets convert it to json below 
			data = json.loads(data)
			## Now get the screen_name	
			self.screenname = data["screen_name"]
			print "My screenname is :", self.screenname

	def mytweets(self,show=0,force=0):
		## Twitter api link to get our tweets
		### "https://api.twitter.com/1.1/statuses/user_timeline.json?"
		#force  ## To reload the twitter feed after you add or remove tweets
		endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
		encode_message =  urllib.urlencode({'screen_name':self.screenname})
		final_endpoint = endpoint + encode_message
  		if self.my_tweets == 0 or force == 1:	
			self.mytweets_response, mytweets_data = self.connect.request(final_endpoint,'GET')
			self.my_tweets = json.loads(mytweets_data)
		if show == 1:
			print "\n@%s Twitter Feed:" %(self.screenname)
			for tweet in self.my_tweets:
				print "Tweet is: %s" %(tweet['text'])
			print "The available number of calls left:", self.mytweets_response['x-rate-limit-remaining']	
		return self.mytweets_response, self.my_tweets	

	def findtweet(self,findstring,delete=0):
		## You first need to call the mytweets method, if twitter feed is not already cached
		#self.mytweets()
		if self.my_tweets == 0:
		## Call the mytweets method
			self.mytweets()
		for tweet_find in self.my_tweets:
			if tweet_find['text'].lower().find(findstring.lower()) != -1:
				print "\nFound the tweet containing text: %s" %(findstring)
				#print "The tweet id is : %s" %(self.tweet_find['id'])
				print "The tweet text is : %s" %(tweet_find['text'])
				if delete == 1:
					## https://api.twitter.com/1.1/statuses/destroy/:id.json
					print "Deleting tweet: %s" %(tweet_find['text'])
					tweet_id =  tweet_find['id']
					destroy_endpoint = "https://api.twitter.com/1.1/statuses/destroy/"
					final_destroy_endpoint = destroy_endpoint + str(tweet_id) + ".json"
					#print self.final_destroy_endpoint
					delete_response, delete_data = self.connect.request(final_destroy_endpoint,'POST')
					#print delete_response
					#print delete_data	

	def post(self,message):
		## Truncate incoming messages to 140 character
		if len(message) > 140:
			print "Truncating message to 140 characters"
			message = message[:140]
		post_endpoint = "https://api.twitter.com/1.1/statuses/update.json"
		encode_message =  urllib.urlencode({'status':message})
		## Now actual posting to twitter
		print "\nPosting your tweet: %s" %(message)
		post_response, post_data = self.connect.request(post_endpoint,'POST', encode_message)
		#print self.post_data
		#{"errors":[{"code":187,"message":"Status is a duplicate."}]}
		#print type(self.post_data)
		if post_data.find('errors') != -1:
			print "Error in posting your tweet,below is the error"
			print post_data
		else:
			print "Successfully posted your tweet: %s" %(message)	
			#Now update the twitter feed, which will include your new post too
			self.mytweets(force=1)
		#	print "Error in posting , as :%s" %(self.post_data['errors'][0]['message'])
				
	def deletetweet(self,findstring):
		# Call the find tweet method , with delete=1 optional parameter
		print "\nTrying to find the tweet containing text: %s" %(findstring)
		self.findtweet(findstring,delete=1)
		## Now update the tweet feed, calling the mytweets method
		self.mytweets(force=1)

	def othertweet(self,screenname):
		pass	

if __name__ == '__main__':
	#Create a Twitter object for user hitesh , get config details from config.py
	hitesh = Twitter(config.CONSUMER_KEY,config.CONSUMER_SECRET,config.ACCESS_KEY,config.ACCESS_SECRET)
	hitesh.mytweets(show=1)	## To show your twitter feed
	message = "This is a new tweet containing keyword Python"
	message2 = "This is a new tweet containing keyword python2"
	hitesh.post(message)
	hitesh.post(message2)
	hitesh.deletetweet("python") ## to delete tweet containing string python
	#hitesh.deletetweet("milking")
	hitesh.mytweets(show=1)	


CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'

naresh = Twitter(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
naresh.mytweets(show=1)
naresh.post("This is posting as naresh")
naresh.mytweets(show=1)
naresh.deletetweet("tweet")
hitesh.mytweets(show=1)	

