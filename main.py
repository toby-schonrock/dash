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

def paper(children):
    return dmc.Paper(children=children, radius="sm", p="md", shadow="md", withBorder=True)

app.layout = dmc.MantineProvider([
    dmc.Title('Country stats', style={'textAlign':'center'}, order=2, m="md"),
    dmc.Grid(
        children = [
            dmc.GridCol(paper(dmc.Select(data=countryNames, value='Canada', id='select-country')), span=3, p=20),
            dmc.GridCol(
                dmc.LineChart(id='graph',
                    h=300,
                    data=[{}], 
                    dataKey="year", 
                    xAxisLabel="year",
                    series=[{"name": "pop"}],
                    yAxisLabel="pop",
                    tooltipAnimationDuration=50,
                    valueFormatter={"function": "sciNotaFormatter"}
                    ),
                span=9, p=20)
        ],
        mx=50,
        align="flex-start"
    )
], forceColorScheme="dark")

@callback(
    Output('graph', 'data'),
    Input('select-country', 'value')
)
def update_graph(value):
    if not value: return None 
    res = countries.find_one({"name": {"$eq": value}}, {"data": 1})["data"]
    # print(res)
    return res

if __name__ == '__main__':
    app.run(debug=False)
