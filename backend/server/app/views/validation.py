# /app/views/validation.py

from flask import Blueprint, jsonify, request
from app.models import Urls
from mongoengine import Q

validation_bp = Blueprint('validation', __name__, url_prefix='/validation')

@validation_bp.route('/get_list', methods=['GET'])
def get_all():
    documents = Urls.objects.all()
    # documents = Urls.objects.filter(Q(manual_inspection__triggered=True) & Q(phishtank_inspection=None) & Q(online=True))
    urls = []
    for document in documents:
        validated = True if document.manual_inspection else False
        # validated = document.manual_inspection and document.manual_inspection.get('comments')
        url = {
            'id': str(document.id),
            'url': document.url,
            'online': document.online,
            'validated': validated
        }
        urls.append(url)
    return jsonify(urls)

@validation_bp.route('/get_document/<string:id>', methods=['GET'])
def get_document(id):
    """
    Get a single document by ID.
    """
    document = Urls.objects.get(id=id)
    if document:
        return jsonify(document)
    else:
        return jsonify({'error': 'Document not found'})

@validation_bp.route('/get_next_document/<string:id>', methods=['GET'])
def get_next_document(id):
    """
    Get the next document ID.
    """
    document = Urls.objects.get(id=id)
    if document:
        next_document = Urls.objects.filter(id__gt=id).first()
        # next_document = Urls.objects.filter(Q(id__gt=id) & Q(online=True) & Q(manual_inspection__triggered=True) & Q(phishtank_inspection=None)).first()
        if next_document:
            return jsonify({'id': str(next_document.id)})
        else:
            return jsonify({'error': 'No next document'})
    else:
        return jsonify({'error': 'Document not found'})

@validation_bp.route('/update_document/<string:id>', methods=['PUT'])
def update_document(id):
    """
    Update a document by ID.
    """
    document = Urls.objects.get(id=id)
    if document:
        document.online = request.json['online']
        document.manual_inspection = request.json['manual_inspection']
        document.save()
        return jsonify({'message': 'Document updated successfully'})
    else:
        return jsonify({'error': 'Document not found'})