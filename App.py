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
markdown_text = '''
# Some references
@@ -9,11 +14,17 @@
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/)
- [Dash DataTable](https://dash.plotly.com/datatable)
'''

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
        return [
            html.H1('Intructions'
                    )
        ]
    elif pathname == "/page-1":
        return [
            dcc.Tabs([
                dcc.Tab(label='Table', children=[
                     html.H1("NBA dataset"),
                     dcc.Markdown(markdown_text),
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
                    html.Label(["Range of values for body weight:",
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
            html.P(f"The pathname {pathname} was not recognised..."),
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
    return px.scatter(flt, x="PTS", y="MP", color="Pos", hover_data=['Tm'])


@app.callback(
    Output('selected_data_table', 'children'),
    Input('graph', 'selectedData'))
def display_selected_data(selectedData):
    if selectedData is None:
        return None
    names = [o['customdata'][0] for o in selectedData['points']]
    table = dash_table.DataTable(columns=[{"name": i, "id": i} for i in df.columns], 
            data=df[df['Tm'].isin(names)].to_dict('records'))
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
