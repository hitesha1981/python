#!/usr/bin/python
## Twitter api implementation using oauth2
import oauth2 as oauth
import json
import sys
import config
import urllib

"""

Your Twitter Feed:
Tweet is: @DRMJodhpurNWR @RailMinIndia @drmmumbaicr @sureshpprabhu https://t.co/8sNVst6aMx -- Any update on this  , still no reply
Tweet is: @DRMJodhpurNWR @RailMinIndia @drmmumbaicr PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
Tweet is: @RailMinIndia @DRMJodhpurNWR @drmmumbaicr Any Updates.... https://t.co/X5DEy5Pa6W
Tweet is: @sureshpprabhu @RailMinIndia can you help -- https://t.co/uChaI3fUgC
Tweet is: Check my tweets , looks like a nexus in railway ticket booking.... https://t.co/54T9SsEpFy
Tweet is: @ndtv @timesofindia @aajtak guess railway agents/corrupt staff milking money due to mis-utilization of HQ Quota.https://t.co/Awt0jGWClp …
Tweet is: @ndtv @timesofindia agent nexus in railway tkt bking PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
Tweet is: @sureshpprabhu @RailMinIndia guess railway agents/corrupt staff milking money due to mis-utilization of HQ Quota.https://t.co/Awt0jGWClp
Tweet is: @sureshpprabhu @RailMinIndia can you look into this railway agent/corrpt staff nexus, was application submitted to DRM for HQ allocation
Tweet is: @sureshpprabhu @RailMinIndia due to this my wife and 7 yrs old daughter couldnt travel , last ticket status after chrt preparation CKWL1/2
Tweet is: @sureshpprabhu @RailMinIndia agent nexus in ticket booking PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
Tweet is: Train No:12479  journey dt:22/12/2015 , @DRMJaipur @sureshpprabhu @RailMinIndia , ticket bked by agt in mumbai conf. in HQ quota misused
Tweet is: @sureshpprabhu @RailMinIndia can you look into this railway agent/corrpt staff nexus, was application submitted to DRM for HQ allocation
Tweet is: @sureshpprabhu @RailMinIndia due to this my wife and 7 yrs old daughter couldnt travel , last ticket status after chrt preparation CKWL1/2
Tweet is: @sureshpprabhu @RailMinIndia agent nexus in ticket booking PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
The available number of calls left: 163

Posting your tweet: This is a new tweet containing keyword python
Successfully posted your tweet: This is a new tweet containing keyword python

Posting your tweet: This is a new tweet containing keyword python2
Successfully posted your tweet: This is a new tweet containing keyword python2

Trying to find the tweet containing text: python

Found the tweet containing text: python
The tweet text is : This is a new tweet containing keyword python2
Deleting tweet: This is a new tweet containing keyword python2

Found the tweet containing text: python
The tweet text is : This is a new tweet containing keyword python
Deleting tweet: This is a new tweet containing keyword python

Your Twitter Feed:
Tweet is: @DRMJodhpurNWR @RailMinIndia @drmmumbaicr @sureshpprabhu https://t.co/8sNVst6aMx -- Any update on this  , still no reply
Tweet is: @DRMJodhpurNWR @RailMinIndia @drmmumbaicr PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
Tweet is: @RailMinIndia @DRMJodhpurNWR @drmmumbaicr Any Updates.... https://t.co/X5DEy5Pa6W
Tweet is: @sureshpprabhu @RailMinIndia can you help -- https://t.co/uChaI3fUgC
Tweet is: Check my tweets , looks like a nexus in railway ticket booking.... https://t.co/54T9SsEpFy
Tweet is: @ndtv @timesofindia @aajtak guess railway agents/corrupt staff milking money due to mis-utilization of HQ Quota.https://t.co/Awt0jGWClp …
Tweet is: @ndtv @timesofindia agent nexus in railway tkt bking PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
Tweet is: @sureshpprabhu @RailMinIndia guess railway agents/corrupt staff milking money due to mis-utilization of HQ Quota.https://t.co/Awt0jGWClp
Tweet is: @sureshpprabhu @RailMinIndia can you look into this railway agent/corrpt staff nexus, was application submitted to DRM for HQ allocation
Tweet is: @sureshpprabhu @RailMinIndia due to this my wife and 7 yrs old daughter couldnt travel , last ticket status after chrt preparation CKWL1/2
Tweet is: @sureshpprabhu @RailMinIndia agent nexus in ticket booking PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
Tweet is: Train No:12479  journey dt:22/12/2015 , @DRMJaipur @sureshpprabhu @RailMinIndia , ticket bked by agt in mumbai conf. in HQ quota misused
Tweet is: @sureshpprabhu @RailMinIndia can you look into this railway agent/corrpt staff nexus, was application submitted to DRM for HQ allocation
Tweet is: @sureshpprabhu @RailMinIndia due to this my wife and 7 yrs old daughter couldnt travel , last ticket status after chrt preparation CKWL1/2
Tweet is: @sureshpprabhu @RailMinIndia agent nexus in ticket booking PNR:2413208434 CKWL/23 confirmed in HO quota but CKWL9/10 PNR:2757985160 not cnf
The available number of calls left: 160
[Finished in 3.4s]
"""

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
		## By default get first 10 tweets , if no number specified	
		## Twitter api link to get our tweets
		### "https://api.twitter.com/1.1/statuses/user_timeline.json?""
		self.show = show
		self.force = force  ## To reload the twitter feed once you delete a tweet
		self.user_timeline = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
		self.encode_message =  urllib.urlencode({'screen_name':self.screenname})
		self.final_endpoint = self.user_timeline + self.encode_message
  		if self.my_tweets == 0 or self.force == 1:	
			self.mytweets_response, self.mytweets_data = self.connect.request(self.final_endpoint,'GET')
			self.my_tweets = json.loads(self.mytweets_data)
		if self.show == 1:
			print "\nYour Twitter Feed:"
			for self.tweet in self.my_tweets:
				print "Tweet is: %s" %(self.tweet['text'])
			print "The available number of calls left:", self.mytweets_response['x-rate-limit-remaining']	
		return self.mytweets_response,self.my_tweets	

	def findtweet(self,findstring,delete=0):
		self.findstring = findstring
		self.delete = delete
		## You first need to call the mytweets method
		#self.mytweets()
		if self.my_tweets == 0:
		## Call the mytweets method
			self.mytweets()
		for self.tweet_find in self.my_tweets:
			if self.tweet_find['text'].find(self.findstring.lower()) != -1:
				print "\nFound the tweet containing text: %s" %(self.findstring)
				#print "The tweet id is : %s" %(self.tweet_find['id'])
				print "The tweet text is : %s" %(self.tweet_find['text'])
				if self.delete == 1:
					## https://api.twitter.com/1.1/statuses/destroy/:id.json
					print "Deleting tweet: %s" %(self.tweet_find['text'])
					self.tweet_id =  self.tweet_find['id']
					self.destory_endpoint = "https://api.twitter.com/1.1/statuses/destroy/"
					self.final_destroy_endpoint = self.destory_endpoint + str(self.tweet_id) + ".json"
					#print self.final_destroy_endpoint
					self.delete_response, self.delete_data = self.connect.request(self.final_destroy_endpoint,'POST')
					#print self.delete_response
					#print self.delete_data
		self.delete = 0	

	def post(self,message):
		self.message = message
		self.post_endpoint = "https://api.twitter.com/1.1/statuses/update.json"
		self.encode_message =  urllib.urlencode({'status':self.message})
		## Now actual posting to twitter
		print "\nPosting your tweet: %s" %(self.message)
		self.post_response, self.post_data = self.connect.request(self.post_endpoint,'POST', self.encode_message)
		#print self.post_data
		#{"errors":[{"code":187,"message":"Status is a duplicate."}]}
		#print type(self.post_data)
		if self.post_data.find('errors') != -1:
			print "Error in posting your tweet,below is the error"
			print self.post_data
		else:
			print "Successfully posted your tweet: %s" %(self.message)	
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
	hitesh.deletetweet("python") ## to delete tweet containing string python
	hitesh.mytweets(show=1)	




