from .. import db

class CommoncrawlUsedSources(db.Document):

    file = db.StringField(required=True)    

    meta = {
        'collection': 'commoncrawl_used_sources',
    }