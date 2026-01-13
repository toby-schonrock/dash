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
countriesCol = db["countries"]

countryNames = pd.DataFrame(countriesCol.find({}, {"name": 1}))["name"]
if len(countryNames) == 0:
    raise RuntimeError("Couldn't retrieve countryNames")

app = Dash()

def paper(children, **kwargs):
    kwargs.setdefault('m', "md")
    kwargs.setdefault('p', "md")
    return dmc.Paper(children=children, radius="sm", shadow="md", withBorder=True, **kwargs)

optionsMenu = paper([
    dmc.MultiSelect(
        data=countryNames, 
        value=['Germany'], 
        id='country-select',
        placeholder='search',
        searchable=True,
        clearable=True
    ),
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
    data=[],
    dataKey="year",
    xAxisLabel="year",
    withLegend=True,
    series=[],
    tooltipAnimationDuration=50,
    valueFormatter={"function": "numberFormatter"}
)

app.layout = dmc.MantineProvider([
    dmc.Title('Country stats', style={'textAlign':'center'}, order=2, m="lg"),
    dmc.Grid(
        children = [
            dmc.GridCol(optionsMenu, span=4, p="md"),
            dmc.GridCol(graph, span=8, p="md")
        ],
        mx="lg",
        align="flex-start"
    )
], forceColorScheme="dark")

seriesColors = ["lime.5","cyan.5","blue.5","red.6","orange.6","yellow.5"]

@callback(
    Output('graph', 'data'),
    Output('graph', 'series'),
    Output('graph', 'yAxisLabel'),
    Input('country-select', 'value'),
    Input('key-radio', 'value')
)
def updateGraph(countries, key):
    if len(countries) == 0: return [[], [], ""]
    res = countriesCol.find({"name": {"$in": countries}}, {"name" : 1, "data" : 1})

    dfs = [pd.DataFrame(c["data"])[["year", key]].rename(columns={key:c["name"]}) for c in res]
    data = pd.DataFrame(columns=["year"])
    for df in dfs: data = pd.merge(data, df, on="year", how="outer", copy=False) ## join all countrys
    
    series = [{"name": country, "color" : seriesColors[i % len(seriesColors)]} for i, country in enumerate(countries)]
    return [data.to_dict(orient="records"), series, key]

if __name__ == '__main__':
    app.run(debug=False)
