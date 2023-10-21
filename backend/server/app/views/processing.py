from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import Urls
from app.models import Redirections
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from mongoengine import Q
import time
import multiprocessing
import requests
import sys
import warc
import os
import json

processing_bp = Blueprint('processing', __name__, url_prefix='/processing')

def check_network_status(url):
    try:
        r = requests.get(url)
        network_status = 'ONLINE'
    except:
        network_status = 'OFFLINE'

    return network_status

def crawl_searching_redirections(url):
    # If url not in the redirections collection
    if Redirections.objects(url=url).count() != 0:
        print(f'URL {url} already scaned')
        return False

    # Registering it in the database to avoid multiple scans
    try:
        url_obj = Urls.objects.get(url=url)
        url_obj.last_update_dt = datetime.now()
    except Urls.DoesNotExist:
        url_obj = Urls(**{
            'url': url,
            'added_dt': datetime.now(),
            'last_update_dt': datetime.now(),
            'source': "MANUAL"
        })
    url_obj.save()

    try:
        redirections_obj = Redirections.objects.get(url=url)
        redirections_obj.last_update_dt = datetime.now()
        redirections_obj.hops_amount = 0
    except Redirections.DoesNotExist:
        redirections_obj = Redirections(**{
            'url': url,
            'last_update_dt': datetime.now(),
            'hops_amount': 0
        })
    redirections_obj.save()

    # Start the trigger to crawl the URL
    print(f'Crawling URL: {url}')
    
    # Constant variables
    EXTENSION_PATH = './nnpljppamoaalgkieeciijbcccohlpoh'   # Custom Browser Extension to Save URL Redirections

    # Configuring Selenium Driver
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--load-extension={}'.format(EXTENSION_PATH))
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    
    service = Service('/usr/bin/chromedriver')

    # User Agent Settings
    # chrome_options.add_argument('user-agent=Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36')
    # chrome_options.add_argument("--user-data-dir=/home/joao/.config/google-chrome")
    # chrome_options.add_argument("--profile-directory=Profile 1")
    
    try:
        driver = Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(40)
    except:
        print('Could not open Chrome Driver')
        return

    # Not sure what are the impacts. Maybe some cloaking bypass
    try:
        driver.get('https://www.google.com')
        time.sleep(1)
    except Exception as e:
        print('Could not open Google')
        driver.quit()
        return

    time.sleep(1)
    
    # Open the URL in the Selenium Driver
    try:
        driver.get(url)
        time.sleep(5)
    except:
        print('Could not open URL')
        driver.quit()

    # Bypass alerts
    try:
        while True:
            driver.switch_to.alert.text
            driver.switch_to.alert.accept()
            time.sleep(1)
    except:
        print('Error handling alerts')
        pass

    driver.quit()

    return True

@processing_bp.route('/check_url_network_status', methods=['POST'])
def check_url_network_status():
    url = request.json['url']

    network_status = check_network_status(url)
    
    url_obj = Urls.objects.get(url=url)

    if url_obj is not None:
        url_obj.network_status = network_status
        url_obj.last_update_dt = datetime.now()
        url_obj.save()
    else:
        url_obj = Urls(**{
            'url': url,
            'added_dt': datetime.now(),
            'last_update_dt': datetime.now(),
            'source': "MANUAL"
        })
        url_obj.save()
    
    return jsonify({'network_status': network_status, 'message': 'Network status succesfully checked'}), 200

@processing_bp.route('/check_database_network_status', methods=['POST'])
def check_database_network_status():
    urls = Urls.objects(network_status=None)

    updated_urls_count = 0

    for url in urls:
        updated_urls_count += 1
        network_status = check_network_status(url.url)
        url.network_status = network_status
        url.last_update_dt = datetime.now()
        url.save()

    return jsonify({'message': 'Network Status Updated', 'updated_urls_count': updated_urls_count}), 200

@processing_bp.route('/callback_check_url_redirections', methods=['POST'])
def callback_check_url_redirections():
    hops = request.json['hops']

    main_url = hops[0]['url']
    print(f'Processing Redirections for {main_url}')

    try:
        url_obj = Urls.objects.get(url=main_url)
        url_obj.last_update_dt = datetime.now()
    except Urls.DoesNotExist:
        url_obj = Urls(**{
            'url': main_url,
            'added_dt': datetime.now(),
            'last_update_dt': datetime.now(),
            'source': "MANUAL"
        })
    url_obj.save()

    try:
        redirections_obj = Redirections.objects.get(url=main_url)
        redirections_obj.last_update_dt = datetime.now()
        redirections_obj.hops_amount = len(hops)
    except Redirections.DoesNotExist:
        redirections_obj = Redirections(**{
            'url': main_url,
            'last_update_dt': datetime.now(),
            'hops_amount': len(hops)
        })
    
    redirections_obj.save()
    
    return jsonify({'message': f'Updated Redirections for {main_url}'}), 200

@processing_bp.route('/check_url_redirections', methods=['POST'])
def check_url_redirections():
    url = request.json['url']

    try:
        url_obj = Urls.objects.get(url=url)
    except Urls.DoesNotExist:
        url_obj = Urls(**{
            'url': url,
            'added_dt': datetime.now(),
            'last_update_dt': datetime.now(),
            'source': "MANUAL"
        })
        url_obj.save()

    try:
        crawl_searching_redirections(url)
    except:
        return jsonify({'message': 'Error triggering crawl procedure'}), 500
        
    return jsonify({'message': 'Crawling Procedure Triggered'}), 200    

@processing_bp.route('/check_database_redirections', methods=['POST'])
def check_database_redirections():
    urls = [url.url for url in Urls.objects(source='COMMONCRAWL', network_status='ONLINE')]

    # Multiprocessing Version
    num_proc = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_proc * 2)
    pool.map(crawl_searching_redirections, urls)

    # Sequential Version
    # for url in urls:
        # crawl_searching_redirections(url)

    return jsonify({'message': 'Redirections Checked', 'urls_count': len(urls)}), 200
