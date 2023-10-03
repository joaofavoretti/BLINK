# /app/views/gsb.py

from flask import Blueprint, jsonify, request
from app.models import Urls
import requests
import os

gsb_bp = Blueprint('gsb', __name__, url_prefix='/gsb')

def GSB_URL():
    key = os.environ.get('GSBAPIKEY')
    
    if key is None:
        print('GSBAPIKEY environment variable not set')
        return None

    return "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + key

def REQ_BODY(urls):
    return {
        "client": {
            "clientId": "phishing-research",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["SOCIAL_ENGINEERING", "MALWARE", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": urls
        }
    }

def validate_urls(urls):
    urls_res = []
    matches = []

    num_urls = len(urls)
    batch_size = 400

    for i in range(0, num_urls, batch_size):
        urls_req = [{'url': url.url} for url in urls[i:i+batch_size]]
        res = requests.post(GSB_URL(), json=REQ_BODY(urls_req))

        if res.status_code != 200:
            return jsonify({
                'error': 'Google Safe Browsing API returned status code ' + str(res.status_code)
            })
        
        if 'matches' in res.json():
            matches += res.json()['matches']
            for result in res.json()['matches']:
                url = Urls.objects.get(url=result['threat']['url'])
                urls_res.append(url.url)
                url.update(gsb_inspection={
                    'triggered': True,
                    'comments': result
                })
    
    urls_req = [url.url for url in urls]

    for url in urls_req:
        if url not in urls_res:
            url = Urls.objects.get(url=url)
            url.update(gsb_inspection={
                'triggered': False,
                'comments': None,
            })

    return matches

@gsb_bp.route('/validate_database', methods=['POST'])
def validate_database():
    urls = Urls.objects.all()
    
    matches = validate_urls(urls)

    return jsonify(matches)

@gsb_bp.route('/validate_unkown', methods=['POST'])
def validate_unkown():
    urls = Urls.objects(gsb_inspection=None)
    
    matches = validate_urls(urls)

    return jsonify(matches)