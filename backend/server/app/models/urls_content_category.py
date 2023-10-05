from .. import db

class UrlsContentCategory(db.Document):
    # URL Label: String Field to contain the Label of the Document
    label = db.StringField(required=True, unique=True)

    meta = {
        'collection': 'urls_content_category',
    }