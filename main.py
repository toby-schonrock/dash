from dash import Dash, html, dcc, callback, Output, Input
from pymongo import MongoClient
import plotly.express as px

app = Dash()

uri = "mongodb://localhost:27017/?directConnection=true"
client = MongoClient(uri)
db = client.get_database("data")
countries = db.get_collection("countries")

countryNames = [c["name"] for c in countries.find({}, {"name": 1})]
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
    res = countries.find_one({"name": {"$eq": value}}, {"data": 1})
    xs = [d["pop"] for d in res["data"]]
    ys = [d["year"] for d in res["data"]]
    return px.line({"pop": xs, "year": ys}, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=False)
