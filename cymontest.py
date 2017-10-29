import requests
from cymon import Cymon
api = Cymon("3dfdd08c72aec1245ff3242d276be06d41b6cebc")

def request_error_handler(e):
    res = "I can't fulfill your request. Cymon says:\n" 
    res += str(e)
    return res

def do_task(task, info):
    try:
        res = ""
        if (task == "iplookup"):
            r = api.ip_lookup(info)
            res = "This IP address was created "+r["created"]+" and last"+\
            " updated on "+r["updated"]+". It has the following sources:\n"
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
                    if result["description"]: res += result["description"]
                    res += "\n"
            else:
                res = "There are no security events associated with this IP address."
        elif (task == "ipdomains"):
            r = api.ip_domains(info)
            if r["count"] > 0:
                res = "Here are all the domains associated with "+info+\
                " based on Cymon's databases.\n"
                for result in r["results"]:
                    res += result["name"]+" created on "+result["created"]+"."
                    res += "\n"
            else:
                res = "There are no domains associated with this IP address.\n"
        elif (task == "ipurls"):
            r = api.ip_urls(info)
            if r["count"] > 0:
                res = "Here are all the URLs associated with "+info+\
                " based on Cymon's databases.\n"
                for result in r["results"]:
                    res += result["location"]+" created on "+result["created"]+"."
                    res += "\n"
            else:
                res = "There are no URLs associated with this IP address.\n"
        elif (task == "ipblacklist"):
            r = api.ip_blacklist(info)
            if r["count"] > 0:
                res = "In the past day, these IP addresses have been\
                     tagged with "+info+"."
                for result in r["results"]:
                    res += result["addr"]
                    res += "\n"
            else:
                res = "There are no IP addresses tagged with "+info+" in the \
                    past day on Cymon.\n"
        elif (task == "help"):
            res = '''Hi! I'm a bot that can give you relevant security information on IP addresses. My commands are:\n
            - `iplookup [IP address]`: returns when the address was created and its sources
            - `ipevents [IP address]`: returns any security events associated with the IP address
            - `ipdomains [IP address]`: returns any domains associated with the IP address
            - `ipurls [IP address]`: returns any URLs associated with the IP address
            - `ipblacklist [tag]`: returns IP addresses blacklisted in the past day based on the tag
               (`malware`, `botnet`, `spam`, `phishing`, `malicious activity`, `blacklist`, `dnsbl`)\n'''
        return res
    except requests.exceptions.RequestException as e:
        return request_error_handler(e)

print do_task("help", None)
print do_task("iplookup", "5.248.253.190")
print do_task("ipevents", "5.248.253.190")
print do_task("ipdomains", "5.248.253.190")
print do_task("ipurls", "5.248.253.190")
print do_task("ipblacklist", "5.248.253.190")

#print api.domain_lookup("google.com")
#print api.ip_domains("185.27.134.165")
#print api.ip_blacklist("botnet")
