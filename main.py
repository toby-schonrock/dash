import pandas as pd
from dash import Dash, ClientsideFunction, clientside_callback, callback, Output, Input
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

def paper(children, **kwargs):
    kwargs.setdefault('m', "md")
    kwargs.setdefault('p', "md")
    return dmc.Paper(children=children, radius="sm", shadow="md", withBorder=True, **kwargs)

optionsMenu = paper([
    dmc.Select(data=countryNames, value='Canada', id='country-select'),
    paper(dmc.RadioGroup(
        id="key-radio",
        children=dmc.Group([
            dmc.Radio("life expectancy", value="lifeExp"), 
            dmc.Radio("population", value="pop"), 
            dmc.Radio("gdp per capita", value="gdpPercap"), 
        ]),
        value="pop",
        size="sm"
    ), mx = 0)
], mt = 0)

graph = dmc.LineChart(id='graph',
    h=300,
    data=[{}],
    dataKey="year",
    xAxisLabel="year",
    series=[],
    tooltipAnimationDuration=50,
    valueFormatter={"function": "numberFormatter"}
)

app.layout = dmc.MantineProvider([
    dmc.Title('Country stats', style={'textAlign':'center'}, order=2, m="md"),
    dmc.Grid(
        children = [
            dmc.GridCol(optionsMenu, span=4, p="md"),
            dmc.GridCol(graph, span=8, p="md")
        ],
        mx="lg",
        align="flex-start"
    )
], forceColorScheme="dark")

@callback(
    Output('graph', 'data'),
    Input('country-select', 'value')
)
def updateGraphCountry(value):
    if not value: return None
    res = countries.find_one({"name": {"$eq": value}}, {"data": 1})["data"]
    return res

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='updateGraphKey'),
    Output('graph', 'series'),
    Output('graph', 'yAxisLabel'),
    Input('key-radio', 'value')
)

if __name__ == '__main__':
    app.run(debug=False)
