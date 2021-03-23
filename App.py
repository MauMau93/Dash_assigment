import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
app = dash.Dash(__name__, title="2021 Dash Python App",external_stylesheets=[dbc.themes.CERULEAN])
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

app.layout = html.Div([
    html.H1(app.title),
    dcc.Markdown(markdown_text),
     html.Label(["Select Position of the player",
        dcc.Dropdown('mydropdown', options=opt_Pos, value=opt_Pos[0]['value'])
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
])


@app.callback(
     Output('my-table', 'data'),
     Input('mydropdown', 'value'),
    Input('mydropdown2', 'value'))
def update_data(mydropdown, mydropdown2):

    if type(mydropdown2) == type([]):
        filter=df[(df['Pos'] == mydropdown) & (df['Tm'].isin(mydropdown2))]
    else:
        filter=df[(df['Pos'] == mydropdown) & (df['Tm'] == mydropdown2)]


    return filter.to_dict("records")

   
if __name__ == '__main__':
 app.server.run(debug=True)
