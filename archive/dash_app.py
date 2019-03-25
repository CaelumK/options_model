import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.DataFrame(columns = ['ID','Name', 'Address'])
ID = [1,2,3,4,5,6,7,8,9,10]
Name = ['A','B','C','D','E','F','G','H','I','J']
Address = [123,234,345,456,567,678,789,890,901,112]
df['ID'] = ID
df['Name'] = Name
df['Address'] = Address

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#273746',
    'text': '#7FDBFF'
}





def generate_table(dataframe, max_rows = 10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],
    style = {'color' : colors['text']}
    )
    
  
    
app.layout = html.Div(children=[
        html.H1('Credit Union Analysis Tool', style={'color' : colors['text'], 'textAlign' : 'center'}),
        html.Div([
            html.P('A web application for evaluation and comparison of Canadian credit unions.',style={'color' : colors['text'], 'fontSize' : 21, 'textAlign' : 'center'}),
            html.P('Developed by: Caelum W. Kamps', style={'color' : colors['text'], 'textAlign' : 'center'}),
            dcc.Markdown('___'),
            html.H4('Credit Union Data', style = {'color' : colors['text']}),
            generate_table(df),
            dcc.Checklist(
                    options=[
                            {'label': 'New York City', 'value': 'NYC'},
                            {'label': 'Montréal', 'value': 'MTL'},
                            {'label': 'San Francisco', 'value': 'SF'}
                            ],
                    values=['MTL', 'SF'], style ={'color' : colors['text']})
        ])
], style = {'marginBottom': 0, 'marginTop': 0})

if __name__ =='__main__':
    app.run_server()
    