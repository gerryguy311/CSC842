#Prologue 
Name: Gerry Auger
Date - 8/28/16
Module - 1. TweePreText.py
#Purpose
TweePreText is a python script that queries Twitter for a specified account, returning a list ordered by highest frequency of hashtags.
User timelines belonging to protected users may only be requested when the authenticated user either “owns” the timeline or is an approved follower of the owner.

The logic is individuals that take time to Tweet and add a Hashtag have an interest or care relative to that topic. With hashtags having a high frequency, it suggests the indivdual cares more about that topic. Trust is a powerful element in a social engineering attack, and knowing ideas/topics an individual has interest in provides an easy "in" to conversation and manipulation.

#Usage 
------------------------------------
TweePreText.py Argument Usage: 
-t Twitter Target 
-c Number of tweets to go back in time for user
-r Number of hashes to return
-w shows WordCloud graphic
------------------------------------
Default values are: -t  Gerald_Auger  -c  200  -r 10  
This is my Twitter Account, 200 messages (the limit) and 10 hash tags.

#Other
You will need to generate your own Twitter Access Tokens and put the values in the code.
dev.twitter.com
Twitter Rate limiting limits 180 requests every 15 minutes.
Twitter will only go back up to 200 tweets. This includes retweets and replies.


#Future Work
- Add Session Tokens to Oauth.io or some other vendor so I dont have to give away the secret key but can allow my code to be run.
- 
