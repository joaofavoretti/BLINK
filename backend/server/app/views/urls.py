from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import Urls
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
