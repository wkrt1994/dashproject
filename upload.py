import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([
     html.Div(
         className="",
         children=[
             html.Div(
                 className='one-third column',
                 children=[
                     html.H2('Plantillas de valoración de riesgos'),
                    
                    ],
                ),
            ],

        ),
        html.Div(
            className='container',
            children=[
                html.Div(className='row',
                style={},
                children=[
                    html.Div(
                        className= 'two columns',
                        children=[
                            html.P('Lectura de datos:', 
                            className= 'control-label'),
                            
                                html.Label(
                                    [
                                        html.Div(["Descarga"]),
                                        html.A(
                                            html.Button('Descarga aquí la plantilla de valoración sencilla', id='plantilla'),
                                                href='Imp.xlsx',
                                                style={'color':'blue', 'border':'solid 1px white'},
                                        ),
                                     ]
                                    ),
                                html.Label(
                                    [
                                        html.Div(['Método frecuencia']),
                                        dcc.Dropdown( id='metodos',
                                             options=[
                                                 {'label': 'Método 1', 'value':'1'},
                                                 {'label': 'Método 2', 'value':'2'},
                                                 {'label': 'Método 3', 'value':'3'}

                                             ],
                                            value=1,
                                            id="dropdown-input",
                                         ),
                                         

                                        ]
                                    ),
                                    html.Label([
                                        html.Div(['A continuación, carga la plantilla']),
                                        dcc.Upload(
                                            id='upload-data',
                                            children=html.Div([
                                                html.A('Arrastra o selecciona el archivo')
                                                ]),
                                                style={
                                                    'width': '30%',
                                                    'height': '30px',
                                                    'lineHeight': '30px',
                                                    'borderWidth': '1px',
                                                    'borderStyle': 'dashed',
                                                    'borderRadius': '3px',
                                                    'textAlign': 'center',
                                                    'margin': '10px'
                                                    },
                                                    
                                                    multiple=True
                                            ),
                                            html.Div(id='output-data-upload'),
                                     ]),
                                    

                                
                            ],
                      ),
                    ],
                   ),
            ],
            ),                         
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), sheet_name=('Imp'))
            df1= pd.read_excel(io.BytesIO(decoded), sheet_name=('Frec'))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        
        dash_table.DataTable(
            data=df1.to_dict('records'),
            columns=[{'name':i, 'id':i} for i in df1.columns]
        ),
        

       
       

        html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# @app.callback(
#     Output("input-metodos", "children"), [Input("metodos", "value")])

# def updateTable(metodo):
#     if metodo == "1":
#             return  
#             met=df1.iloc[0:10,0:4]
#             met=met.fillna(value=0)
#             met[['L Inferior','L Superior']]=met[['L Inferior','L Superior']].astype(int)
#             met1=met[met['Probabilidad'] != 0]

#         elif metodo == "2":
#             return  
#             met=df1.iloc[0:1,5:7]
#             met=met.astype(int)
        
#         elif metodo == '3':
#             return 
#             met=df1.iloc[0:1,8:10]
#             met.columns=['Poblacion','Prob de un evento']
#             met['Poblacion']=met['Poblacion'].astype(int)
    
if __name__ == '__main__':
    app.run_server(debug=True)