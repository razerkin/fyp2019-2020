import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.subplots
#import plotly.express as px
from dash.dependencies import Input, Output
import os.path
import pandas as pd


param = pd.read_csv('./CSV/Background/PARAM/sa_param.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.Div([
        html.H4('CVX_Graph'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='cvx-update-graph'),
        dcc.Interval(
            id='cvx-interval-component',
            interval=1000,  # in milliseconds
            n_intervals=0)]),
    html.Div([
        html.H4('SA_Graph'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='sa-update-graph'),
        dcc.Interval(
            id='sa-interval-component',
            interval=10000,  # in milliseconds
            n_intervals=0)]),
    html.Div([
        html.H4('GLOBAL_Graph'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='global-update-graph'),
        dcc.Interval(
            id='global-interval-component',
            interval=100000,  # in milliseconds
            n_intervals=0)]),
])




# @app.callback(Output('live-update-text', 'children'),
#               [Input('interval-component', 'n_intervals')])
# def update_metrics(n):
#     lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return [
#         html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#         html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#         html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#     ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('cvx-update-graph', 'figure'),
              [Input('cvx-interval-component', 'n_intervals')])
def update_cvx_graph_live(n):
    N_WORKERS = param['N_WORKERS'][0]
    worker_cvx = []
    for i in range(N_WORKERS):
        # print(i)
        data = pd.read_csv('./CSV/Background/CVX/Worker_' + str(i) + '_cvx.csv', index_col=0)
        worker_cvx.append(data)
    # Create the graph with subplots
    rows = int(N_WORKERS/2) + 1
    cols = 2
    sub = 0
    fig = plotly.subplots.make_subplots(rows=rows, cols=cols)
    for r in range(rows):
        for c in range(cols):
            if sub <= N_WORKERS - 1:
                fig.append_trace({
                    'x': worker_cvx[sub]['time'],
                    'y': worker_cvx[sub]['vt'],
                    'name': 'Worker_' + str(sub) + '_CVX',
                    'mode': 'lines',
                    'type': 'scatter'
                }, r + 1, c + 1)
                # print(sub)
                fig.update_xaxes(title_text="Time", row=r + 1, col=c + 1)
                fig.update_yaxes(title_text="Vt", row=r + 1, col=c + 1)
                sub = sub + 1
            else:
                fig.update_layout(height=400, width=800, title_text="CVX Figures")
                break
    return fig



    # fig['layout']['margin'] = {
    #     'l': 30, 'r': 10, 'b': 30, 't': 10
    # }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}



@app.callback(Output('sa-update-graph', 'figure'),
              [Input('sa-interval-component', 'n_intervals')])
def update_sa_graph_live(n):
    N_WORKERS = param['N_WORKERS'][0]
    worker_sa = []
    for i in range(N_WORKERS):
        if os.path.exists('./CSV/Background/SA/Worker_' + str(i) + '_SA.csv'):
            data = pd.read_csv('./CSV/Background/SA/Worker_' + str(i) + '_SA.csv')
            worker_sa.append(data)
    # Create the graph with subplots
    rows = int(N_WORKERS/2) + 1
    cols = 2
    sub = 0
    fig = plotly.subplots.make_subplots(rows=rows, cols=cols,)
    for r in range(rows):
        for c in range(cols):
            if sub <= N_WORKERS - 1 and os.path.exists('./CSV/Background/SA/Worker_' + str(sub) + '_SA.csv'):
                fig.append_trace({
                    'x': worker_sa[sub]['step'],
                    'y': worker_sa[sub]['Gain'],
                    'name': 'Worker_' + str(sub) + '_SA',
                    'mode': 'lines',
                    'type': 'scatter'
                }, r + 1, c + 1)
                fig.update_xaxes(title_text="Step", row=r + 1, col=c + 1)
                fig.update_yaxes(title_text="Gain", row=r + 1, col=c + 1)
                sub = sub + 1
            else:
                fig.update_layout(height=400, width=800, title_text="SA Figures")
                break
    return fig



@app.callback(Output('global-update-graph', 'figure'),
              [Input('global-interval-component', 'n_intervals')])
def update_sa_graph_live(n):
    global_data = []
    if os.path.exists('./CSV/Background/GLOBAL/GLOBAL.csv'):
        data = pd.read_csv('./CSV/Background/GLOBAL/GLOBAL.csv')
        global_data.append(data)
    # Create the graph with subplots
    rows = 1
    cols = 1
    fig = plotly.subplots.make_subplots(rows=rows, cols=cols,)
    if os.path.exists('./CSV/Background/GLOBAL/GLOBAL.csv'):
        fig.append_trace({
            'x': global_data[0]['step'],
            'y': global_data[0]['Gain'],
            'name': 'GLOBAL GAIN',
            'mode': 'lines',
            'type': 'scatter'
        }, 1, 1)
        fig.update_xaxes(title_text="Step", row=1, col=1)
        fig.update_yaxes(title_text="Gain", row=1, col=1)
        fig.update_layout(height=400, width=800, title_text="GLOBAL Figures")


    return fig






if __name__ == '__main__':
    app.run_server(debug=False)


