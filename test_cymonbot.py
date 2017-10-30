import cymonbot
from cymon import Cymon
import requests
from slackclient import SlackClient
import time
import os

CYMON_TOKEN = os.environ["CYMON_TOKEN"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Test request_error_handler(e)
## request_error_handler(exception) => string
def test_answer():
    res = "I can't fulfill your request. Cymon says:\n" + str(requests.exceptions.RequestException)\
    +"\nTry a different IP address."
    assert cymonbot.request_error_handler(requests.exceptions.RequestException) == res

# Test at_bot(message, botid)
# at_bot(string, string) => string
def test_ab_1():
    IDupc = "G3N3R1C1D"
    mes1 = "This is a message without a command directed <@G3N3R1C1D>"
    mes2 = "This is a message without a command directed <@G3N3R1C1D> possible command"
    mes3 = "This is a message not directed <@cymon> but at someone else"
    mes4 = "This is a message directed <@G3N3R1C1D> that does not have a possible command"
    mes5 = "This is a message directed <@G3N3R1C1D> hi"

    assert cymonbot.at_bot(mes1, IDupc) == "" 
    assert cymonbot.at_bot(mes2, IDupc) == "possible command"
    assert cymonbot.at_bot(mes3, IDupc) == None
    assert cymonbot.at_bot(mes4, IDupc) == "that does not have a possible command"
    assert cymonbot.at_bot(mes5, IDupc) == "hi"


# Test process(command)
# process(string) => (string, string)
# Note that process(command) will never take a Nonetype
def test_process1():
    c1 = "possible command"
    c2 = "that does not have a possible command"
    c3 = "hi"
    c4 = ""

    assert cymonbot.process(c1) == ("possible", "command")
    assert cymonbot.process(c2) == (None, None)
    assert cymonbot.process(c3) == ("hi", None)
    assert cymonbot.process(c4) == (None, None)

###############################################################################

# Test integration with Slack

# Test integration with Cymon
# Test do_task(task, info)
# do_task(string, string) => string
def test_dt1():
    api = Cymon(CYMON_TOKEN)
    sampleIP = "5.248.253.190"
    reflookup = {"addr": "5.248.253.190", "created": "2015-06-19T22:11:26", "updated": "2015-06-19T22:11:43", "sources":\
    ["pbl.spamhaus.org","zen.spamhaus.org","v6.fullbogons.cymru.com","dnsbl.ahbl.org","tor.ahbl.org","virustotal.com","urlquery.net"],\
    "events": "https://cymon.io/api/nexus/v1/ip/5.248.253.190/events","domains": "https://cymon.io/api/nexus/v1/ip/5.248.253.190/domains",\
    "urls": "https://cymon.io/api/nexus/v1/ip/5.248.253.190/urls"}

    # IP used as example in http://docs.cymon.io/v1/#ip-lookup. 
    # Formatting differs due to Python but check that contents are the same.
    samplelookup = api.ip_lookup(sampleIP)
    for key in samplelookup:
        if (key == "created") or (key == "updated"):
            assert samplelookup[key][:len(samplelookup[key])-1] == reflookup[key]
        else:
            assert samplelookup[key] == reflookup[key]

