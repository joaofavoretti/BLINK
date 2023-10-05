# /app/views/urls.py

from flask import Blueprint, jsonify, request
from app.models import Urls
from mongoengine import Q

urls_bp = Blueprint('urls', __name__, url_prefix='/urls')

@urls_bp.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    url = Urls(**data)
    url.save()
    return jsonify(data)

@urls_bp.route('/save_from_url', methods=['POST'])
def save_from_url():
    req_json = request.get_json()
    url = req_json['url']
    data = Urls(**{
        'url': url,
        'online': True,
        'phishtank_inspection': None,
        'gsb_inspection': None,
        'manual_inspection': None
    })
    data.save()
    return jsonify(data)

@urls_bp.route('/save_from_phishtank', methods=['POST'])
def save_from_phishtank():
    req_json = request.get_json()
    url = req_json['url']
    data = Urls(**{
        'url': url,
        'online': True,
        'phishtank_inspection': {
            'triggered': True,
        },
        'gsb_inspection': None,
        'manual_inspection': None
    })
    data.save()
    return jsonify(data)

@urls_bp.route('/get', methods=['GET'])
def get():
    print('asdf')
    urls = Urls.objects()
    return jsonify(urls)

@urls_bp.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    url = Urls.objects.get(id=data['id'])
    url.update(**data)
    return jsonify(data)

@urls_bp.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    url = Urls.objects.get(id=data['id'])
    url.delete()
    return jsonify(data)

@urls_bp.route('/save_triggered', methods=['POST'])
def get_triggered():
    documents = Urls.objects.filter(Q(manual_inspection__triggered=True) & Q(phishtank_inspection=None))
    with open('commoncrawl_suspicious.txt', 'w') as f:
        for document in documents:
            f.write(document.url + '\n')

    return jsonify({
        'saved': len(documents)
    })