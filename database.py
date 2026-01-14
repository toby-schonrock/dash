import pandas as pd
from pymongo import MongoClient, cursor

uri = "mongodb://localhost:27017/?directConnection=true"
mongoClient = MongoClient(uri)
if "data" not in mongoClient.list_database_names():
    raise RuntimeError("Couldn't retrieve data db")
db = mongoClient["data"]

if "countries" not in db.list_collection_names():
    raise RuntimeError("Couldn't retrieve data db")
countriesCol = db["countries"]

def loadFromCsv():
    mongoClient.drop_database("data")
    db = mongoClient["data"]
    col = db.create_collection("countries")

    df = pd.read_csv('data.csv')
    objs = []

    for count in df.country.unique():
        dff = df[df.country==count]
        objs.append({"name": count, 
            "continent": dff.loc[dff.index[0], "continent"], 
            "data": dff[["year", "lifeExp", "pop", "gdpPercap"]].to_dict('records')})
        
    col.insert_many(objs)

def getCountryNames() -> pd.Series:
    countryNames = pd.DataFrame(countriesCol.find({}, {"name": 1}))
    if len(countryNames.index) > 0:
        return countryNames["name"]
    return pd.Series()

def getCountries(countries: list[str], keys: list[str] = None) -> cursor.Cursor[object]:
    if keys:
        keys = {key: 1 for key in keys}
    return countriesCol.find({"name": {"$in": countries}}, keys)