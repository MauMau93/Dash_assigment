import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_table
import pandas as pd
import numpy as np
import json

from dash.dependencies import Input, Output, State
app = dash.Dash(__name__, title="2021 Dash Python App",
                external_stylesheets=[dbc.themes.CERULEAN])

df_url = 'https://raw.githubusercontent.com/JavierEA1/nbadataset/main/DatosNBA.csv'
df = pd.read_csv(df_url, sep=';')

df_url2 = 'https://raw.githubusercontent.com/MauMau93/data_diabetes/main/data_diabetes.csv'
df2 = pd.read_csv(df_url2, sep=',')


df_Pos = df['Pos'].dropna().sort_values().unique()
opt_Pos = [{'label': x, 'value': x} for x in df_Pos]
df_Tm = df['Tm'].dropna().sort_values().unique()
opt_Tm = [{'label': x, 'value': x} for x in df_Tm]
df_Outcome = df2['Outcome'].dropna().sort_values().unique()
opt_Outcome = [{'label': x, 'value': x} for x in df_Outcome]


col_Pos = {x: px.colors.qualitative.G10[i] for i, x in enumerate(df_Pos)}
col_Outcome = {x: px.colors.qualitative.G10[i]
               for i, x in enumerate(df_Outcome)}

min_pts = min(df['PTS'].dropna())
max_pts = max(df['PTS'].dropna())


table_tab = dash_table.DataTable(
    id='my-table2',
    columns=[{"name": i, "id": i} for i in df2.columns],
    data=df2.to_dict("records")
)
graph_tab = html.Div([
    dcc.Graph(id="graph2"

              )
])

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "Select data", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("NBA", href="/page-1", active="exact"),
                dbc.NavLink("Diabetes", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],

)
content = html.Div(id="page-content", children=[])
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(id='data', style={'display': 'none'}),
    content
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H1("Instruction"),
            html.P(["Welcome to this Dash app"]),
            html.P(["Here you will find two panels: one for the diabetes dataset and the second one regarding NBA dataset."]),
            html.P(["In the NBA panel, you will have the opportunity to explore the different players and their charateristics. Firstly, you will be able to filter for Player Position and team, and you will visualize the data in a table. Also, you have the opportunity to choose to look at a plot, of this datapoints in two axes: MP and PTS. In this plot, you have the option to filter for a specific interval of points per match (in average). Please note that the plot is interactive, so you can see the information of every point when moving the pointer. You can also select with lasso as many points as you want and take a closer look at their information in a table on the bottom part of the page"]),
            html.P(["Then, you have the panel for the diabetes dataset. First you can see a table with the information of each datapoint, where you can filter to see the people that has diabetes and the people that does not have diabetes ("0" for those who don´t have diabetes and "1" for those who do have it). You also have the chance to check at a plot of Blood Preassure against Glucose, and again you can choose between the people who has and does not have diabetes. Please note that, again, this plot is also interactive, so you can see the information of each datapoint when going through it with your mousse."]),
            html.P(["This is the glosary for the NBA dataset abreviattions: The significance of the abrevations are: C--Center F--Foward G--Guard Rk -- Rank Pos -- Position Age -- Player's age on February 1 of the season Tm -- Team G -- Games GS -- Games Started MP -- Minutes Played Per Game FG -- Field Goals Per Game FGA -- Field Goal Attempts Per Game FG% -- Field Goal Percentage 3P -- 3-Point Field Goals Per Game 3PA -- 3-Point Field Goal Attempts Per Game 3P% -- 3-Point Field Goal Percentage 2P -- 2-Point Field Goals Per Game 2PA -- 2-Point Field Goal Attempts Per Game 2P% -- 2-Point Field Goal Percentage eFG% -- Effective Field Goal Percentage This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal. FT -- Free Throws Per Game FTA -- Free Throw Attempts Per Game FT% -- Free Throw Percentage ORB -- Offensive Rebounds Per Game DRB -- Defensive Rebounds Per Game TRB -- Total Rebounds Per Game AST -- Assists Per Game STL -- Steals Per Game BLK -- Blocks Per Game TOV -- Turnovers Per Game PF -- Personal Fouls Per Game PTS -- Points Per Game"]),


        ])
    elif pathname == "/page-1":
        return [
            dcc.Tabs([
                dcc.Tab(label='Table', children=[
                     html.H1("NBA dataset"),
                     html.Label(["Select Position of the player",
                                 dcc.Dropdown(
                                     'mydropdown', options=opt_Pos, value=opt_Pos[0]['value'])
                                 ]),
                     html.Label(["Select Team of the player",
                                 dcc.Dropdown('mydropdown2', options=opt_Tm,
                                              value=opt_Tm[0]['value'], multi=True)
                                 ]),
                     dash_table.DataTable(

                         id='my-table',
                         columns=[{"name": i, "id": i} for i in df.columns],
                         data=df.to_dict("records")
                     )
                     ]
                ),
                dcc.Tab(label='Plot', children=[
                    html.Label(["Range of values for point per match (average):",
                                dcc.RangeSlider(id="rangeSlider",
                                                max=40,
                                                min=0,
                                                step=1,
                                                marks={m: m for m in [
                                                    x for x in range(41) if x % 5 == 0]},
                                                value=[0, 40]
                                                )
                                ]),
                    dcc.Graph(id="graph"),
                    html.Div(id='selected_data_table')
                ])
            ])
        ]
    elif pathname == "/page-2":
        return [
            html.Label(["Select diabetes or not:",
                        dcc.Dropdown('my-dropdown3', options=opt_Outcome,
                                     value=[opt_Outcome[0]['value']])
                        ]),
            html.H1('Diabetes'),

            dcc.Tabs(id="tabs", value='tab-t', children=[
                dcc.Tab(label='Table', value='tab-t'),
                dcc.Tab(label='Graph', value='tab-g'),
            ]),
            html.Div(id='tabs-content')
        ]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...")
        ]
    )


@app.callback(
    Output('my-table', 'data'),
    Input('mydropdown', 'value'),
    Input('mydropdown2', 'value'))
def update_data(mydropdown, mydropdown2):
    if type(mydropdown2) == type([]):
        filter = df[(df['Pos'] == mydropdown) & (df['Tm'].isin(mydropdown2))]
    else:
        filter = df[(df['Pos'] == mydropdown) & (df['Tm'] == mydropdown2)]
    return filter.to_dict("records")


@app.callback(
    Output('graph', 'figure'),
    Input('rangeSlider', 'value'))
def update_graph(rangeSlider):
    flt = df[(df['PTS'] >= rangeSlider[0])
             & (df['PTS'] <= rangeSlider[1])]
    return px.scatter(flt, x="PTS", y="MP", color="Pos", hover_data=['Player'])


@app.callback(
    Output('selected_data_table', 'children'),
    Input('graph', 'selectedData'))
def display_selected_data(selectedData):
    if selectedData is None:
        return None
    names = [o['customdata'][0] for o in selectedData['points']]
    table = dash_table.DataTable(columns=[{"name": i, "id": i} for i in df.columns], 
            data=df[df['Player'].isin(names)].to_dict('records'))
    return table

@ app.callback(Output('tabs-content', 'children'),
               Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-t':
        return table_tab
    elif tab == 'tab-g':
        return graph_tab


@ app.callback(
    Output('my-table2', 'data'),
    Input('data', 'children'),
    State('tabs', 'value'))
def update_table(data, tab):
    if tab != 'tab-t':
        return None
    dff= pd.read_json(data, orient='split')
    return dff.to_dict("records")


@ app.callback(
    Output('graph2', 'figure'),
    Input('data', 'children'),
    State('tabs', 'value'))
def update_graph2(data, tab):

    df2= pd.read_json(data, orient='split')
    return px.scatter(df2, x="Glucose", y="BloodPressure", color="Outcome",
                      # color_discrete_sequence=px.colors.qualitative.G10
                      color_discrete_map=col_Outcome)


@ app.callback(Output('data', 'children'),
              Input('my-dropdown3', 'value'))
def update(values):
    flr= df2[df2['Outcome'] == values]

    # more generally, this line would be
    # json.dumps(cleaned_df)
    return flr.to_json(date_format='iso', orient='split')


if __name__ == '__main__':
    app.server.run(debug=True)
