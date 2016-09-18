"""
#Gerry Auger - Module 2, underlying python code to tie to lambda function for Alexa (amazon echo) current vuln skill set.
This code built off of alexa-skills-kit-color-expert-python template provided by Amazon.
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
#    "outputSpeech": {
#       "type": "SSML",
#       "ssml": "<speak>Cyber security news for you. <audio src="https://carfu.com/audio/carfu-welcome.mp3" /></speak>"
#   }
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "I am Hal. I will tell you current vulnerabilities. " \
                    "Please ask if you want current vulnerabilities or vulnerabilities by system type by saying, " \
                    "what new vulnerabilities are there, " \
                    "or speaking, tell me vulnerabilities for system, where system is a valid system type, " \
                    "current system types are Windows, Linux, Mac OS X, mobile, and wireless"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Are you there? " \
                    "Please ask if you want current vulnerabilities or vulnerabilities by system type by saying, " \
                    "what new vulnerabilities are there, " \
                    "or speaking, tell me vulnerabilities for system, where system is a valid system type, " \
                    "current system types are Windows, Linux, Mac OS X, mobile, and wireless"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for brushing up on new vulnerabilities. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def get_vuln_data_pull():
    """get vulns here"""
    vulnList = ["Microsoft Internet Explorer and Edge CVE-2016-3351 Information Disclosure Vulnerability","Microsoft ASP.NET Core MVC Multiple Privilege Escalation Vulnerabilities", "Microsoft Office CVE-2016-0141 Information Disclosure Vulnerability","Microsoft Office CVE-2016-3366 Spoofing Vulnerability"]
    return vulnList

def get_easter_egg():
    session_attributes = {}
    reprompt_text = None
    card_title = "Easter Egg"
    
    speech_output = "This is a hidden feature. This is Gerry's 842 Module 2 assignment."
    should_end_session = False
   
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_new_vulnerabilities():
    session_attributes = {}
    reprompt_text = None
    card_title = "Report Vulnerabilties"
    
    #THIS NEEDS UPDATING TO ACTUALLY PULL CURRENT VULNS    
    '''
    usock = urllib2.urlopen('https://www.symantec.com/xml/rss/listings.jsp?lid=advisories') 
    e = xml.etree.ElementTree.parse(usock).getroot()
    vulnList = e.findall("./channel/item")

    counter = 5
    vulns = ""
    for item in vulnList:
        if counter <=0:
            break
        else:
            vulns = vulns + ", " + item[0].text
            counter = counter - 1

        
    speech_output = "The following items are the newest vulnerabilties."
    speech_output = speech_output + vulns
    '''

    vulnList = ["Microsoft Internet Explorer and Edge CVE-2016-3351 Information Disclosure Vulnerability","Microsoft ASP.NET Core MVC Multiple Privilege Escalation Vulnerabilities", "Microsoft Office CVE-2016-0141 Information Disclosure Vulnerability","Microsoft Office CVE-2016-3366 Spoofing Vulnerability"]
    speech_output = "The following items are the newest vulnerabilties."
    for vuln in vulnList:
        speech_output = speech_output + ", " + vuln
    should_end_session = True
   
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_new_vulnerabilities_category(intent):
    session_attributes = {}
    reprompt_text = None
    card_title = "New vulnerabilties for a category"
  
    if 'vulnCategory' in intent['slots']:
        category = intent['slots']['vulnCategory']['value']

    else:
        speech_output = "I'm not sure what category you said. " \
                        "Please try again."
        #reprompt_text = "I'm not sure what your favorite color is. " \
        #               "You can tell me your favorite color by saying, " \
        #              "my favorite color is red."
    if (category):
         
         #THIS NEEDS UPDATING TO ACTUALLY PULL CURRENT VULNS FOR A CATEGORY, OR FILTER ON PULLED VULNS FOR A CATEGORY.    
        '''
        usock = urllib2.urlopen('https://www.symantec.com/xml/rss/listings.jsp?lid=advisories') 
        e = xml.etree.ElementTree.parse(usock).getroot()
        vulnList = e.findall("./channel/item")

        counter = 5
        vulns = ""
        for item in vulnList:
            if counter <=0:
                break
            else:
                vulns = vulns + ", " + item[0].text
                counter = counter - 1

        
        speech_output = "The following items are the newest vulnerabilties."
        speech_output = speech_output + vulns
        '''

        vulnList = ["Linux Kernel do_mremap Function Boundary Condition Vulnerability, Linux-HA Heartbeat Remote Buffer Overflow Vulnerability, udev Netlink Message Validation Local Privilege Escalation Vulnerability"]
        speech_output = "The following items are the newest vulnerabilties for, " + category
        for vuln in vulnList:
            speech_output = speech_output + ", " + vuln
        
        should_end_session = True
    else:
        speech_output = "I'm not sure what category you are talking about. " 
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WhatNewVulnerabilitiesCategoryIntent":
        return get_new_vulnerabilities_category(intent)
    elif intent_name == "WhatsNewVulnerabilitiesIntent":
        return get_new_vulnerabilities()
    elif intent_name == "EasterEggIntent":
        return get_easter_egg()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
