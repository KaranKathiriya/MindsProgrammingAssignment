# -*- coding: utf-8 -*-
"""TelegramAnalysis.py

MINDS PROGRAMMING ASSIGNMENT

"""

import pandas as pd
import json
import nltk
from langdetect import detect
from textblob import TextBlob
import numpy as np
import plotly.express as px
from tqdm import tqdm

# load data using Python JSON module
with open('result.json','r') as f:
    data = json.loads(f.read())

# Flatten data
df_nested_list = pd.json_normalize(data, record_path =['messages'])
df_nested_list = df_nested_list[['date','text']]

# Formatting date
df_nested_list['Date'] = pd.to_datetime(df_nested_list['date']).apply(lambda x: x.date())
df_nested_list.drop(['date'],inplace=True,axis=1)
df_nested_list

df_nested_list

def preProcess(msg):
    cleanedMsg=""
    for i in msg:
        if(type(i) is str):
            cleanedMsg+=i
        else:
            cleanedMsg+=""
            
    return cleanedMsg

df_nested_list['text'] = df_nested_list['text'].apply(lambda x: preProcess(x))
df_nested_list

# Funtion to remove messagaes that are Non-english and doesn't have SHIB or DOGE in them
def removeNonEn(text):
    try:
        lang = detect(text)
        if lang == 'en' :
            if("SHIB" in text or "DOGE" in text):
                return text
            else:
                return None
        else:
            return None
    except:
        return None

tqdm.pandas()
df_nested_list['text'] = df_nested_list['text'].progress_apply(lambda x: removeNonEn(x))
df_nested_list

df_nested_list.dropna(inplace=True)

# Analysing Sentiments per message
df_nested_list["sentiment_score"] = df_nested_list["text"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
df_nested_list["sentiment"] = np.select([df_nested_list["sentiment_score"] < 0, df_nested_list["sentiment_score"] == 0, df_nested_list["sentiment_score"] > 0],
                           ['negative', 'neutral', 'positive'])

sentimentCount = df_nested_list.groupby(['Date', 'sentiment']).size().to_frame(name = 'count').reset_index()
sentimentCount

# Bar Graph Showing count of each sentiment per day
fig = px.bar(sentimentCount, x="Date", y="count", color="sentiment")
fig.show()