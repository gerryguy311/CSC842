#!/usr/bin/env python
#Started then modd'd code from https://github.com/amueller/word_cloud/blob/master/examples/simple.py
#@Gerald_Auger
#8/28/16
# DSU D.Sc CSC848 Fall 2016

#Twitter API access requirements
#Lots of blank space so the video wont show this.
#Register with Twitter to get tokens/keys/secrets
#https://apps.twitter.com/

ACCESS_TOKEN = '<your generated value here>'
ACCESS_SECRET = '<your generated value here>'
CONSUMER_KEY = '<your generated value here>'
CONSUMER_SECRET = '<your generated value here>'


"""

PURPOSE:
TweePreText is a python script that queries Twitter for a specified account, returning a list ordered by highest frequency of hashtags.
You do not have to be 'follow' or be 'followed' by an individual to query. 
The logic is individuals that take time to Tweet and add a Hashtag have an interest or care relative to that topic. With hashtags having a high frequency, it suggests the indivdual cares more about that topic. Trust is a powerful element in a social engineering attack, and knowing ideas/topics an individual has interest in provides an easy "in" to conversation and manipulation.

Code for generating the wordCloud at the bottom was just tweaked code from WordCloud example.py script. I changed the input.
"""
debug = False

import sys, getopt #for processing command line args.
from os import path
from wordcloud import WordCloud #wordCloud for having fun with the visual represenation of the hashtags
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream #Twitter API through Python
import json #working with Twitter API returned Objects
from collections import Counter #for word frequency analysis
import matplotlib.pyplot as plt # Display the generated image: the matplotlib way:

#Dynamic Variables and Cmd Line Args:
TARGET = "Gerald_Auger"
HASHES_TO_RETURN = 10
COUNT = 200
showWordCloud = False

try:
	opts, args = getopt.getopt(sys.argv[1:], "wht:c:r:", ["wordCloud", "help", "target=", "count=", "hashesToReturn="])
except getopt.GetoptError:
	print '\n\r\n\r------------------------------------\n\r TweePreText.py Argument Usage: \n\r -t Twitter Target \n\r -c Number of tweets to go back in time for user\n\r -r Number of hashes to return \n\r -w shows WordCloud graphic \n\r------------------------------------\n\r\n\r'
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print '\n\r\n\r------------------------------------\n\r TweePreText.py Argument Usage: \n\r -t Twitter Target \n\r -c Number of tweets to go back in time for user\n\r -r Number of hashes to return \n\r -w shows WordCloud graphic \n\r------------------------------------\n\r\n\r'		
		if debug: print 'Default values are: -t ', TARGET, ' -c ', COUNT, ' -r',HASHES_TO_RETURN 
		sys.exit()
	elif opt in ("-c", "--count"):
		if debug: print "in -c logic. arg is ", arg, "Count is ", COUNT
		COUNT = arg
	elif opt in ("-r", "--hashesToReturn"):
		HASHES_TO_RETURN = arg
	elif opt in ("-t", "--target"):
		if debug: print "in -t logic. arg is ", arg, "Target is ", TARGET
		TARGET = arg
	elif opt in ("-w", "--wordCloud"):
		if debug: print "in -w logic. arg is "
		showWordCloud = True

if debug: print 'Target is:', TARGET
if debug: print 'HASHES_TO_RETURN:', HASHES_TO_RETURN
if debug: print 'COUNT: ', COUNT

#Build Twitter object to hook into API then pull a users timeline.
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth=oauth)
timeline = twitter.statuses.user_timeline(screen_name=TARGET, count=COUNT, exclude_replies="false", include_rts="true")


#Normalize to string #convert to JSON object
timelineString = json.dumps(timeline)
timelineJSON = json.loads(timelineString)

if debug: counter = 0 #to confirm max tweets returned
hashtagList = []
for G in timelineJSON:
	if debug:	counter += 1 #to confirm max tweets returned
	for x in G['entities']['hashtags']:

		hashtagList.append(x['text'].lower())

if debug: print "counter: ", counter #to confirm max tweets returned




counts = Counter(hashtagList)
if debug: print counts
print '\n\rMost common #Hashtags for Twitter User:' + TARGET
print '#HASHTAG : INSTANCES'
for tag, count in counts.most_common(int(HASHES_TO_RETURN)):
    print '%s: %i' % (tag, count)
    


#initialize vars going into this for loop
text = ""
# Generate a word cloud image; Its fun, why not? use the -w arg
if showWordCloud: 
	for word in hashtagList:
			text = text + " " + word
			if debug: print text


	wordcloud = WordCloud().generate(text)
	wordcloud = WordCloud(max_font_size=100, relative_scaling=.85, max_words=int(HASHES_TO_RETURN)).generate(text)
	plt.figure()
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()


#END OF FILE
