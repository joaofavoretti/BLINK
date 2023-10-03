import pymongo

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Get a reference to the database
db = client["mydatabase"]

# Get a reference to the collection
collection = db["mycollection"]

# Insert a document into the collection
# document = {"name": "John", "age": 30}
# result = collection.insert_one(document)

# Find documents in the collection
query = {"name": "John"}
results = collection.find(query)

for result in results:
    print(result)
