from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import Urls
from app.models import UrlsUsedSources
from mongoengine import Q
import requests
import warc
import os

urls_bp = Blueprint('urls', __name__, url_prefix='/urls')

@urls_bp.route('/', methods=['GET'])
def get_urls():
    urls = Urls.objects().limit(200)

    formated_urls = [
        {
            "id": str(url.id),
            "url": url.url,
            "added_dt": str(url.added_dt),
            "classification": url.classification,
            "network_status": url.network_status,
            "last_update_dt": str(url.last_update_dt),
            "content_category": url.content_category if url.content_category else None,
        } for url in urls
    ]

    return jsonify(formated_urls), 200

# Change the endpoint names and maybe use a separate controller 
#   and api to make those manipulations on commoncrawl files and urls
@urls_bp.route('/available_commoncrawl_files', methods=['GET'])
def get_available_commoncrawl_files():
    AVAILABLE_PATHS = 'files/warc.paths'

    # Filter by attribute "source" == 'COMMONCRAWL
    used_sources = UrlsUsedSources.objects.filter(Q(source='COMMONCRAWL'))
    used_sources = set([os.path.basename(source.file) for source in used_sources])

    amount = request.args.get('amount')
    if amount is None:
        amount = 10
    else:
        amount = int(amount)

    with open(AVAILABLE_PATHS, 'r') as f:
        paths = f.readlines()

    fnames = [os.path.basename(path.strip()[:-3]) for path in paths if os.path.basename(path.strip()[:-3]) not in used_sources][-amount:]

    return jsonify({'available_fnames': fnames}), 200

@urls_bp.route('/add_commoncrawl_urls', methods=['POST'])
def add_commoncrawl_urls():
    AVAILABLE_PATHS = 'files/warc.paths'
    BASE_DOWNLOAD_URL = 'https://data.commoncrawl.org'
    FILES_DIR = './files'
    
    files = request.json['files']
    
    used_sources = UrlsUsedSources.objects.filter(Q(source='COMMONCRAWL'))
    used_sources = set([os.path.basename(source.file) for source in used_sources])

    # Verify if it was not already added
    files = [file for file in files if os.path.basename(file) not in used_sources]

    with open(AVAILABLE_PATHS, 'r') as f:
        paths = f.readlines()

    fpaths = [path.strip() for path in paths if os.path.basename(path.strip()[:-3]) in files]

    fname_count = 0

    for fpath in fpaths:
        used_url_obj = UrlsUsedSources(source='COMMONCRAWL', file=os.path.basename(fpath[:-3]))
        used_url_obj.save()

        url = f'{BASE_DOWNLOAD_URL}/{fpath}'
        fname = os.path.basename(fpath[:-3])
        print(f'Processing {fname}')
        print(f'Downloading {url}')
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            print(f'Saving content at {FILES_DIR}/{fname}.gz')
            with open(f'{FILES_DIR}/{fname}.gz', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
        else:
            print(f'Error downloading {fname}')
            continue

        # gzip decompress the file .gz
        print(f'Decompressing {FILES_DIR}/{fname}.gz')
        os.system(f'gzip -d {FILES_DIR}/{fname}.gz')

        with warc.open(f'{FILES_DIR}/{fname}') as f:
            for record in f:
                print(f'Current count: {fname_count}', end='                                   \r')

                if 'WARC-Target-URI' not in record:
                    continue

                # Search if the URL already exists
                # TODO: For optimizations, maybe make that search on the RAM instead of the database
                url_document = Urls.objects(url=record['WARC-Target-URI']).first()

                if url_document:
                    continue

                fname_count += 1

                url_dict = {
                    "url": record['WARC-Target-URI'],
                    "network_status": 'ONLINE',
                    "classification": 'BENIGN',
                    "added_dt": datetime.now(),
                    "last_update_dt": datetime.now(),
                    "content_category": None,
                    "source": "COMMONCRAWL"
                }

                url = Urls(**url_dict)
                url.save()
        
        # Remove the file
        os.system(f'rm {FILES_DIR}/{fname}')

    return jsonify({'message': 'URLs added successfully', 'included_file_count': fname_count}), 200