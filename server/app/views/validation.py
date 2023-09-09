# /app/views/urls.py

from flask import Blueprint, jsonify, request
from app.models import Urls

validation_bp = Blueprint('validation', __name__, url_prefix='/validation')

@validation_bp.route('/get_list', methods=['GET'])
def get_all():
    documents = Urls.objects.all()
    urls = []
    for document in documents:
        url = {
            'id': str(document.id),
            'url': document.url,
            'online': document.online,
            'validated': True if document.manual_inspection else False
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