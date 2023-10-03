from .. import db

class Urls(db.Document):
    url = db.StringField(required=True, unique=True)
    online = db.BooleanField(default=True)
    phishtank_inspection = db.DictField(default=None, null=True)
    gsb_inspection = db.DictField(default=None, null=True)
    manual_inspection = db.DictField(default=None, null=True)

    meta = {
        'collection': 'urls',
    }