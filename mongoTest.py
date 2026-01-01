from pymongo import MongoClient

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)
try:
    database = client.get_database("data")
    movies = database.get_collection("collection")
    movie = movies.find_one({  })
    print(movie)
    client.close()
except Exception as e:
    raise Exception("Unable to find the document due to the following error: ", e)

