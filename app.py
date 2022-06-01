# Import required libraries

import pickle
import datetime as dt
import requests
import pandas as pd
from flask import Flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


# plotly libs
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, html, dcc


app = dash.Dash()
server = app.server


# load data 
df = pd.read_csv('data/Unicorn_Companies_Edited.csv')


# Def Graphs

#Treemap
fig_tmap = px.treemap(df,path= ["country", "industry", "company"],
                
            values="valuation_in_billions", color_discrete_sequence=px.colors.qualitative.Pastel,
            height=650,
            
    )

fig_tmap.update_traces(root_color="lightblue")
fig_tmap.update_layout(margin = dict(t=25, l=25, r=25, b=25))





import pycountry

input_countries = df['country']

countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

codes = [countries.get(country, 'Unknown code') for country in input_countries]


df['iso_alpha'] = codes


# Create app layouts
app.layout = html.Div(
    [
        # -- header div
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                        'Unicorn Companies',
                        ),
                        
                    ],

                    className='eight columns'
                ),
                html.Img(
                    src="/assets/unicorn.png",
                    className='uimg',
                ),

            ],
            id="header",
            className='row',
        ),
        # -- main div
        html.Div(
            [
                # -- filtering div
                html.Div(
                    [
                        
                        
                        #dcc.Graph(id='myGraph',figure=fig),
                        
                        

                        html.H5(
                            'Filter by Industry:',
                            className="control_label"
                        ),
                        dcc.Dropdown(df['industry'].unique(),
                                     id='DDI',placeholder="Select an industry",className="dcc_control",multi=True),
                        
                        dcc.RadioItems(['All', 'Customize'], 'All', inline=True,id='industry_radio') ,

                        
                        html.H5(
                            'Filter by Country:',
                            className="control_label"
                        ),
                        dcc.Dropdown(df['country'].unique(),id='DDCTR',
                                     placeholder="select a country",className="dcc_control",multi=True),
                        
                        dcc.RadioItems(['All', 'Customize'], 'All', inline=True,id='countries_radio'),
                        
                        html.H5(
                            'Filter by Company:',
                            className="control_label"
                        ),
                        dcc.Dropdown(df['company'].unique(),
                                     id='DDCMP',placeholder="select a company",className="dcc_control",multi=True),
                        
                        dcc.RadioItems(['All', 'Customize'], 'All', inline=True,id='company_radio'),


                    ],
                    className="pretty_container four columns"
                ),
                
                # -- BANs div
                html.Div(
                    [
                        html.Div(
                            [
                            
                                # -- BANs div
                            
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5("Companies"),
                                                html.H4(
                                                    id="companies",
                                                    className="info_text"
                                                )
                                            ],
                                            id="gas",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.H5("Valuation"),
                                                html.H4(
                                                    id="valuation",
                                                    className="info_text"
                                                )
                                            ],
                                            id="oil",
                                            className="pretty_container"
                                        ),
                                        html.Div(
                                            [
                                                html.H5("Total Raised"),
                                                html.H4(
                                                    id="tot_raised",
                                                    className="info_text"
                                                )
                                            ],
                                            id="water",
                                            className="pretty_container"
                                        ),
                                    ],
                                    id="tripleContainer",
                                )

                            ],
                            id="infoContainer",
                            className="row"
                        ),
                        
                        # -- Graph below BANs div
                        
                        html.Div(
                            [
                                html.H3(children='How many unicorn companies in each country?',
                                        style={
                                    'textAlign': 'center',
                                    'color': "#343434"
                                }),
                                dcc.Graph(
                                    id='Graph_hist',
                                )
                            ],
                            id="countGraphContainer",
                            className="pretty_container"
                        )
                    ],
                    id="rightCol",
                    className="eight columns"
                )
            ],
            className="row"
        ),
        
        # graphs level 2 div
        html.Div(
            [
                html.Div(
                    [
                        html.H3(children='How long it takes to become a unicorn?',
                                style={
                            'textAlign': 'center',
                            'color': "#343434"
                        }),
                        dcc.Graph(id='graph_years'),
                        dcc.RangeSlider(
                        id = 'my-slider',
                        min=1,
                        max=22,
                        step=None,
                        marks={
                            str(years):str(years) for years in range(1,23)
                        },
                        value=[1, 5]
                    ),
                    ],
                    className='pretty_container six columns',
                ),
                html.Div(
                    [
                        html.H3(children='When did most companies become unicorns?',
                                style={
                            'textAlign': 'center',
                            'color': "#343434"
                        }),
                        dcc.Graph(id='graph_jy'),
                        dcc.RangeSlider(
                        id = 'my-slider_joind_years',
                        min=2007,
                        max=2022,
                        step=None,
                        marks={
                            str(years):str(years) for years in df['year_joined'].unique()
                        },
                        value=[2012, 2022]
                    ),
                    ],
                    className='pretty_container six columns',
                ),
            ],
            className='row'
        ),
        
        
        # graphs level 3 --> Map 
        html.Div(
            [
                html.Div(
                    [
                        html.H3(children='Where are our unicorns?',
                                style={
                            'textAlign': 'center',
                            'color': "#343434"
                        }),
                        
                        dcc.Graph(id='val_Gmap')
                    ],
                    className='pretty_container twelve columns',
                ),
                
                

            ],
            className='row'
        ),
        
        # graphs level 3 div
        
        html.Div(
            [
                
                html.Div(
                    [
                        html.H3(children='Which cities have top valuations?',
                                style={
                            'textAlign': 'center',
                            'color': "#343434"
                        }),
                        dcc.Graph(id='top_10')
                        
                    ],
                    className='pretty_container five columns',
                ),
              
                html.Div(
                    [
                     html.H3(children='Industry-Valuation Market Share',
                                style={
                            'textAlign': 'center',
                            'color': "#343434"
                        }),
                        #dcc.Graph(id='val_Graph2'),
                        dcc.Graph(id='dounut_G'),
                        
                    ],
                    className='pretty_container seven columns',
                ),
            ],
            className='row'
        ),
        
        
    
        
        # tree map div
        html.Div(
            [
                html.Div(
                    [
                        html.H3(children='See the whole picture & dig deeper',
                                style={
                            'textAlign': 'center',
                            'color': "#343434"
                        }),
                        dcc.Graph(figure=fig_tmap),
                        

                    ],
                    className='pretty_container twelve columns',
                )
            ],
            className='row'
        ),
        
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
    
    
)



@app.callback(
    Output(component_id='companies',component_property='children'),
    Output(component_id='valuation',component_property='children'),
    Output(component_id='tot_raised',component_property='children'),
    Input(component_id='DDI',component_property='value'),
    Input(component_id='DDCTR',component_property='value'),
    Input(component_id='DDCMP',component_property='value'),
    
    Input(component_id='industry_radio',component_property='value'),
    Input(component_id='countries_radio',component_property='value'),
    Input(component_id='company_radio',component_property='value')
    
    
)
def update_bans(DDI,DDCTR,DDCMP,RBI,RBCTR,RBCMP):
    filt_df = df
    if (RBI == 'Customize'):
        if (DDI != None):
            filt_df=filt_df[filt_df['industry'].isin(DDI)] 
    
    
    if (RBCTR == 'Customize'):
        if (DDCTR != None):
            filt_df=filt_df[filt_df['country'].isin(DDCTR)]  
            
            
    if (RBCMP == 'Customize'):
        if (DDCMP != None):
            filt_df=filt_df[filt_df['company'].isin(DDCMP)]  
            
            
    company_sum = filt_df['company'].count()

##############################

    tot_val = filt_df['valuation_in_billions'].sum()
    if tot_val > 0:
        tv= " B"
    else:    
        tv = " "
    tot_val =round(tot_val, 2)
    tot_val ="$ "+ str(tot_val) + tv
    
###########################

    tot_raised = filt_df['total_raised'].sum()
    
    if (tot_raised/1000>1):
        v = " K"
        if (tot_raised/1000000>1):
            v = " M"
            if (tot_raised/1000000000>1):
                v = " B"
    else:
        v= " "
        
    if v == " K" :
        tot_raised= tot_raised/1000
    if v == " M" :
        tot_raised= tot_raised/1000000
    if v == " B" :
        tot_raised=tot_raised/1000000000

    tot_raised =round(tot_raised, 2)
    tot_raised ="$ "+ str(tot_raised) + v


    return company_sum,tot_val,tot_raised




@app.callback(
    Output(component_id='Graph_hist',component_property='figure'),
    Input(component_id='DDI',component_property='value'),
    Input(component_id='DDCTR',component_property='value'),
    
    Input(component_id='industry_radio',component_property='value'),
    Input(component_id='countries_radio',component_property='value'),
)
def update_stacked_bar(DDI,DDCTR,RBI,RBCTR):
    
    filt_df = df
    
    if (RBI == 'Customize'):
        if (DDI != None):
            filt_df=df[df['industry'].isin(DDI)]  
            
            
    if (RBCTR == 'Customize'):
        if DDCTR != None:
            filt_df=filt_df[filt_df['country'].isin(DDCTR)]
    
    
    
    fig = px.histogram(x=filt_df['country'],color=filt_df['industry'],
                       
                    )
    fig.update_layout(
    #title="Plot Title",
    xaxis_title="Countries",
    yaxis_title="Count Of Unicorns",
    #legend_title="Legend Title"
    )
    
    
    return(fig)


"""
@app.callback(
    Output(component_id='val_Graph1',component_property='figure'),
    Output(component_id='val_Graph2',component_property='figure'),
    Input(component_id='DDI',component_property='value'),
    Input(component_id='DDCTR',component_property='value'),
    Input(component_id='DDCMP',component_property='value'),
    Input(component_id='industry_radio',component_property='value'),
    Input(component_id='countries_radio',component_property='value'),
)
def update_valuation(DDI,DDCTR,DDCMP,RBI,RBCTR):
    filt_df = df  
    filt_df2 =df
    
    if (RBI == 'Customize'):
        if (DDI != None):
            filt_df=df[df['industry'].isin(DDI)]  

    if (RBCTR == 'Customize'):
        if (DDCTR != None):
            filt_df2=filt_df2[df['country'].isin(DDCTR)]


    fig = px.histogram(x = filt_df['company'],y=filt_df['valuation_in_billions'])
    
    fig.update_layout(
    #title="Plot Title",
    xaxis_title="Companies",
    yaxis_title="Valuations in billions",
    #legend_title="Legend Title"
    )
    
    
    fig2 = px.histogram(x = filt_df['city'],y=filt_df['valuation_in_billions'])
    
    
    fig2.update_layout(
    #title="Plot Title",
    xaxis_title="Cities",
    yaxis_title="Valuations in billions",
    #legend_title="Legend Title"
    )
    
    return fig,fig2




"""




################### top10 ##################

@app.callback(
    Output(component_id='top_10',component_property='figure'),
    Input(component_id='DDI',component_property='value'),
    Input(component_id='DDCTR',component_property='value'),
    Input(component_id='DDCMP',component_property='value'),
    Input(component_id='industry_radio',component_property='value'),
    Input(component_id='countries_radio',component_property='value'),
)
def update_valuation(DDI,DDCTR,DDCMP,RBI,RBCTR):
    filt_df = df  
    
    if (RBI == 'Customize'):
        if (DDI != None):
            filt_df=filt_df[filt_df['industry'].isin(DDI)]  

    if (RBCTR == 'Customize'):
        if (DDCTR != None):
            filt_df=filt_df[filt_df['country'].isin(DDCTR)]
    
    filt_df = filt_df.groupby(['city','industry'])[['valuation_in_billions']].sum().reset_index().sort_values('valuation_in_billions', ascending= False)[:15]

    fig = px.histogram(x = filt_df['city'],y=filt_df['valuation_in_billions'],
                       color=filt_df['industry'])
#    fig = px.histogram(x = filt_df['company'],y=filt_df['valuation_in_billions'])
    
    fig.update_layout(
    #title="Plot Title",
    xaxis_title="Cities",
    yaxis_title="Valuations in billions",
    #legend_title="Legend Title"
    )
    
    
    return fig




@app.callback(
    Output(component_id='graph_years',component_property='figure'),
    Input('my-slider','value'),
    )

def update_years_unicorn(selected_range):
    # Filter data 
    
    #color=filt_df['industry']
    
    filtered_df = df.loc[(df['years_to_unicorn'] >= selected_range[0])
                     & (df['years_to_unicorn'] <= selected_range[1])]
    

    fig = px.bar(filtered_df, x=filtered_df['years_to_unicorn'].value_counts().index, y=filtered_df['years_to_unicorn'].value_counts().sort_values(ascending=False),
                 )


    fig.update_layout(
    #title="Plot Title",
    xaxis_title="Number of Years Needed to be a unicorn",
    yaxis_title="Number Of Companies",
    #legend_title="Legend Title"
    )

    return fig






@app.callback(
    Output(component_id='graph_jy',component_property='figure'),
    Input('my-slider_joind_years','value'),
    Input(component_id='DDCTR',component_property='value'),
    Input(component_id='countries_radio',component_property='value'),
    )
def update_joind_years_unicorn(selected_range,DDCTR,RBCTR):
    #line
    filt_df = df
    if (RBCTR == 'Customize'):
        if (DDCTR != None):
            filt_df=df[df['country'].isin(DDCTR)]
    
    
    filtered_col = 'country'
    # Divided by country
    filtered_df = filt_df.loc[(filt_df['year_joined'] >= selected_range[0])
                     & (filt_df['year_joined'] <= selected_range[1])]
    
    df_year_joined= filtered_df.groupby(['year_joined', filtered_col]).count()
    fig = px.line(
        df_year_joined,
        x=df_year_joined.index.get_level_values(0),
        y="company",
        color=df_year_joined.index.get_level_values(1),
        markers=True

    )
    
    fig.update_layout(
    #title="Plot Title",
    xaxis_title="Years",
    yaxis_title="Number Of Companies became Unicorns",
    #legend_title="Legend Title"
    )
    
    return fig




######################  dounut graph  ############################



@app.callback(
    Output(component_id='dounut_G',component_property='figure'),
    Input(component_id='DDI',component_property='value'),    
    Input(component_id='industry_radio',component_property='value'),

)
def update_dounutG(DDI,RBI):
    
    filt_df = df.groupby('industry')[['valuation_in_billions']].sum().reset_index()
    
    if (RBI == 'Customize'):
        if (DDI != None):
            filt_df=filt_df[filt_df['industry'].isin(DDI)]
    
    fig = px.pie(filt_df,values='valuation_in_billions', names='industry',hole=.4,
                )
    fig.update_traces(textposition='outside')
#  height=800,width=800
    
    return(fig)




###################  Map ###########################
f_df = df.groupby(['iso_alpha','country','industry'])[['valuation_in_billions',]].sum().reset_index()





@app.callback(
    Output(component_id='val_Gmap',component_property='figure'),
    Input(component_id='DDI',component_property='value'),
    Input(component_id='industry_radio',component_property='value')
    )
def update_map(DDI_values,RBI):
    #line
    filt_df = f_df
    fig = px.scatter_geo(filt_df, locations="iso_alpha",
                 size=filt_df["valuation_in_billions"],
                 size_max = 55,
                 color = filt_df["industry"],
                 # size of markers, "pop" is one of the columns of gapminder,
                 )
    
    if (RBI == 'Customize'):
        if (DDI_values != None):
            filt_df=f_df[f_df['industry'].isin(DDI_values)]

        fig = px.scatter_geo(filt_df, locations="iso_alpha",
                     size=filt_df["valuation_in_billions"],
                     size_max = 55,
                     color = filt_df["industry"],
                     # size of markers, "pop" is one of the columns of gapminder,
                     )

    fig.update_layout(
        geo = go.layout.Geo(
            resolution = 50,
            showframe = False,
            #landcolor = "green",
            #countrycolor = "red" ,
            #coastlinecolor = "blue",
    
        ),)
    
    return fig



app.server.run()
