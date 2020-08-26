#!/usr/bin/env python
# coding: utf-8

# # EDA and Data Cleaning for Ad Campaign Success Analysis
# This script is used to perform preliminary EDA and data cleaning on the Facebook ad campaign data set.

# In[1]:


#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from plotly import graph_objects as go


# In[5]:


#Import data
url = 'https://raw.githubusercontent.com/gnyirjesy/Ad-Campaign-Dashboard/master/Data/QA%20HW%20Data.csv'
ads = pd.read_csv(url)


# In[6]:


#Preview data
ads.head()


# In[7]:


#Since we are focusing on ad campaign success, identify how many unique ad campaigns are included in data
len(ads['Ad Set Name'].unique())


# In[18]:


#Define function to find n/a columns 
def find_na_cols(df):
    '''
    Find columns that contain any n/a values
    find_na_cols(df) --> list of columns that contain n/a
    '''
    return(df.isna().any()[lambda x:x])

get_ipython().run_line_magic('matplotlib', 'inline')

def stacked_bar(df, x_var, category, values):
    '''
    Function to create a stacked bar chart with given x_var on x-axis, category as color coding,
    and values as summed feature on y-axis.
    '''
    ax = pd.crosstab(df[x_var], df[category], values = df[values], aggfunc=sum, margins=True)
    ax = ax.sort_values(by='All', ascending=False)
    ax = ax.drop('All', axis=1)
    ax = ax.drop('All', axis=0)
    ax.plot.bar(stacked=True)      


# In[8]:


#View information on features and data types
ads.info()


# In[16]:


#Find all columns that contain n/a's
find_na_cols(ads)


# In[13]:


#Some of the columns containing n/a's can be imputed to zero:
impute_to_zero_cols = ['Link Clicks', 'Website Registrations Completed', 'Website Leads', 'Post Shares',
                       'Post Comments', 'Post Reactions']
ads[impute_to_zero_cols] = ads[impute_to_zero_cols].fillna(0)


# In[17]:


#Confirm all columns identified were imputed to zero
find_na_cols(ads)


# In[38]:


#Examine rows where the 'Link Clicks' contain 'n/a' to determine how to impute
ads[ads['Link Clicks'].isna()].head()


# In[39]:


#Examine summary statistics for numeric columns
ads.describe()


# In[49]:


#View how many age groups are included
ads['Age'].unique()


# In[50]:


#View how many genders are included
ads['Gender'].unique()


# In[25]:


#Remove the 'Ad Set' string from the ad set name
ads['Ad Set Name'] = ads['Ad Set Name'].apply(lambda x: x.replace('Ad Set ',''))


# In[19]:


#Experiment with crosstabs across age and gender to examine conversion percent
x = pd.crosstab(ads['Age'], ads['Gender'], values = ads['Website Registrations Completed'], aggfunc=sum, margins=True)
x
x = ads[['Website Registrations Completed', 'Impressions', 'Gender', 'Age']].groupby(['Age','Gender']).sum()
x['conversion_percent'] = round(x['Website Registrations Completed']/x['Impressions']*100,2)
x = x.drop(['Website Registrations Completed', 'Impressions'], axis=1)
x.unstack('Gender')


# In[21]:


#Create stacked bar chart to look at the number of website registrations completed by each gender within an ad set
stacked_bar(ads, 'Ad Set Name', 'Gender', 'Website Registrations Completed')


# In[22]:


#Create stakced bar chart to examine website registrations completed by different age groups for each ad set
stacked_bar(ads, 'Ad Set Name', 'Age', 'Website Registrations Completed')


# In[27]:


#Find the values for the funnel inputs
funnel_features = ["Impressions", "Link Clicks", "Website Leads", "Website Registrations Completed", 'Ad Set Name']
funnel_stats = ads[funnel_features].groupby('Ad Set Name').sum()
funnel_stats.head()


# In[28]:


data = funnel_stats.loc['13',:]


# In[29]:


#Examine conversion cycle funnel for ad set 13
fig = go.Figure(go.Funnel(x=data.values, y=data.index, textinfo = "value+percent initial"))
fig.show()


# Now that I have a general idea for the data, I will extract the data and create the dashboard to include an interactive analysis of the ad set performance.
