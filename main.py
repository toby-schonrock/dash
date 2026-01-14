import pandas as pd
from dash import Dash, callback, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_mantine_components as dmc

from pymongo import MongoClient

from insertFromCSV import insertFromCsv

uri = "mongodb://localhost:27017/?directConnection=true"
mongoClient = MongoClient(uri)
if "data" not in mongoClient.list_database_names():
    raise RuntimeError("Couldn't retrieve data db")
db = mongoClient["data"]

if "countries" not in db.list_collection_names():
    raise RuntimeError("Couldn't retrieve data db")
countriesCol = db["countries"]


def getCountryNames() -> pd.Series:
    countryNames = pd.DataFrame(countriesCol.find({}, {"name": 1}))
    if len(countryNames.index) > 0:
        return countryNames["name"]
    return pd.Series()


app = Dash()


def paper(children: any, **kwargs) -> dmc.Paper:
    kwargs.setdefault('m', "md")
    kwargs.setdefault('p', "md")
    return dmc.Paper(children=children, radius="sm", shadow="md", withBorder=True, **kwargs)


optionsMenu = paper([
    dmc.MultiSelect(
        data=getCountryNames(),
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
    ), mx=0),
    dmc.Button("Refresh data from csv", variant="subtle", id="refresh-button")
], mt=0)

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
    dmc.Title('Country stats', style={'textAlign': 'center'}, order=2, m="lg"),
    dmc.Grid(
        children=[
            dmc.GridCol(optionsMenu, span=4, p="md"),
            dmc.GridCol(graph, span=8, p="md")
        ],
        mx="lg",
        align="flex-start"
    )
], forceColorScheme="dark")

seriesColors = ["lime.5", "cyan.5", "blue.5", "red.6", "orange.6", "yellow.5"]


@callback(
    Output('graph', 'data'),
    Output('graph', 'series'),
    Output('graph', 'yAxisLabel'),
    Input('country-select', 'value'),
    Input('key-radio', 'value')
)
def updateGraph(countries: list[str], key: str):
    if len(countries) == 0:
        return [[], [], ""]

    res = countriesCol.find({"name": {"$in": countries}},
                            {"name": 1, "data": 1})
    dfs = [(c["name"], pd.DataFrame(c["data"]))
           for c in res]  # get country data as dfs

    # remove countries which were not found
    countries = [name for name, df in dfs if name in countries]

    dfs = [df.rename(columns={key: name})[["year", name]]
           for name, df in dfs]  # rename key to country

    data = pd.DataFrame(columns=["year"])  # join dfs into a single df
    for df in dfs:
        data = pd.merge(data, df, on="year",
                        how="outer", copy=False)

    series = [{
        "name": country,
        "color": seriesColors[i % len(seriesColors)]
    } for i, country in enumerate(countries)]  # make series with colours
    return [data.to_dict(orient="records"), series, key]


@callback(
    Output('country-select', 'data'),
    Input('refresh-button', 'n_clicks'),
    prevent_initial_call=True
)
def loadFromCsv(n_clicks):
    insertFromCsv(mongoClient)
    countryNames = getCountryNames()
    return countryNames


if __name__ == '__main__':
    app.run(debug=True)
