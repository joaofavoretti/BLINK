from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import Urls
from mongoengine import Q
import json

urls_bp = Blueprint('urls', __name__, url_prefix='/urls')

# Temporary route to save data from /home/joao/my/projects/url-analyser/backup/phishing.urls.json
@urls_bp.route('/import_data', methods=['POST'])
def import_data():
    fpath = '/home/joao/my/projects/url-analyser/backup/phishing.urls.json'
    
    with open(fpath, 'r') as f:
        data = json.load(f)
    
    insertion_counter = 0

    for url in data:
        insertion_counter += 1

        url_classification = None
        
        url_added_dt = datetime.now()

        url_last_update_dt = datetime.now()

        url_content_category = None

        url_source = None

        args = {
            'url': url['url'],
            'network_status': 'ONLINE' if url['online'] else 'OFFLINE',
            'classification': url_classification,
            'added_dt': url_added_dt,
            'last_update_dt': url_last_update_dt,
            'content_category': url_content_category,
            'source': url_source
        }

        url = Urls(**args)
        url.save()

    return jsonify({
        'insertion_counter': insertion_counter
    })

@urls_bp.route('/get-category', methods=['GET']):
def get_category():
    # Filter
    urls = Urls.objects()
    return jsonify(urls)