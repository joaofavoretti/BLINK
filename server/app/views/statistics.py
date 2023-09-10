# /app/views/statistics.py

from flask import Blueprint, jsonify, request
from app.models import Urls
from mongoengine import Q

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')

@statistics_bp.route('/amount_validated', methods=['GET'])
def amount_validated():
    """
    Get the amount of validated URLs.
    """
    # Documents with manual_inspection == True or online == False
    documents = Urls.objects.filter(Q(manual_inspection__ne=None) | Q(online=False))
    return jsonify({
        'amount': len(documents),
        'total': len(Urls.objects.all())
    })

@statistics_bp.route('/amount_online', methods=['GET'])
def amount_online():
    """
    Get the amount of online URLs.
    """
    documents_online = Urls.objects.filter(Q(online=True) & Q(manual_inspection__ne=None))
    document_offline = Urls.objects.filter(online=False)
    return jsonify({
        'onlineAmount': len(documents_online),
        'offlineAmount': len(document_offline),
        'total': len(documents_online) + len(document_offline)
    })

@statistics_bp.route('/confidence', methods=['GET'])
def confidence():
    """
    Get the confidence of the model.
    """
    # Documents with phishtank_inspeciton != None and manual_inspection.triggered == True
    documents_found = Urls.objects.filter(Q(phishtank_inspection__ne=None) & Q(manual_inspection__triggered=True))
    documents_not_found = Urls.objects.filter(Q(phishtank_inspection__ne=None) & Q(manual_inspection__triggered=False))
    return jsonify({
        'found': len(documents_found),
        'notFound': len(documents_not_found),
        'total': len(documents_found) + len(documents_not_found)
    })

@statistics_bp.route('/save', methods=['POST'])
def save():
    documents = Urls.objects.filter(Q(manual_inspection__triggered=False) & Q(phishtank_inspection=None) & Q(online=True))
    with open('verified.txt', 'w') as f:
        for document in documents:
            f.write(document.url + '\n')

    return jsonify({
        'saved': len(documents)
    })
        