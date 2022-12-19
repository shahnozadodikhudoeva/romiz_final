from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import sqlite3
import numpy as np
import bs4
import requests
from bs4 import BeautifulSoup
db = sqlite3.connect('hr.db')
df = pd.read_sql_query('select * from jobs;', db)


app = Dash(__name__)
server =  app.server
#ex1
#exercise 1
#https://pypi.org/project/ERAlchemy/#:~:text=ERAlchemy%20generates%20Entity%20Relation%20(ER,databases%20or%20from%20SQLAlchemy%20models. 
#https://stackoverflow.com/questions/66381950/error-when-trying-to-install-eralchemy-in-jupyter-from-a-windows-device 
#https://graphviz.org/download/
#https://stackoverflow.com/questions/66381950/error-when-trying-to-install-eralchemy-in-jupyter-from-a-windows-device
#the file uploaded with the name part1.png
#the work was done in the google collab as it was not working in the vscode
#pip install sqlalchemy== 1.3
#pip install --upgrade --no-deps git+https://github.com/psychemedia/eralchemy.git
#from eralchemy import render_er
#png = render_er("sqlite:///hr.db", "part1.png")
#png.render("part1")
#ex2
#https://dash.plotly.com/dash-core-components
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html
dtc = pd.read_sql("SELECT employees.first_name, jobs.job_title " +
                                "FROM employees " + 
                                "INNER JOIN jobs ON employees.job_id " + 
                                "= jobs.job_id",db)

# fig = go.Figure()
fig = px.bar(dtc, x='job_title')
options = dtc["job_title"].unique()


# 3
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql.html
#https://dash.plotly.com/dash-core-components
df = df.iloc[1: , :]
df["difference"]=df['max_salary']-df['min_salary']
differences_option=df["difference"].unique()
differences_option=np.append(0, differences_option)
max_salary=df['difference'].max()

# 4
employee_sal = pd.read_sql("SELECT employees.salary " +"FROM employees",db)
avg_salary = employee_sal['salary'].mean()

def percentages():
    URL = "https://www.itjobswatch.co.uk/jobs/uk/sqlite.do"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib') 
    table = soup.find('table', attrs = {'class':'summary'}) 
    table.find('form').decompose()
    table_dt = table.tbody.find_all("tr")
    table = []
    for i in table_dt:
        row = []
        r = i.find_all("td")
        if len(r) == 0:
            r = i.find_all("th")
        for j in r:
            row.append(j.text)
        table.append(row)

    header = table[1]
    header[0] = "index"
    df = pd.DataFrame(table)
    df.drop(index=[0,1,2,3,4,5,6,7,10,11,14,15],axis=0,inplace=True)
    df.columns = header
    df.set_index("index",inplace=True)
    df.reset_index(inplace=True)
    df['Same period 2021'] = df['Same period 2021'].str.replace('£','')
    df['Same period 2021'] = df['Same period 2021'].str.replace(',','')
    df['Same period 2021'] = df['Same period 2021'].str.replace('-','0').astype(float)
    df['6 months to19 Dec 2022'] = df['6 months to19 Dec 2022'].str.replace('£','')
    df['6 months to19 Dec 2022'] = df['6 months to19 Dec 2022'].str.replace(',','').astype(float)
    df['Same period 2020'] = df['Same period 2020'].str.replace('£','')
    df['Same period 2020'] = df['Same period 2020'].str.replace(',','').astype(float)
    df.loc[4] = ['Average', avg_salary, avg_salary,avg_salary] 
    return df

perc = percentages()
axis = perc["index"]
perc.drop("index",inplace=True,axis=1)
years = perc.columns


app.layout = html.Div(children=[
    html.H1(children='Final exam',style={'color':'rgb(148, 137,137)','text-align': 'center', "font-size": "50px", }),
    html.P("Exercise 1",
               style={'text-align': 'center', "padding": "10px", "font-size": "25px"}),
    html.P("Read the comments, and the output itself is in the zip file, in the png format",
               style={'color':'blue','text-align': 'center', "padding": "10px", "font-size": "17px"}),
    html.P("Exercise 2",
               style={'text-align': 'center', "padding": "10px", "font-size": "25px"}),
     dcc.Checklist(
        options=options,
        id = "input1",

        inline=True
    ),
    dcc.Graph(id="output1"),
    html.P("Exercise 3",
               style={'text-align': 'center', "padding": "10px", "font-size": "25px"}),
    html.Div(children=[
    dcc.Dropdown(
        options=differences_option,
        value=differences_option.min(),
        id="input2min"
        ),
    dcc.Dropdown(
        options=differences_option,
        value=differences_option.max(),
        id="input2max"
        ),], className="dropdown1"),
    dcc.Graph(id='output2'),
    html.P("Exercise 4",
               style={'text-align': 'center', "padding": "10px", "font-size": "25px"}),
    dcc.Dropdown(years,
                             
            value='all',
            placeholder="6 months to19 Dec 2022",
            id="input3"
                             ),
        dcc.Graph(id="output3"),
               
], className="mainDiv")
    

@ app.callback(
    Output('output1', 'figure'),
    Input('input1', "value"),)

def update_output(value):
    liste=dtc[dtc["job_title"].isin(value)]
    fig= px.bar(liste, x=liste['job_title'])
    return fig



@app.callback(
Output('output2', 'figure'),
[Input('input2min', 'value'),
Input('input2max', 'value')]
)
def update_output(value1,value2):
    fig2 = go.Figure()
    fig2["layout"]["xaxis"]["title"] = "Jobs"
    fig2["layout"]["yaxis"]["title"] = "Difference"
    dft = df[df["difference"]>=value1][df["difference"]<=value2]
    fig2.add_trace(go.Bar(x=dft['difference'], y=dft['job_title'],
    name='Job differences', orientation="h"))
    return fig2

@app.callback(
        Output('output3', 'figure'),
        Input('input3', 'value')
        )
def update_output(value):
    if value == "all" or value == None:
        y = perc["6 months to19 Dec 2022"]
    else:
        y =perc[value]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=axis.values,y=y.values, marker_color=['green','green','green','green','black'], marker_size=15))
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)