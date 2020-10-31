import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import plotly.express as px
import itertools

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel('/home/zhenhuixu/mysite/download_data.xlsx')

tab_14 = pd.read_excel('/home/zhenhuixu/mysite/sed17-sr-tab014.xlsx', skiprows=[0,1,2,3])
tab_14.columns = ["Fields","Number_1987","Percent_1987","Number_1992","Percent_1992","Number_1997",
              "Percent_1997","Number_2002","Percent_2002","Number_2007","Percent_2007","Number_2012","Percent_2012",
             "Number_2017","Percent_2017"]
tab_14 = tab_14.set_index("Fields")
tab_14_number = tab_14.loc[:,tab_14.columns[tab_14.columns.str.startswith("Number")]]
tab_14_number["Subject"] = list(itertools.chain.from_iterable(itertools.repeat(x, 3) for x in tab_14_number.index if x not in ["Female","Male"]))
tab_14_number = tab_14_number.reset_index()
tab_14 = pd.concat([tab_14_number[tab_14_number.Fields=="Male"],tab_14_number[tab_14_number.Fields=="Female"]]).rename({'Fields':'Sex'},axis='columns')
year_unique = [1987,1992,1997,2002,2007,2012,2017]

#df = pd.read_excel('download_data.xlsx')
grouped = df.groupby('Categories')
categories_unique = [x[0] for x in grouped.Categories.unique()]
subjects_unique = df.columns[2:]

app.layout = html.Div([
    html.H1(children='Survey of Earned Doctorates'),
    html.Div([
        dcc.Dropdown(
            id='categories',
            options=[{'label': i, 'value': i} for i in categories_unique],
            value=categories_unique[0]
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in subjects_unique],
                value=subjects_unique[0]
            )
    ],style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(
        id='graph-with-subject'
    ),
    dcc.Graph(
        id='bar-chart'
    ),
    dcc.Slider(
        id='year--slider',
        min=1987,
        max=2017,
        value=2017,
        marks={str(year): str(year) for year in year_unique},
        step=None
    )
])

@app.callback(
    Output('graph-with-subject', 'figure'),
    [Input('categories', 'value'),
     Input('yaxis-column', 'value')])
def update_figure(selected_subject, yaxis_column_name):
    filtered_df = grouped.get_group(selected_subject)

    fig = px.line(filtered_df, x="Year", y=yaxis_column_name,
              title="Doctorate Recipients by Field of Study")

    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year--slider', 'value')])
def update_figure(yaxis_year):
    column_name = "Number_"+str(yaxis_year)
    ylab_name = "Number of doctorate recipients in "+str(yaxis_year)
    fig = px.bar(tab_14, x="Subject", y=column_name,
                 color="Sex", barmode='group', labels={column_name:ylab_name},
              title="Bar chart by Sex")

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)