from .. import db

class UrlsClothingCategory(db.Document):
    # URL Label: String Field to contain the Label of the Document
    label = db.StringField(required=True, unique=True)

    meta = {
        'collection': 'urls_clothing_category',
    }