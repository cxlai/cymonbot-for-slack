'''
cymonbot.py handles messages directed to the bot user (based on ID) and 
responds if possible. If it is a command Cymonbot can fulfill, it does so
using Cymon's Python API. It can also explain its own usage methods.

The commands Cymonbot can handle are IP Lookup, IP Events, IP Domains, IP URLs,
and IP Blacklists. More documentation on these API requests can be found at
http://docs.cymon.io/v1/#apis. 
'''

import os
import requests
from cymon import Cymon
import time
from slackclient import SlackClient

# Store your Cymon and Slack bot tokens as environmental variables for security.
CYMON_TOKEN = os.environ["CYMON_TOKEN"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_NAME = "general"
BOT_NAME = "cymonbot"

def request_error_handler(e):
# Handles errors in the request to API. Can be updated to have specific error
# handling messages based on the type of error from requests module.
    res = "I can't fulfill your request. Cymon says:\n"
    res += str(e)
    res += "\nTry a different IP address."
    return res

def at_bot(message, botid):
# Parse message to see if it's directed at Cymonbot and return
# command if it is.
    command = None
    if message and len(message) > 0:
        if botid in message:
            command = message.split(botid)[1].lower()
            try:
                command = command.split("> ")[1]
            except:
                #This occurs when there is no text after mentioning Cymonbot.
                command = ""
    return command

def process(command): 
# Use whitespace to split command into task and info
# i.e. the command and the IP address or tag.
    words = command.split()
    n = len(words)
    if (n==1):
        (task, info) = (words[0], None)
    elif (n==2):
        (task, info) = (words[0], words[1])
    else:
        (task, info) = (None, None)
    return (task, info)

def do_task(task, info):
# Takes a task in format specified by bot's introduction and completes lookup
# in Cymon database. Handles errors with helper function. 
    api = Cymon(CYMON_TOKEN)
    greetings = ["hi", "hello", "Hi", "Hello"]
    try:
        res = ""
        if (task == "help" or task in greetings):
            res = '''Hi! I'm a bot that can give you relevant security information on IP addresses. My commands are:
            - `iplookup [IP address]`: returns when the address was created and the information sources 
            - `ipevents [IP address]`: returns any security events associated with the IP address
            - `ipdomains [IP address]`: returns any domains associated with the IP address
            - `ipurls [IP address]`: returns any URLs associated with the IP address
            - `ipblacklist [tag]`: returns IP addresses blacklisted in the past day based on the tag
               (`malware`, `botnet`, `spam`, `phishing`, `malicious activity`, `blacklist`, `dnsbl`)\n'''
        elif (task == "iplookup"):
            r = api.ip_lookup(info)
            res = "This IP address was created "+r["created"][:len(r["created"])-1]+" and last"+\
            " updated on "+r["updated"][:len(r["updated"])-1]+". It has information from the following sources:\n"
            for source in r["sources"]:
                res += source
                res += "\n"
        elif (task == "ipevents"):
            r = api.ip_events(info)
            if r["count"] > 0:
                res = "Here are all the events associated with "+info+\
                " based on Cymon's databases.\n"
                for result in r["results"]:
                    res += result["title"]+" on basis of "+result["tag"]+"."
                    if result["description"]: res += "\n"+result["description"]+"\n"
                    res += "\n"
            else:
                res = "There are no security events associated with this IP address."
        elif (task == "ipdomains"):
            r = api.ip_domains(info)
            if r["count"] > 0:
                res = "Here are all the domains associated with "+info+\
                " based on Cymon's databases.\n"
                for result in r["results"]:
                    res += result["name"]+" created on "+result["created"][:len(result["created"])-1]+"."
                    res += "\n"
            else:
                res = "There are no domains associated with this IP address.\n"
        elif (task == "ipurls"):
            r = api.ip_urls(info)
            if r["count"] > 0:
                res = "Here are all the URLs associated with "+info+\
                " based on Cymon's databases.\n"
                for result in r["results"]:
                    res += result["name"]+" created on "+result["created"][:len(result["created"])-1]+"."
                    res += "\n"
            else:
                res = "There are no URLs associated with this IP address.\n"
        elif (task == "ipblacklist"):
            r = api.ip_blacklist(info)
            if r["count"] > 0:
                res = "In the past day, these IP addresses have been "+\
                "tagged with "+info+".\n"
                for result in r["results"]:
                    res += result["addr"]
                    res += "\n"
            else:
                res = "There are no IP addresses tagged with "+info+" in the \
                    past day on Cymon.\n"
        return res
    except requests.exceptions.RequestException as e:
        return request_error_handler(e)
    except: 
        return "Sorry, I can't do that. Ask me for 'help' and I'll give you instructions!"

def main():
# Connect to Slack client using bot token (sets Cymonbot to 'online').
# Then waits for any direct mentions to @cymonbot and responds with either
# a help message, command fulfillment, or suggestions for valid commands if
# invalid. Does not respond unless directly mentioned. 
    sc = SlackClient(BOT_TOKEN)
    if sc.rtm_connect():
        sc.rtm_send_message(CHANNEL_NAME, "Hi! I'm Cymon Says, a Slack bot. Ask me directly for 'help' and I'll tell you what I can do.")
        # Get bot ID #
        apiCall = sc.api_call("users.list")
        if apiCall.get("ok"):
            users = apiCall.get("members")
        for user in users: 
            if ("name" in user) and (user.get("name") == BOT_NAME):
                BOT_ID = user.get("id")
        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                command = at_bot(message, BOT_ID)
                if (command is not None):
                    (task, info) = process(command)
                    if (task is None):
                        sc.rtm_send_message(CHANNEL_NAME, "Sorry, I don't understand that. Ask me for 'help' if you need it.")
                    else:
                        sc.rtm_send_message(CHANNEL_NAME, do_task(task, info))
            # Sleep for half a second
            time.sleep(0.5)
	
if __name__ == '__main__':
    main()
