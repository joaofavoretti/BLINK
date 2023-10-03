import requests
from sensitive import GSBAPIKEY
import json

def GSB_URL(key=GSBAPIKEY):
    return "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + key

def REQ_BODY(url):
    return {
        "client": {
            "clientId": "phishing-research",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["SOCIAL_ENGINEERING", "MALWARE", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

if __name__ == '__main__':

    BENIGN = 'https://www.google.com'
    PHISHING = 'http://aeon-cardkkm.tokyo/jp/login.html'

    with requests.Session() as session:
        res = session.post(GSB_URL(), json=REQ_BODY(PHISHING))
        
        # Print the response as disctionary
        print(res.json())
