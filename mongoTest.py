from pymongo import MongoClient

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)
try:
    db = client.get_database("data")
    countries = db.get_collection("countries")
    germ = countries.find_one({"name": {"$eq": "Germany"}})
    print(germ)
    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)