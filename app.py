# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 12:10:16 2019

@author: Caelum Kamps
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

options = pd.DataFrame(columns = ['name','type','position','strike','price'])

# Html Stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Intialize app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Text and background color selection
colors = {
    'background': '#273746',
    'text': '#7FDBFF'
}


# Define app layout   
app.layout = html.Div(children=[
        # Header
        html.H3('Option Modeling and Sensitivity Tool', 
                style={'color' : colors['text'], 'textAlign' : 'center',
                       'marginBottom' : 0}),
        # Description
        html.Div([
            html.P('''A web app for the evaluation and visualization of 
                   option strategies and their risks''',
                   style={'color' : colors['text'], 
                          'fontSize' : 15, 'textAlign' : 'center'}),
            # Author 
            html.P('Developer: Caelum Kamps', 
                   style={'color' : colors['text'], 'textAlign' : 'center',
                          'marginBottom' : 0}),
            # Line break
            dcc.Markdown('___'),
            
            # Label and checkboxes
            html.Div([
                    # %% option properties entry
                    html.Div([
                            html.Label('Enter a name for you option', 
                                       style = {'color' : colors['text']}),
                            # option name           
                            dcc.Input(id = 'name', 
                                      value = 'Example', 
                                      type='text'),
                            # Update Available options          
                            html.Button('Add Option', id='button', n_clicks=0,
                                        style = {'color' : colors['text']}),
                            # Select position and type
                            html.Div([
                                
                                # Type
                                html.Div([dcc.RadioItems(
                                        id = 'call_put',
                                        options=[
                                                {'label': 'Call', 
                                                 'value': 'call'},
                                                {'label': 'Put', 
                                                 'value': 'put'}
                                                ],
                                        value = 'call',
                                        style = {'color' : colors['text']})
                                        ],className = 'six columns'),
                                
                                # Position
                                html.Div([dcc.RadioItems(
                                        id = 'long_short',
                                        options=[
                                                {'label': 'Long', 
                                                 'value': 'long'},
                                                {'label': 'Short', 
                                                 'value': 'short'}
                                                ],
                                        value = 'long',
                                        style = {'color' : colors['text']})
                                ],className = 'six columns')
                            ], className='row'),
                
                            #%% Strike and Premium
                            html.Div([
                                # Strike
                                html.Div([
                                        html.Label('Enter the option strike price:', 
                                                   style = {'color' : colors['text']}),
                                        dcc.Input(id = 'strike', 
                                                  value = 100, 
                                                  type='number')
                                        ],className = 'six columns'),
                                
                                # Premium
                                html.Div([
                                        html.Label('Enter the option premium:', 
                                                   style = {'color' : colors['text']}),
                                        dcc.Input(id = 'price', 
                                                  value = 5, 
                                                  type='number')
                                ],className = 'six columns')
                            ], className='row'),
                            
                            #%% Underlying Price and Time to Maturity
                            # Current price of the underlying
                            html.Div([
                                html.Div([
                                        html.Label('Enter the current price of the underlying:', 
                                                   style = {'color' : colors['text']}),
                                        dcc.Input(id = 'underlying_price', 
                                                  value = 100, 
                                                  type='number')
                                        ],className = 'six columns'),
                            
                                # Time to maturity 
                                html.Div([
                                        html.Label('Enter the time to matrurity in days:', 
                                                   style = {'color' : colors['text']}),
                                        dcc.Input(id = 'maturity', 
                                                  value = 5, 
                                                  type='number')
                                ],className = 'six columns')
                            ], className='row'),
                            
            
                            ], className='six columns'),
                     
                    #%% Select active options
                    html.Div([
                            dcc.Dropdown(
                                    id='dropdown',
                                    options=[],
                                    multi = True,
                                    value=None)
                            ], className='six columns'),
                    ], className = 'row'
            ), 
            
            html.Div(html.P('Select Figure Step Size'), 
                     style = {'color' : colors['text']}),     
                       
            # Step Size Slider
            dcc.Slider(id = 'step_size', 
                       min = 0.25, 
                       max = 5, 
                       step = 0.25, 
                       value = 2),
            
            # Slider output container
            html.Div(id='slider-output-container', 
                     style = {'color' : colors['text']}),
           
            # Table 
            dcc.Graph(id = 'plot')
            
        ])
], style = {'backgroundColor' : colors['background'], 'marginBottom': 0, 'marginTop': 0})

# CSS style sheet for rows and columns
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})    
                            
@app.callback(Output('dropdown', 'options'),
              [Input('button', 'n_clicks')],
              [State('name', 'value'),
               State('call_put', 'value'),
               State('long_short','value'),
               State('strike','value'),
               State('price','value'),
               State('underlying_price','value'),
               State('maturity', 'value'),
               State('dropdown', 'options')])

def update_available_options(click, name, call_put, long_short, K, P, underlying_price, maturity, existing_options):
    option_name = name
    existing_options.append({'label': option_name+' '
                                      +str(long_short)+' '
                                      +str(call_put)+' ' 
                                      +str(K)+' '
                                      +str(P)+' UP = '
                                      +str(underlying_price)+' T= '
                                      +str(maturity), 
                             'value': option_name+' '
                                      +str(long_short)+' '
                                      +str(call_put)+' ' 
                                      +str(K)+' '
                                      +str(P)+' UP = '
                                      +str(underlying_price)+' T= '
                                      +str(maturity)})
    return existing_options

@app.callback(Output('plot', 'figure'),
              [Input('dropdown', 'value')])
    
def update_chart(active_options):
    return


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('step_size', 'value')])

def update_output(value):
    return 'Step Size = "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=False)
