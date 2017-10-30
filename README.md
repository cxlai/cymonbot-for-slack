# cymonbot-for-slack
Slack bot based on Cymon's Python API. Looks up information about IP addresses and more.

## About
[Cymon](http://www.cymon.io) aggregates threat sournces into a single interface. Cymonbot is a Slack bot written in Python that pulls information from Cymon. Cymonbot can be invited to any channel. While it's online, users can ask Cymonbot (Cymon Says) for security information about IP addresses, such as recent security events related to an IP address and domains associated with an IP address. With this information, users can be more informed about the trustworthiness of IP addresses and internet traffic. With information comes more power for the users! 

## Requirements
* A server with Python 3.* and the Python packages in `requirements.txt` installed. 
* Cymon API key (free!) obtained with an account at [Cymon.io](http://www.cymon.io)
* Slack bot key (free!) obtained with a Slack account, workspace, and service. 
    1. Visit [Slack API apps](https://api.slack.com/apps)
    2. Select the service you'd like to attach Cymonbot to. Make a new one if it doesn't exist yet.
    3. Create a bot user (under 'Bot Users').
    4. Click 'OAuth & Permissions' for the Bot User OAuth Access Token.

## Installation
1. Clone the repo. 
2. Install Python requirements with `pip install -r requirements.txt`. 
3. Set environmental variables. This means private tokens aren't hardcoded into visible code of your repo!
    * `BOT_TOKEN` and `CYMON_TOKEN` are all you should need!
4. Invite `@cymonbot` to your `#general` channel.
5. Run `cymonbot.py` on a server with all requirements fulfilled. While `cymonbot.py` is running, the user `@cymonbot` should be online in the `#general` channel. 

## Usage
While Cymonbot is running, mention `@cymonbot` with the following commands: 
* `help`: display the below usage information
* `iplookup [IP address]`: returns when the address was created and its sources
* `ipevents [IP address]`: returns any security events associated with the IP address
* `ipdomains [IP address]`: returns any domains associated with the IP address
* `ipurls [IP address]`: returns any URLs associated with the IP address
* `ipblacklist [tag]`: returns IP addresses blacklisted in the past day based on the tag (options are `malware`, `botnet`, `spam`, `phishing`, `malicious activity`, `blacklist`, `dnsbl`)
