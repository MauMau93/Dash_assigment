import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_table
import pandas as pd
import numpy as np

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

df_Pos = df['Pos'].dropna().sort_values().unique()
opt_Pos = [{'label': x, 'value': x} for x in df_Pos]
df_Tm = df['Tm'].dropna().sort_values().unique()
opt_Tm = [{'label': x, 'value': x} for x in df_Tm]

col_Pos = {x: px.colors.qualitative.G10[i] for i, x in enumerate(df_Pos)}

min_pts = min(df['PTS'].dropna())
max_pts = max(df['PTS'].dropna())

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
                                                marks={m:m for m in [x for x in range(41) if x % 5 == 0]},
                                                value=[0, 40]
                                                )
                                ]),
                    dcc.Graph(id="graph", figure=px.scatter(
                        df, x="PTS", y="MP", color="Pos"))
                ])
            ])
        ]
    elif pathname == "/page-2":
        return [
            html.H1('Diabetes')

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
    return px.scatter(flt, x="PTS", y="MP", color="Pos")


if __name__ == '__main__':
    app.server.run(debug=True)
