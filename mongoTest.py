from pymongo import MongoClient

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)
try:
    db = client.get_database("data")
    countries = db.get_collection("countries")
    res = countries.find({"name": {"$eq": "Germany"}}, {"name": 1})
    res = countries.find({}, {"name": 1})
    names = [c["name"] for c in res]
    print(res)
    print(names)
    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)