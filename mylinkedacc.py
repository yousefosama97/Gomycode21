# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:31:18 2021

@author: Yousef_Hanna
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 10:12:06 2021
@author: Yousef_Hanna
"""
import dash                              
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
from dash_extensions import Lottie       
import dash_bootstrap_components as dbc 
import plotly.express as px              
import pandas as pd                      
from datetime import date
import calendar
from wordcloud import WordCloud


# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets9.lottiefiles.com/private_files/lf30_5ttqPi.json"
url_companies = "https://assets9.lottiefiles.com/packages/lf20_EzPrWM.json"
url_msg_in = "https://assets9.lottiefiles.com/packages/lf20_8wREpI.json"
url_msg_out = "https://assets2.lottiefiles.com/packages/lf20_Cc8Bpg.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


# Import App data from csv sheets **************************************
df_cnt = pd.read_csv("C:/Users/Yousef Hanna/Desktop/Data/Connections.csv")
df_cnt["Connected On"] = pd.to_datetime(df_cnt["Connected On"])
df_cnt["month"] = df_cnt["Connected On"].dt.month
df_cnt['month'] = df_cnt['month'].apply(lambda x: calendar.month_abbr[x])

df_invite = pd.read_csv("C:/Users/Yousef Hanna/Desktop/Data/Invitations.csv")
df_invite["Sent At"] = pd.to_datetime(df_invite["Sent At"])

df_msg = pd.read_csv("C:/Users/Yousef Hanna/Desktop/Data/messages.csv")
df_msg["DATE"] = pd.to_datetime(df_msg["DATE"])


# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardImg(src='C:/Users/Yousef Hanna/Desktop/Data/linkdin.png')
            ],className='mb-2'),
            dbc.Card([
                dbc.CardBody([
                    dbc.CardLink("My Account", target="_blank",
                                 href="https://www.linkedin.com/in/yousef-osama/"
                    )
                ])
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.DatePickerSingle(
                        id='my-date-picker-start',
                        date=date(2019, 1, 1),
                        className='ml-5'
                    ),
                    dcc.DatePickerSingle(
                        id='my-date-picker-end',
                        date=date(2021, 4, 4),
                        className='mb-2 ml-2'
                    ),
                ])
            ], color="info", style={'height':'18vh'}),
        ], width=8),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Connections'),
                    html.H2(id='content-connections', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Companies'),
                    html.H2(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Invites received'),
                    html.H2(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="53%", height="53%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Invites sent'),
                    html.H2(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
], fluid=True)


# Updating the 5 number cards ******************************************
@app.callback(
    Output('content-connections','children'),
    Output('content-companies','children'),
    Output('content-msg-in','children'),
    Output('content-msg-out','children'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_small_cards(start_date, end_date):
    # Connections
    dff_c = df_cnt.copy()

    dff_c = dff_c[(dff_c['Connected On']>=start_date) & (dff_c['Connected On']<=end_date)]
    conctns_num = len(dff_c)
    compns_num = len(dff_c['Company'].unique())

    # Invitations
    dff_i = df_invite.copy()
    dff_i = dff_i[(dff_i['Sent At']>=start_date) & (dff_i['Sent At']<=end_date)]
    # print(dff_i)
    in_num = len(dff_i[dff_i['Direction']=='INCOMING'])
    out_num = len(dff_i[dff_i['Direction']=='OUTGOING'])

    return conctns_num, compns_num, in_num, out_num


# Line Chart ***********************************************************
@app.callback(
    Output('line-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_line(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]
    dff = dff[["month"]].value_counts()
    dff = dff.to_frame()
    dff.reset_index(inplace=True)
    dff.rename(columns={0: 'Total connections'}, inplace=True)

    fig_line = px.line(dff, x='month', y='Total connections', template='ggplot2',
                  title="Total Connections by Month Name")
    fig_line.update_traces(mode="lines+markers", fill='tozeroy',line={'color':'blue'})
    fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig_line


# Bar Chart ************************************************************
@app.callback(
    Output('bar-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_bar(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]

    dff = dff[["Company"]].value_counts().head(6)
    dff = dff.to_frame()
    dff.reset_index(inplace=True)
    dff.rename(columns={0:'Total connections'}, inplace=True)
    # print(dff_comp)
    fig_bar = px.bar(dff, x='Total connections', y='Company', template='ggplot2',
                      orientation='h', title="Total Connections by Company")
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_bar.update_traces(marker_color='blue')

    return fig_bar


# Pie Chart ************************************************************
@app.callback(
    Output('pie-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)

# Word Cloud ************************************************************
@app.callback(
    Output('wordcloud','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_pie(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff.Position[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)].astype(str)

    my_wordcloud = WordCloud(
        background_color='white',
        height=275
    ).generate(' '.join(dff))

    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2',
                              title="Total Connections by Position")
    fig_wordcloud.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    return fig_wordcloud


if __name__=='__main__':
    app.run_server(debug=False, port=8004)