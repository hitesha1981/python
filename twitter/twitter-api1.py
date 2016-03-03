#!/usr/bin/python
## Twitter api implementation using oauth2
import oauth2 as oauth
import json
import sys
import config
import urllib


#Setting output encoding to utf8
reload(sys)
sys.setdefaultencoding('utf-8')

class Twitter():
	def __init__(self,consumerkey,consumersecret,accesskey,accesssecret,screenname='hiteshagrawal81'):
		self.consumerkey = consumerkey
		self.consumersecret = consumersecret
		self.accesskey = accesskey
		self.accesssecret = accesssecret
		self.consumer = oauth.Consumer(key=self.consumerkey, secret=self.consumersecret)
		self.access_token = oauth.Token(key=self.accesskey, secret=self.accesssecret)
		self.screenname = screenname
		self.connect = oauth.Client(self.consumer, self.access_token)
		self.my_tweets = 0  ## This will avoid repeatable calls to the twitter api
		## To get the screen name
		### https://api.twitter.com/1.1/users/show.json
		## endpoint = screen_name
		#self.screenname = self.connect.request()


	def mytweets(self,show=0,force=0):
		## Twitter api link to get our tweets
		### "https://api.twitter.com/1.1/statuses/user_timeline.json?""
		#show = show
		#force = force  ## To reload the twitter feed once you delete a tweet
		endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
		encode_message =  urllib.urlencode({'screen_name':self.screenname})
		final_endpoint = endpoint + encode_message
  		if self.my_tweets == 0 or force == 1:	
			self.mytweets_response, mytweets_data = self.connect.request(final_endpoint,'GET')
			self.my_tweets = json.loads(mytweets_data)
		if show == 1:
			print "\nYour Twitter Feed:"
			for tweet in self.my_tweets:
				print "Tweet is: %s" %(tweet['text'])
			print "The available number of calls left:", self.mytweets_response['x-rate-limit-remaining']	
		return self.mytweets_response, self.my_tweets	

	def findtweet(self,findstring,delete=0):
		#findstring = findstring
		#delete = delete
		## You first need to call the mytweets method
		#self.mytweets()
		if self.my_tweets == 0:
		## Call the mytweets method
			self.mytweets()
		for tweet_find in self.my_tweets:
			if tweet_find['text'].find(findstring.lower()) != -1:
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
		#delete = 0	

	def post(self,message):
		#message = message
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
		# Call the find tweet method , with delete optional parameter
		print "\nTrying to find the tweet containing text: %s" %(findstring)
		self.findtweet(findstring,delete=1)
		## Now update the tweet feed
		self.mytweets(force=1)

if __name__ == '__main__':
	##Create a Twitter object for user hitesh , get config details from config.py
	hitesh = Twitter(config.CONSUMER_KEY,config.CONSUMER_SECRET,config.ACCESS_KEY,config.ACCESS_SECRET,screenname='hiteshagrawal81')
	hitesh.mytweets(show=1)	## To show your twitter feed
	message = "This is a new tweet containing keyword python"
	message2 = "This is a new tweet containing keyword python2"
	hitesh.post(message)
	hitesh.post(message2)
	#hitesh.deletetweet("python") ## to delete tweet containing string python
	hitesh.deletetweet("milking")
	hitesh.mytweets(show=1)	




