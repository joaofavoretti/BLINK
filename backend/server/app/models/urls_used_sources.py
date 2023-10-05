from .. import db

class UrlsUsedSources(db.Document):

    source = db.StringField(required=True)
    file = db.StringField(required=True)    

    meta = {
        'collection': 'urls_used_sources',
    }