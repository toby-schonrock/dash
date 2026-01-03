from dash import Dash, html, dcc, callback, Output, Input
from pymongo import MongoClient
import plotly.express as px

app = Dash()

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)
db = client.get_database("data")
countries = db.get_collection("countries")

countryNames = [c["name"] for c in countries.find({}, {"name": 1})]

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(countryNames, 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    res = countries.find_one({"name": {"$eq": value}}, {"data": 1})
    xs = [d["pop"] for d in res["data"]]
    ys = [d["year"] for d in res["data"]]
    # print(xs)
    return px.line({"pop": xs, "year": ys}, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=False)
