# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app
import pandas as pd
from io import BytesIO
from wordcloud import WordCloud
import base64
YouTube_Recommender = pd.read_csv('./assets/YouTube_Recommender_3.csv')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predictions

            Content Creator Recommendations: Slide to the right for tag examples of terms used in more higly rated videos.

            """
        ),
    ],
    md=4,
)

column2 = dbc.Col(
    [   dcc.Markdown(
                    """
                    #### Tags Count
                    """),

        dcc.Slider(
                    id = 'percentile_slider',
                    min=0,
                    max=1,
                    step=None,
                    marks={
                        0: 'All Tags',
                        0.1: 'Top 90',
                        0.2: 'Top 80%',
                        0.3: 'Top 70%',
                        0.4: 'Top 60%',
                        0.5: 'Top 50%',
                        0.6: 'Top 40%',
                        0.7: 'Top 30%',
                        0.8: 'Top 20%',
                        0.9: 'Top 10%'     
        },
        value=0.1),
        html.Img(
                id="image_wc", 
                style={
                'display': 'block',
                'margin-left': 'auto',
                'margin-right': 'auto'})
    ]
)  

def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='black', width=600, height=500)
    wc.fit_words(d)
    return wc.to_image()
@app.callback(
    Output('image_wc', 'src'), 
[Input('percentile_slider', 'value'), 
 Input('image_wc', 'id')])
def make_image(percentile, b):
    df = YouTube_Recommender[(YouTube_Recommender['Percentile Rank'] >=percentile)&(YouTube_Recommender['tags']!='[none]')]
    df_cnt = df[['tags', 'counts']]
    img = BytesIO()
    plot_wordcloud(data=df_cnt).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
layout = dbc.Row([column1, column2])