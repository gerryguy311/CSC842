#Name - 
Gerry Auger
#Date - 
11/20/16
#Module - 5
Suspicious Domain Detector
#Purpose
This tool is designed to comb through DNS logs for an organization and determine if there are any that were registered within the last X (currently x=5) days, an indicator that the site is suspicous.
#Usage 
The tool can be cron'd, but takes one input of a DNS log. Currently the code is written for a custom log file. Some tweaking to work for your log files would need to be done. Future work is to map it to more standard log formats (bro log for example).
#Other
Future ITEMS
1. Implement local db to capture domains already reviewed to reduce overhead and increase performance.
2. Push suspicious domains to VirusTotal and include response in email to infosec
3. If VirusTotal response is malicious site, auto sinkhole the domain for the organization.

If you have any feedback on ways to improve please advise.

