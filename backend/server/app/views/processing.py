from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import Urls
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from mongoengine import Q
import time
import multiprocessing
import requests
import sys
import warc
import os
import json

processing_bp = Blueprint('processing', __name__, url_prefix='/processing')

@processing_bp.route('/add_redirection', methods=['POST'])
def get_asdf():
    text = request.json['text']

    print(text)

    return jsonify({'message': 'Toggled'}), 200

@processing_bp.route('/check_database_for_redirections', methods=['POST'])
def check_database_for_redirections():
    EXTENSION_PATH = './nnpljppamoaalgkieeciijbcccohlpoh'
    
    source = request.json['source']

    urls = Urls.objects.filter(Q(source=source)).values_list('id', 'url')
    
    url = urls[2][1]

    chrome_options = Options()
    prefs = {"download_restrictions": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('--load-extension={}'.format(EXTENSION_PATH))
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('user-agent=Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36')
    driver = Chrome(options=chrome_options)
    driver.set_page_load_timeout(40)

    try:
        driver.get('https://www.google.com')
        time.sleep(1)
    except Exception as e:
        driver.quit()

    time.sleep(1)
    try:
        driver.get(url)
        time.sleep(5)
    except:
        driver.quit()
        print('\tTime Out, Continue')

    # Check whether it contains an alert
    try:
        while True:
            driver.switch_to.alert.text
            driver.switch_to.alert.accept()
            time.sleep(1)
    except:
        pass
    driver.quit()

    return jsonify({'url': url}), 200