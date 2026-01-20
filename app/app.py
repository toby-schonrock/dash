import os
import pandas as pd
from dash import Dash, callback, clientside_callback, ClientsideFunction, Output, Input, State, dcc, html
import dash_mantine_components as dmc

import database as db


def paper(children: any, **kwargs) -> dmc.Paper:
    kwargs.setdefault('m', "md")
    kwargs.setdefault('p', "md")
    return dmc.Paper(children=children, radius="sm", shadow="md", withBorder=True, **kwargs)


def createLayout() -> dmc.MantineProvider:
    optionsMenu = paper([
        dmc.MultiSelect(
            data=db.getCountryNames(),
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
            value='pop',
            size="sm"
        ), mx=0),
        dmc.Group([
            dmc.Button("Reload db from csv",
                       variant="subtle", id="reload-button"),
            dmc.Button("Delete selected countries from db",
                       variant="light", id="delete-button", color="red")
        ], justify="space-around")
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

    return dmc.MantineProvider([
        dcc.Location(id='url', refresh=False),
        html.Div(id='output-sink', style={'display': 'none'}),
        dmc.Title('Country stats', style={
                  'textAlign': 'center'}, order=2, m="lg"),
        dmc.Grid(
            children=[
                dmc.GridCol(optionsMenu, span=4, p="md"),
                dmc.GridCol(graph, span=8, p="md")
            ],
            mx="lg",
            align="flex-start"
        )
    ], forceColorScheme="dark")


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

    res = db.getCountries(countries, ["name", "data"])
    dfs = [(c["name"], pd.DataFrame(c["data"]))
           for c in res]  # get country data as dfs

    # remove countries which were not found
    countries = [name for name, _ in dfs if name in countries]

    dfs = [df.rename(columns={key: name})[["year", name]]
           for name, df in dfs]  # rename key to country

    data = pd.DataFrame(columns=["year"])  # join dfs into a single df
    for df in dfs:
        data = pd.merge(data, df, on="year",
                        how="outer", copy=False)

    seriesColors = ["lime.5", "cyan.5", "blue.5",
                    "red.6", "orange.6", "yellow.5"]

    series = [{
        "name": country,
        "color": seriesColors[i % len(seriesColors)]
    } for i, country in enumerate(countries)]  # make series with colours
    return [data.to_dict(orient="records"), series, key]


@callback(
    Output('country-select', 'data'),
    Input('reload-button', 'n_clicks'),
    prevent_initial_call=True
)
def loadFromCsv(n_clicks: int):
    db.loadFromCsv()
    return db.getCountryNames()


@callback(
    Output('country-select', 'data', allow_duplicate=True),
    Input('delete-button', 'n_clicks'),
    State('country-select', 'value'),
    prevent_initial_call=True
)
def deleteCountries(n_clicks: int, countries: list[str]):
    db.deleteCountries(countries)
    return db.getCountryNames()


clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='fixCountrySelections'
    ),
    Output('country-select', 'value', allow_duplicate=True),
    Input('country-select', 'data'),
    State('country-select', 'value'),
    prevent_initial_call=True
)


clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='updateURLFromInputs'
    ),
    # prevents dash from duplicating history
    Output('output-sink', 'children'),
    Input('key-radio', 'value'),
    Input('country-select', 'value')
)


clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='updateInputsFromURL'
    ),
    Output('key-radio', 'value'),
    Output('country-select', 'value'),
    Input('url', 'search')
)


BASE_PATH = os.getenv("BASE_PATH", "") + "/"
app = Dash(requests_pathname_prefix=BASE_PATH,
           routes_pathname_prefix=BASE_PATH)
app.layout = createLayout()
server = app.server  # global for gunicorn

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
