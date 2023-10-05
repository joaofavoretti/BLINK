from .. import db

class Urls(db.Document):
    # URL Field: String Field to contain the URL of the Document
    url = db.StringField(required=True, unique=True)

    # Network Status Field: Boolean Field to contain true if the URL is online, false if it is offline or null if it has not been checked
    network_status = db.BooleanField(choices=['ONLINE', 'OFFLINE', None], default=None)

    # Classification: String Field to contain the classification of the URL. It can only be fields that are on the "urls_classifications" collection
    classification = db.StringField(default=None)

    # Added Date: DateTime Field to contain the date when the URL was added to the database
    added_dt = db.DateTimeField(required=True)

    # Last Update: DateTime Field to contain the date when the URL was last updated
    last_update_dt = db.DateTimeField(required=True)
    
    # Content Category: String Field to contain the category of the content of the URL. It can only be fields that are on the "urls_content_category" collection
    content_category = db.StringField(default=None)

    # Source: String Field to contain the source of the URL. It can only be fields that are on the "urls_sources" collection
    source = db.StringField(default=None)

    meta = {
        'collection': 'urls',
    }