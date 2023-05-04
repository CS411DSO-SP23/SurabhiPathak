from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
from mysql.connector import errorcode
from mysql_utils import *
from mongodb_utils import *
from neo4j_utils import *
#import pymysql

cnx = mysql.connector.connect(host='127.0.0.1', user='root', password='Welcome1', database='academicworld')
cursor = cnx.cursor()

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = Dash(__name__, external_stylesheets=external_stylesheets)


# this is temporary for testing
#df= pd.read_sql("select name, position, email, phone from faculty_bak_for_updates limit 40", cnx)


app.layout = html.Div(children=[
    html.H1(children='Know about the top faculties, their most cited publications and popular keywords', style={'textAlign':'center'}),
    html.Div(children=[

        # Dropdown for universities
        dcc.Dropdown(getAllUniversities(cnx.cursor()), "University of illinois at Urbana Champaign", id='dropdown-university', maxHeight=300),
        #dcc.Dropdown(getAllUniversities(cnx.cursor()), "University of illinois at Urbana Champaign", id='dropdown-university'),
        dcc.Graph(
            id='graph-content-positions', style={'display': 'inline-block'}
        ),

        # Dropdown for publication year
        dcc.Dropdown(getPublicationYears(cnx.cursor()), "2012", id='dropdown-selection-year', maxHeight=300),
        dcc.Graph(
            id='graph-content-pubCount', style={'display': 'inline-block'}
        ),

        dcc.Dropdown(getPublicationYears(cnx.cursor()), "2012", id='dropdown-selection-year01', maxHeight=300),
        dcc.Graph(
            id='graph-content-pubCount01', style={'display': 'inline-block'}
        ),

       # dcc.Dropdown(getPublicationYears(cnx.cursor()), "2012", id='dropdown-selection-year01', maxHeight=300),
    #    html.Div([
    #         dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
    #         html.Div(id='dd-output-container')
    #     ]),

        dcc.Dropdown(getTop20Keywords(cnx.cursor()), "algorithm" ,  id='dropdown-top20-keywords', maxHeight=300),
        dcc.Graph(
            id='graph-content-faculty-krc', style={'display': 'inline-block'}
        ),

        # Neo4J layout

        dcc.Dropdown(getAllUniversities(cnx.cursor()), "University of illinois at Urbana Champaign", id='university-info', maxHeight=300),
        dcc.Graph(
            id='graph-content-neo4j-faculty', style={'display': 'inline-block'}
        ),

        #MongoDB add/delete
        dash.html.Label("University of illinois at Urbana Champaign"), 
        html.Div([

                html.Div(id='mongo-datatable', children=[]),

                # activated once/week or when page refreshed
                dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
                html.Button("Save to Mongo Database", id="save-it"),
                html.Button('Add Row', id='adding-rows-btn', n_clicks=0),

                html.Div(id="show-graphs", children=[]),
                html.Div(id="placeholder")

        ]),


#------------------------------------test code to verify datatable - closing comment --------------------
        # This is for Mongo layout
       # dcc.Dropdown(getAllUniversities(cnx.cursor()), "University of illinois at Urbana Champaign", id='university-mongo', maxHeight=300),

        #  dash.html.Label("University of illinois at Urbana Champaign"),       
        #  html.Div([
            
        #     dash_table.DataTable(
        #         #id='datatable_id2',
        #         id='graph-content-mongo-faculty',
        #         data=showFacultyinfo().to_dict('records'),
        #         columns=[
        #             {"name": i, "id": i, "deletable": True, "selectable": True , 'renamable': True} for i in showFacultyinfo().columns
        #         ],
        #         editable=True,
        #         filter_action="native",
        #         sort_action="native",
        #         sort_mode="multi",
        #         row_selectable="multi",
        #         #row_deletable=True,
        #         selected_rows=[],
        #         page_action="native",
        #         page_current= 0,
        #         page_size= 6,
        #         # page_action='none',
        #         # style_cell={
        #         # 'whiteSpace': 'normal'
        #         # },
        #         # fixed_rows={ 'headers': True, 'data': 0 },
        #         # virtualization=False,
        #         style_cell_conditional=[
        #             {'if': {'column_id': 'name'},
        #             'width': '40%', 'textAlign': 'left'},
        #             {'if': {'column_id': 'email'},
        #             'width': '30%', 'textAlign': 'left'},
        #             {'if': {'column_id': 'phone'},
        #          'width': '30%', 'textAlign': 'left'},
        #         ],
        #     ),
        #     #html.Button('Add Row', id='editing-rows-button', n_clicks=0),


        #     ],className='row2',
        # ),
   
    ])
])




# First CallBack

@app.callback(
    Output('graph-content-positions', 'figure'),
    Input('dropdown-university', 'value')
)
def update_output(value):
    # print("I am in the first widget")
    # print (value)
    university_id=universityId(value, cnx)
    #print ("University id is " + str(university_id))
    #facultyPositions(university_id, cnx.cursor())
    df = pd.DataFrame(facultyPositions(university_id, cnx.cursor()), columns=['position', 'count'])
    #print (df)
    return px.bar(df, x="position", y="count", barmode="group")
   

# Second CallBack
#df3 = None
@app.callback(
    Output('graph-content-pubCount', 'figure'),
    Input('dropdown-selection-year', 'value')
)
def update_output_1(value2):
    year=value2
    df2 = pd.DataFrame(getPublicationCount(str(year), cnx.cursor()), columns = ['facultyname', 'publication_count'])
    #return px.bar(df2, x="name", y="publication_count", barmode="group")
    return px.pie(df2, values='publication_count', names='facultyname', title='Publication Count per faculty')

# Third CallBack

@app.callback(
   Output('graph-content-pubCount01', 'figure'),
   Input('dropdown-selection-year01', 'value')
)
def update_output3(value3):
    df3 = pd.DataFrame(getTop20Publications(value3, cnx.cursor()), columns = ['faculty_name', 'publication_title'])
    #return px.bar(df3, x="faculty_name", y="publication_title", barmode="group")
    #return px.scatter(df3, x='faculty_name', y='publication_title', color='continent', title='Top20 Publications')
    return px.scatter(df3, x='faculty_name', y='publication_title', title='Faculties and the Top 20 Publications with max number of citations')
    #return px.line(df3, x='faculty_name', y='PublicationCount', title='Top20 Publications')


# Fourth CallBack  -- Dummy one

# @app.callback(
#     Output('dd-output-container', 'children'),
#     Input('demo-dropdown', 'value')
# )
# def update_output_static(value3):
#     return f'You have selected {value3}'


#----------------------------------------------------------------------------------------------------MongoDB show faculty details---------------------------#

@app.callback(
    Output('graph-content-faculty-krc', 'figure'),
    Input('dropdown-top20-keywords', 'value')
)
def update_output3(value4):
    #print (value4)
    df4 = pd.DataFrame(getFacultyKRC(value4, cnx.cursor()), columns = ['facultyname', 'krc'])
    #print (df4)
    #return px.bar(df2, x="name", y="publication_count", barmode="group")
    return px.pie(df4, values='krc', names='facultyname', title='Keyword Relevance per faculty')
    #return px.scatter(df4, x="facultyname", y="krc", color="species", hover_data=['krc'])


# Checking for Neo4j

@app.callback(
    Output('graph-content-neo4j-faculty', 'figure'),
    Input('university-info', 'value')
)
def update_output3(value6):
    # print (value6)
    # print(type(value6))
    df6 = pd.DataFrame(neo4j_data(value6), columns = ['keyword.name', 'faculty_count'])
    #print (df6)
    #return px.bar(df2, x="name", y="publication_count", barmode="group")
    return px.histogram(df6, x="faculty_count", y="keyword.name", barmode="group")
    #return px.pie(df4, values='krc', names='facultyname', title='Keyword Relevance per faculty')



#--------------------------------------------------------------Add and update to the MongoDB collection----------------------------------------------------------


# Add new rows to Mongo DB Collection using DataTable ***********************************************

# Display Datatable with data from Mongo database *************************

@app.callback(Output('mongo-datatable', 'children'),
              [Input('interval_db', 'n_intervals')])
def populate_datatable(n_intervals):
    print(n_intervals)
    # Convert the Collection (table) date to a pandas DataFrame
    df = pd.DataFrame(list(collection.find({'affiliation.name': 'University of illinois at Urbana Champaign'}, { "_id": 0, "name": 1, "position": 1, "email": 1, "phone":1 })))
    #Drop the _id column generated automatically by Mongo
    df = df.iloc[:, 0:]
    print(df.head(20))

    return [
        dash_table.DataTable(
            id='my-table',
            columns=[{
                'name': x,
                'id': x,
            } for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
           # row_deletable=True,
            filter_action="native",
            filter_options={"case": "sensitive"},
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_current=0,  # page number that user is on
            page_size=6,  # number of rows visible per page
            style_cell={'textAlign': 'left', 'minWidth': '100px',
                        'width': '100px', 'maxWidth': '100px'},
        )
    ]

@app.callback(
     Output('my-table', 'data'),
    [Input('adding-rows-btn', 'n_clicks')],
    [State('my-table', 'data'),
     State('my-table', 'columns')],
)

def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows


# Save new DataTable data to the Mongo database ***************************
@app.callback(
    Output("placeholder", "children"),
    Input("save-it", "n_clicks"),
    State("my-table", "data"),
    prevent_initial_call=True
)

def save_data(n_clicks, data):
    dff = pd.DataFrame(data)
    #collection.delete_many({})
    collection.insert_many(dff.to_dict('records'))
    return ""





if __name__ == '__main__':
   # app.run_server(dev_tools_hot_reload=None)
   app.run_server(debug=True)
    #app.run_server()

#cnx.close()