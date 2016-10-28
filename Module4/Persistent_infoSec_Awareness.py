#!/usr/bin/env python

import sys
import re
import requests
from bs4 import BeautifulSoup
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream #Twitter API through Python
import smtplib
import string

def lambda_handler(event, context):



	ACCESS_TOKEN = '<AWS ACCESS TOKEN>'
	ACCESS_SECRET = '<AWS ACCESS SECRET>'
	CONSUMER_KEY = '<AWS CONSUMER KEY>'
	CONSUMER_SECRET = '<AWS CONSUMER SECRET>'

	url = "https://www.sans.org/tip-of-the-day/rss"
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	
	tipSubject= extract_tip("title", soup)
	tweet = extract_tip("description", soup)
	body = "Todays cybersecurity tip of the day, brought to you by SANSInstitute: \n\n" + tweet
	tweet = "~@SANSInstitute #DailyCyberTip: " + tweet

	if len(tweet) > 140:
		print "[*] Tweet to long. Cutting last sentence off"
		m = re.search("(.*?\.).*" ,tweet)
		tweet = str(m.group(1))
	else:
		print "[*] Tweet acceptable length"

	if len(tweet) <= 140:
		#TWEET TIP
		oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
		twitter = Twitter(auth=oauth)
		print "[*] Tweeting --> " + tweet
		twitter.statuses.update(status=tweet)



	print "\n\n[*] Preparing SANS tip of the day for emailing... \n"

	username = "<AWS SMTP USERNAME>"
	password = "<AWS SMTP PASSWORD>"
	HOST = "email-smtp.us-east-1.amazonaws.com"
	SUBJECT = "Daily CyberSecurity Tip - " + tipSubject
	TO = '<TO>'
	FROM = '<FROM>'
	BODY = string.join((
	        "From: %s" % FROM,
	        "To: %s" % TO,
	        "Subject: %s" % SUBJECT ,
	        "",
	        body
	        ), "\r\n")

	try:
		server = smtplib.SMTP_SSL(HOST, port=465)
		server.set_debuglevel(True) # show communication with the server
		server.login(username, password)
		server.sendmail(FROM, TO, BODY)
		server.quit()
		print "sent daily tip email : " + BODY
	except:
		print "Error: unable to send daily tip email"

 
	return 0



def extract_tip(section, soup):
	skipFirst = True
	for items in soup.find_all(section):
		if skipFirst:
			skipFirst = False
		else:
			str_items = str(items)
			m = re.search('<'+section+'><!\[CDATA\[(.*)\]\]></'+section+'>', str_items)
			if m:
				print "extracting element " + section
				return m.group(1)

			return 0


