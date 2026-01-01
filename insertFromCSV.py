import pandas as pd
from pymongo import MongoClient

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)

client.drop_database("data")
db = client["data"]
col = db.create_collection("countries")

df = pd.read_csv('data.csv')
objs = []

for count in df.country.unique():
    dff = df[df.country==count]
    objs.append({"name": count, 
           "continent": dff.loc[dff.index[0], "continent"], 
           "data": dff[["year", "lifeExp", "pop", "gdpPercap"]].to_dict('records')})
    
col.insert_many(objs)