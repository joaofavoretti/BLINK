from .. import db

class Redirections(db.Document):
    # URL Field: String Field to contain the URL of the Document
    url = db.StringField(required=True, unique=True)

    last_update_dt = db.DateTimeField(required=True)

    hops_amount = db.IntField(required=True)

    meta = {
        'collection': 'redirections'
    }