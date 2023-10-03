from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/phishing'
mongo = PyMongo(app)

@app.route('/urls', methods=['POST'])
def create_user():

    print(request.json)

    if request.json['url'] is not None:
        mongo.db.urls.insert_one(request.json)

    return {'message': 'received'}


if __name__ == '__main__':
    app.run(debug=True)