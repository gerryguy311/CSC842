
#Gerald Auger gmauger@dsu.edu
#842 Mod 5 - 11/17/16
#Python script that looks at a domain and queries to see if it was registered within a dynamic range period with
#the intention of calling out recently registered domains as an indicator of potential malicious activity.

#querying multiple registrars
import pythonwhois

#OS/sys commands for calling terminal-notifier
import sys
import os
from subprocess import call

#for calculating todays date and creation date for determing domain registration age
from datetime import date, datetime

#for extracting domain and suffix from DNS logs. String clean-up for providing standardized input to whois query
import tldextract

#for implementing delay to ensure account doesnt get banned for hammering on WHOIS server
import time
import random

#simple database tool to save off domains already looked up to reduce overhead on hammering whois service
import dbm

#modules to support sending email when suspicious domains detected.
import smtplib
import string

#modules to support virusTotal API interface
import requests

#Check a URL against VirusTotal; returns a JSON formatted msg.
def CheckURLatVT(url):
	vt_apiKey = 'ENTER YOUR PUBLIC VT API KEY HERE'
	headers = {
  "Accept-Encoding": "gzip, deflate",
  "User-Agent" : "gzip,  My Python requests library example client or username"
  }
	params = {'apikey': vt_apiKey, 'resource':url , 'scan': '1'}
	response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
  	params=params, headers=headers)
	json_response = response.json()
	#print "JSON RESPONSE: " + str(json_response)
	return json_response

#verify inputs are program and domain 
if len(sys.argv) != 2:
	print "[*] Error in execution. \n[*]Proper Usage: python SuspectDomainDetector.py dns_log_file"
	sys.exit(0)


#threshold value in days of how far back you want to look. if value is 5, domains less than 5 days old will be flagged as suspect.
domain_age_threshold = 5
sleep_length_seconds = 15

#list to hold unique domains for whois'ing later
unique_domain_list = []
susp_domain_list = []

#body of email to be built dynamically
body = ""

# connecting to a persistent local database
#db = dbm.open('cache', 'c')

#Access DNS log file; Parse for domain and feed this list to whois.
file = sys.argv[1]
f = open(file, 'r')

#iterate through DNS logs, extract domains and suffixes; 
for line in f:
	named = line.split("|")
	tokens = named[5].split(" ")
	dom_suf = tokens[4][1:-2]
	domain = tldextract.extract(dom_suf)
	domain = domain.registered_domain
	unique_domain_list.append(domain)

#remove duplicates from list; no need to query more than once
unique_domain_list = list(set(unique_domain_list))

#remove a blank element at the front of the list
unique_domain_list = unique_domain_list[1:]

#Alexa top 1Million websites. Remove any of these from the unique domain list of sites to check via whois. (implicit trusted)
top1mFile = open('top-1m.csv', 'r')
for i in top1mFile:
	i = i.strip()
	for x in unique_domain_list:
		x = x.strip()
		if i == x:
			#print "[*] HIT! " + i + " " + x
			unique_domain_list.remove(i)
		#else:
			#print i + " not " + x

#review persistent db of looked up domains to pare down the list to only new domains discovered
#for element in unique_domain_list:
#	if element in db:
#		print "[*] Domain "+ element + " already looked up.\n"
#	else:
#		print "[*] Adding "+element + " to db of domains.\n"


	#query multiple registrars with the domain for creation date
	#if creation date is within the age threshold report it as suspicious. i.e age = 5, if domain was reg'd in the last 5 days its suspect.
	
	#assuming MAC, issue terminal notifcation of susipicous actiivty.
	#timer added to avoid being banned for abusing whois services.
print "[*] Beginning WHOIS lookups on this number of domains: " +str(len(unique_domain_list))
for element in unique_domain_list:
	#Lookup the domain via multiple whois; Calculate today minus creation_date to determine how old/young the domain is. use sleep timer to avoid being banned
	#print "WHOIS PERFORMING ON "+ element
	try:
		details = pythonwhois.get_whois(element)
		diff = (datetime.now() - details['creation_date'][0]).days
		print "[*] Checking creation date on: " + element +""
		if diff <= domain_age_threshold:
			message = "\n[*] POTENTIAL ISSUE: Domain " + domain + " registered "+ str(details['creation_date'][0]) +"; within the last " + str(domain_age_threshold) + " days!\n[*] This is suspect behavior. Verify and ensure this domain is what you are expecting.\n"
			body = body + "\n" + message
			print message
			
			#query VirusTotal for more info
			#VirusTotal restricts to 4 queries per minute (w/public api key). 
			try:
				json_vt_response = CheckURLatVT(element)
				vt_positive = json_vt_response['positives']
				vt_total = json_vt_response['total']
				vt_link = json_vt_response['permalink']
				vt_info = str(vt_positive) + "/" + str(vt_total) + ": There are " + str(vt_positive) + " positives over " + str(vt_total) + "  services that check for malicious sites. More info at " + str(vt_link) + "\n"
				body = body + "\n" + vt_info

			except:
				err_msg = "Error querying VirusTotal for: " + domain
				body = body + "\n" + err_msg
			#if the tool is to be run on local Mac workstation, use terminal-notifier to alert user.
			#notify_msg = "\" " + domain + " registered " + str(details['creation_date'][0]) + "\" "
			#cmd = "terminal-notifier -title \"*** SUSPECT DOMAIN DETECTED ***\" -timeout 3 -message " + notify_msg 
			#print cmd
			#os.system(cmd)

			#Include VirusTotal lookup for suspicious domain.
			# vt = virusTotalLookup(URL)
			# vt_msg = vt.resposne.parse()
			# body = body + "\n" + vt_msg

		#return a list with lots of great info. set pythonwhois verbose to True to see all fields; set pythonwhois to False to hide all fields.
		pythonwhois_verbose = False
		if pythonwhois_verbose:
			keys = details.viewkeys()
			values = details.viewvalues()
			print "KEYS: \n" + str(keys)
			print "\n\n"
			print "VALUES \n" + str(values)

		#delay to avoid getting banned from whois for abuse
		time.sleep(sleep_length_seconds)
	except:
		err_msg = "Domain not found through python_whois " + domain
		body = body + "\n" + err_msg

#send email if anything worthwhile was detected.
if body != "":
	print "\n\n[*] Preparing Email... \n"
	print "EMAIL BODY: " +body
	sys.exit()
	username = ""
	password = ""
	HOST = ""
	SUBJECT = "Suspicious Domain List - " + str(datetime.now())
	TO = 'augerg@musc.edu'
	FROM = 'augerg@musc.edu'
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
		print "Email sent: " + BODY
	except:
		print "Error: unable to send email"

 

