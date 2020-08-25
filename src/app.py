"""
Dash Application
"""
#-----------------#
# Import packages #
#-----------------#

#Base libraries
import numpy as np
import pandas as pd

#Dash and plotly libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

#----------------------#
#Define style elements #
#----------------------#
# Update default color scheme
pio.templates["my_theme"] = go.layout.Template(
    layout_colorway=['#0AD48B', '#62656B', "#E3008C", "#0078D7", "#107C10", "#E81123", "#5C2D91", "#FF8C00",
                     "#004B1C", "#FFF100"]
)

pio.templates.default = "plotly_white+my_theme"

#Tab style:
tab_style = {'borderBottom': '1px solid #3b5998',
             'text-align': 'center',
             'fontSize': '20px'}
tab_selected_style={'borderTop': '1px solid blue',
                               'backgroundColor': '#3b5998',
                               'color': 'white',
                               'text-align': 'center',
                               'fontSize': '20px'}

#------------------#
# Define Functions #
#------------------#
def create_CAC_stats(goal, CAC_features, group_cols):
    '''
    Input: (goal, list of features to keep in dataset, list of features to sum_by) 
    Output: table of stats to visualize
    '''
    CAC_stats = ads[CAC_features].groupby(group_cols).sum()
    CAC_stats['Customer Acquisition Cost'] = round(CAC_stats["Amount Spent (USD)"]/CAC_stats[goal],2)
    CAC_stats = CAC_stats.reset_index()
    CAC_stats['CAC_pass'] = np.where(CAC_stats['Customer Acquisition Cost'] <= 50, '<= $50', '> $50')
    CAC_stats = CAC_stats.sort_values(by=['CAC_pass', 'Ad Set Name'], ascending = True)
    return(CAC_stats)

#--------------------------------#
# Create and run the application #
#--------------------------------#

#Launch the application
app = dash.Dash(__name__)

#Title the webpage
app.title = 'Facebook Ad Campaign Analysis'

#Define location of file and read in data
url = 'https://raw.githubusercontent.com/gnyirjesy/Ad-Campaign-Dashboard/master/Data/ads_clean.csv?token=ANT6WFW5AHER2YXY6LYUTUC7IRYLE'
ads = pd.read_csv(url, index_col=0)

#Create the app layout
app.layout = html.Div([
    dcc.Tabs([
        #First tab consists of goal count and acquisition cost color coding
        dcc.Tab(label='Goal and Acquisition Cost', children=[
            #First divided section contains the title, selectors, and insights
            html.Div([
                html.H3('Ad Set Overview'),
                html.Label('Choose a goal to examine:'),
                #Include website registrations and leads and exploration options
                dcc.Dropdown(id='goal-drop',
                             options=[
                                 {'label': 'Website Registrations',
                                  'value': 'Website Registrations Completed'},
                                 {'label': 'Website Leads',
                                  'value': 'Website Leads'}],
                             value='Website Registrations Completed',
                             multi=False),
                #Add a selector to examine trends within customer segments
                html.Label('Choose a feature by which to segment:'),
                #Allow user to segment data by gender and age
                dcc.Dropdown(id='feature-drop',
                             options=[
                                 {'label': 'Gender',
                                  'value': 'Gender'},
                                 {'label': 'Age',
                                  'value': 'Age'}],
                             value=[],
                             multi=False),
                html.Div([
                    #Include insights based on which selectors are specified
                    html.H6('Insights:'),
                    html.Div(id='insights-output')]
                    )], className = 'three columns',
                                style={'fontsize' : '14px',
                                       'margin': 'auto',
                                       'padding-right': '5px',
                                       'padding-left': '5px',
                                       'padding-bottom': '280px',
                                        'background-color': '#E5ECF6'}),
            #Add right divider containing the output visual
            html.Div([                    
                html.Div([ 
                    #Visual dynamically updates based on selected values
                    html.Div(id='CAC-output')], className='nine columns',
                    style={'fontsize' : '14px',
                                       'margin': 'auto',
                                       'display': 'inline-block',
                                       'padding-right': '0px',
                                       'backgroundColor': '#E5ECF6'})
                ], className='row')
            ], selected_style=tab_selected_style, style=tab_style),
        #Add tab to show the conversion cycle funnel
        dcc.Tab(label='Conversion Cycle', children=[
            html.Div([
                html.H3('Conversion Cycle'),
                html.P('These graphs track the conversion factor at each step \
                       towards the final goal of website registration. The \
                           full process begins with (1) Impressions to (2) \
                               Link Clicks then (3) Website Leads and finally \
                                   (4) Website Registrations.'),
                html.Label('Choose an ad set:'),
                dcc.Dropdown(id = 'funnel-ad-drop',
                             options=[
                                 {'label': i, 'value': i}
                                 for i in ads['Ad Set Name'].unique()
                                 ],
                             value= 6,
                             multi=False),
                html.Label('Select another ad set for comparison:'),
                dcc.Dropdown(id= 'funnel-ad-drop-2'),
                html.H6('Insights:'),
                html.Label('The conversion factor from impression \
                           to website registrations is on average \
                           0.03% for all campaigns and \
                           ~0.05% for ad sets 6 and 13. \
                           The largest dropoff in the \
                           sales funnel is from impressions to \
                                   link clicks.')
                ], className = 'three columns',
                                   style={'fontsize' : '14px',
                                       'margin': 'auto',
                                       'padding-right': '5px',
                                       'padding-left': '5px',
                                       'padding-bottom': '100px',
                                        'background-color': '#E5ECF6'}),
            html.Div([
                html.Div([
                    html.Div(id= 'funnel-output')],
                    className = 'nine columns',
                    style={'fontsize' : '14px',
                                       'margin': 'auto',
                                       'display': 'inline-block',
                                       # 'padding-bottom': '5px',
                                       'padding-right': '0px',
                                       'backgroundColor': '#E5ECF6'})
                ], className='row')
            ], selected_style=tab_selected_style, style=tab_style)
        ])
    ])
               

#-------------------------#
# Functions for first tab #
#-------------------------#

@app.callback([Output('CAC-output', 'children'),
               Output('insights-output','children')],
              [Input('goal-drop', 'value'),
               Input('feature-drop', 'value')])

def update_CAC(goal, feature):
    '''
    Input: (goal, feature) 
    Output: (dcc.Graph object, html.Label object)
    Callback to update visual on Goal and Acquisition Cost tab based on 
    selector values
    '''
    #If a feature is not specified, output an overview chart without segmentation
    if not feature:
        '''Include the goal and ad set for summation and the amount spent to 
        calculate customer acquisition cost'''
        CAC_features = ["Amount Spent (USD)", goal, 'Ad Set Name']
        #Run function to create data table for visual
        CAC_stats = create_CAC_stats(goal, CAC_features, 'Ad Set Name')
        
        '''Create figure including bar chart with count of "goal" as the y 
        value and ad set as the x value. Add color coding to specify if ad set
        hit the customer acquisition cost goal of $50 or less.'''
        fig = px.bar(CAC_stats, x="Ad Set Name", color='CAC_pass',
             y=goal,
             height=690,
             width = 1150,
             hover_data = {'Ad Set Name': True,
                          goal: True,
                          'Customer Acquisition Cost': ':$,.2f',
                          'CAC_pass': False}
            )
        #Update style of chart
        fig.update_layout(xaxis=dict(title='Ad Set Name',
                                      tick0 = 1,
                                      dtick = 1,
                                      showticklabels= True),
                           yaxis=dict(title=' '.join(['Total',goal]),
                                      gridcolor='#E5ECF6'),
                           title=dict(text=' '.join(['Total',goal]), 
                                      x=0.5),
                           legend=dict(title=dict(text='Cost'),
                                        yanchor="bottom",
                                        y=.85,
                                        xanchor="right",
                                        x=.98),
                           showlegend=True,
                           plot_bgcolor='rgba(0,0,0,0)',
                           # keep the original annotations and add a list of new annotations:
                           annotations = list(fig.layout.annotations) + 
                            [go.layout.Annotation(
                                    x=1,
                                    y=1,
                                    font=dict(size=14),
                                    showarrow=False,
                                    text='Acquisition Cost: ',
                                    xref="paper",
                                    yref="paper"
                                )
                            ]
                        )
        #speicify insights based on selected goal
        if goal == 'Website Registrations Completed':
            insight_text = f'Ad sets 6 and 13 have the most {goal} and a \
                customer acquisition cost of $50 or less. Additionally, less \
                    than 25% of ad sets have a customer acquisition cost \
                        of $50 or less.'.format(goal)
        else:
            insight_text = f'Ad sets 13 and 6 have the most {goal} and a \
                customer acquisition cost of $50 or less.'.format(goal)
    #If a feature is selected, create a visual segmented by selected feature
    elif feature:
        #Specificy important colujmns for grouping and summation
        CAC_features = ["Amount Spent (USD)", goal, feature, 'Ad Set Name']
        #Create data table for visual
        CAC_stats = create_CAC_stats(goal, CAC_features, ['Ad Set Name', feature])
        
        #Determine the count towards goal for each segements within the feature 
        feature_stats = CAC_stats[[goal, feature]].groupby(feature).sum()
        #Remove segments of feature that do no have any count towards target goal
        remove_features = [feature_stats.index[row] for row in 
                 range(len(feature_stats[goal]))
                 if feature_stats[goal][row] == 0]
        CAC_stats = CAC_stats[~CAC_stats[feature].isin(remove_features)]
        
        #Define category ordering, and insights based on selected feature and goal
        if feature == 'Gender':
            gender_list = ['female', 'male', 'unknown']
            gender_list_new = [item for item in gender_list if item not in remove_features]
            cat_order = {'Gender': gender_list_new}
            if goal == 'Website Registrations Completed':
                insight_text = f'Ad set 6 has some of the most {goal} and has \
                    a customer acquisition cost of $50 or less across \
                    all genders. Ad set 6 also performs similarly across the \
                        male and female populations. Ad set 13 has the most \
                            {goal} with the male population, but does not \
                                perform as well with females. Ad set 24 \
                                    performs relatively well with both \
                                        females and males, but has a customer \
                                        acquisition cost over $50.'.format(goal)
            else:
                insight_text = f'Ad sets 6 and 13 are in the top 3 performing \
                    ad sets for {goal} across all genders. Ad set 33 achieves \
                        a high number of {goal} for males, but has a significant \
                            drop off in number of {goal} for females and \
                                unknown'.format(goal)
        elif feature == 'Age':
            age_list = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
            age_list_new = [item for item in age_list if item not in remove_features]
            cat_order = {'Age': age_list_new}
            if goal == 'Website Registrations Completed':
                insight_text = f'Customers within age groups of 18-24 and 45+ \
                    did not have any {goal}. Within \
                        the age groups that did have {goal}, ad sets 6 and 13\
                        continued to outperform the other ad sets. However,  \
                    ad set 13 did have a customer acquisition cost over $50 \
                        for the age group of 35-44.'.format(goal.lower())
            else:
                insight_text = f'Customers within age groups of 18-24 and 45+ \
                    did not have any {goal}. Within \
                        the age groups that did have {goal}, ad sets 6 and 13\
                        continued to outperform the other ad sets.'.format(goal)
                        
        '''Create the bar chart with the count towards goal as the y axis, ad 
        set as the x axis, and customer acquisition cost color coding, and 
        subplots for each feature segment'''
        
        fig = px.bar(CAC_stats, x='Ad Set Name', y=goal,
                     color='CAC_pass', facet_col=feature,
                     facet_col_wrap=1, category_orders=cat_order, 
                     hover_data = {'Ad Set Name': True,
                                   feature: True,
                                   goal: True,
                                   'Customer Acquisition Cost': ':$,.2f',
                                   'CAC_pass': False})
        #Create loop to remove redundant y axis labels
        for i in range(2, len(CAC_stats[feature].unique())+1):
            update_yaxis = ''.join(['yaxis', str(i)])
            fig['layout'][update_yaxis]['title']['text'] = ''
        #Update stylist elements of chart
        fig.update_layout(xaxis=dict(title='Ad Set Name',
                                      tick0 = 1,
                                      dtick = 1,
                                      showticklabels= True),
                            yaxis=dict(title=''),
                            title=dict(text=' '.join(['Total',goal]), 
                                      x=0.5),
                            legend=dict(title=dict(text='Cost'), orientation='h',
                                        yanchor="bottom",
                                        y=1.01,
                                        xanchor="right",
                                        x=1),
                            showlegend=True,
                            height = 690,
                            width = 1150,
                            plot_bgcolor='rgba(0,0,0,0)')
        #Remove unneccesary text for each subplot title
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].title()))
        fig.update_layout(
            # keep the original annotations and add a list of new annotations:
            annotations = list(fig.layout.annotations) + 
            #Add overall y axis title for entire plot
            [go.layout.Annotation(
                    x=-0.05,
                    y=0.5,
                    font=dict(size=14),
                    showarrow=False,
                    text=' '.join(['Total',goal]),
                    textangle=-90,
                    xref="paper",
                    yref="paper"
                )
            ] +
            #Add legend title
            [go.layout.Annotation(
                    x=.825,
                    y=1.057,
                    font=dict(
                        size=14
                    ),
                    showarrow=False,
                    text='Acquisition Cost: ',
                    xref="paper",
                    yref="paper"
                )
            ]
        )
        #Add notation to bottom of chart for feature segments with zero goal count
        if len(remove_features) > 0:
            fig.update_layout(
                annotations = list(fig.layout.annotations) + 
                [go.layout.Annotation(
                        x=1,
                        y=-.1,
                        font=dict(
                            size=10
                        ),
                        showarrow=False,
                        text=' '.join(['*',feature,
                                       ', '.join(remove_features),
                                       'have zero', goal]),
                        xref="paper",
                        yref="paper"
                    )
                ])
    return(dcc.Graph(id='CAC-1', figure=fig), 
           html.Label(insight_text))

#--------------------------#
# Functions for second tab #
#--------------------------#

@app.callback([Output('funnel-ad-drop-2', 'options'),
               Output('funnel-ad-drop-2', 'value')],
              [Input('funnel-ad-drop', 'value')])

def update_second_drop(ad_set):
    '''
    Function to update the second add set drop-down
    Input: selection from first ad set drop-down
    Output: drop-down options excluding ad set selected in first drop-down
    '''
    options = [{'label': i, 'value': i}
               for i in ads['Ad Set Name'].unique() if i != ad_set]
    value = []
    return options, value
                       
                       
@app.callback(Output('funnel-output', 'children'),
              [Input('funnel-ad-drop', 'value'),
               Input('funnel-ad-drop-2', 'value')])

def update_funnel(ad_set1, ad_set2):
    '''
    Function to update funnel visual based on ad set selections
    Input: (first ad set selection, optional: second ad set selection)
    Output: Funnel visualization
    '''
    
    #Identify features to include in funnel visual
    funnel_features = ["Impressions", "Link Clicks", "Website Leads",
                       "Website Registrations Completed", 'Ad Set Name']
    #If only one ad set is selected, update chart title accordingly
    if not ad_set2:
        selected_ads = [ad_set1]
        title = 'Ad Set ' + str(ad_set1) + ' Conversion Cycle'
    #If two ad sets are selected, update chart title accordingly
    else:
        selected_ads = [ad_set1, ad_set2]
        title = 'Comparison of Ad Sets ' + str(ad_set1) + ' & ' \
            + str(ad_set2) + ' Conversion Cycles'
    
    #Filter data to only include ad sets selected with drop-downs
    data = ads[ads['Ad Set Name'].isin(selected_ads)]
    #Group data by ad set name and sum
    data = data[funnel_features].groupby('Ad Set Name').sum()
    #Define figure layout
    layout = go.Layout(title=dict(text=title, x=0.6),
                       legend_title_text='Ad Set')
    fig = go.Figure(layout=layout)
    #Add funnel plot to figure for first add set
    fig.add_trace(go.Funnel(
        name = ad_set1,
        y = data.loc[ad_set1,:].index,
        x = data.loc[ad_set1,:].values,
        textinfo = "value+percent initial"))
    #If second ad set is selected, add another trace to figure for that set
    if len(selected_ads) > 1:
        fig.add_trace(go.Funnel(
            name = ad_set2,
            y = data.loc[ad_set2,:].index,
            x = data.loc[ad_set2,:].values,
            textinfo = "value+percent initial"))
    return(dcc.Graph(id='funnel-1', figure=fig))

#Add server clause
if __name__ == '__main__':
    app.run_server(debug=True)