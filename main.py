import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import dash_mantine_components as dmc

from pymongo import MongoClient

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)
if "data" not in client.list_database_names():
    raise RuntimeError("Couldn't retrieve data db")
db = client["data"]

if "countries" not in db.list_collection_names():
    raise RuntimeError("Couldn't retrieve data db")
countries = db["countries"]

countryNames = pd.DataFrame(countries.find({}, {"name": 1}))["name"]
if len(countryNames) == 0:
    raise RuntimeError("Couldn't retrieve countryNames")

app = Dash()

app.layout = dmc.MantineProvider([
    html.H1(children='Country stats', style={'textAlign':'center'}),
    dcc.Dropdown(countryNames, 'Canada', id='select-country'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('select-country', 'value')
)
def update_graph(value):
    res = pd.DataFrame.from_dict(countries.find_one({"name": {"$eq": value}}, {"data": 1})["data"])
    return px.line({"pop": res["pop"], "year": res["year"]}, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=False)
