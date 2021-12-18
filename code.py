import numpy as np
import pandas as pd
import json
import re
import spacy
import spacy_fastlang
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

import plotly.offline as pyo
import plotly.graph_objs as go
# Set notebook mode to work in offline
pyo.init_notebook_mode()
import plotly.express as px


dataset = pd.read_json('result.json', orient='columns')
movie = pd.read_json( ( dataset['messages']).to_json(), orient='index')
movie = movie[['id','date','text']]


#considered only those messages that are 'str' type. Messages of type 'list' are objects containing 'type' and 'text'
#as keys where 'type' = 'link'. Cannot predict sentiment for types such as 'link','mention' etc ,therefore removed those messages.
strng_text = []
for i in range(len(movie)):
    if type(movie['text'].iloc[i]) == str:
        strng_text.append([movie['id'].iloc[i], movie['date'].iloc[i], movie['text'].iloc[i]])
        
movie = pd.DataFrame(strng_text, columns=['id', 'date', 'text'])

#replacing '\n' with blank for future analysis
for sub in range(len(movie)):
    movie['text'].iloc[sub] = movie['text'].iloc[sub].replace("\n", "")

#Messages that mention SHIB or DOGE    
strng_text = []
for i in range(len(movie)):
    strng_text.append(str(movie['date'].iloc[i]) + "+" + movie['text'].iloc[i])

doc = '\n'.join(strng_text)
keywords = [' *shib *',' *doge *']
#keywords = [' *shib *','^shib *', ' *shib.*$',' *doge *','^doge *', ' *doge.*$']
pattern = r'.*\b(?='+'|'.join(keywords) + r')\b.*'
a = re.findall(pattern, doc, re.IGNORECASE)

lis = []
for i in a:
    lis.append(i.split("+",1))
df = pd.DataFrame(lis, columns=["date", "text"])

#messages in english only
en_messages = []
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("language_detector")
for i in range(len(df)):
    doc = nlp(df['text'].iloc[i])
    

    if doc._.language == 'en':
        en_messages.append([df['date'].iloc[i],df['text'].iloc[i]])
df= pd.DataFrame(en_messages, columns =['date','text'])


df['polarity_score'] = ""
df['score_between_-1and1'] = ""
sia = SentimentIntensityAnalyzer()
for i in range(len(df)):
    sc = sia.polarity_scores(df['text'].iloc[i])
    if sc['compound'] > 0.0:
        df['polarity_score'].iloc[i] = 'POSITIVE'
        df['score_between_-1and1'].iloc[i] = sc['compound']
        
    elif sc['compound']  < 0.0:
        df['polarity_score'].iloc[i] = 'NEGATIVE'
        df['score_between_-1and1'].iloc[i] = sc['compound']
        
    else:
        df['polarity_score'].iloc[i] = 'NEUTRAL'
        df['score_between_-1and1'].iloc[i] = sc['compound']

#removing timestamp from DATETIME        
for i in range(len(df)):
    t = df['date'].iloc[i].split(" ")
    df['date'].iloc[i] = t[0]
    
#Analysis   
df['score_between_-1and1'] = df['score_between_-1and1'].astype('float')
messages_per_day = df.groupby(['date']).size()
average_sentiment_per_day = df.groupby(['date']).mean()
plot3 = df.groupby(['date', 'polarity_score']).size()


plot1 = pd.DataFrame(messages_per_day, columns = ['count']).reset_index()
plot2 = pd.DataFrame(average_sentiment_per_day, columns = ['score_between_-1and1']).reset_index()
plot3 = pd.DataFrame(plot3, columns = ['count']).reset_index()


#plotting

#No.of messages per day
fig = px.line(plot1, x="date", y="count", title='No.of messages/ day', markers=True)
fig.show()


#Average Sentiment is between -1 and 1. This is because, compound score is averaged for each day.
                #-1(most extreme negative) and +1 (most extreme positive). 
                #The more Compound score closer to +1, the higher the positivity of the text.
fig = px.line(plot2, x="date", y="score_between_-1and1",labels={
                     "score_between_-1and1": "Average Sentiment",
                     
                 }, title='Average Sentiment/day', markers=True)
fig.show()

#Extra
#Count of each group of sentiment/day
fig = px.bar(plot3, x="date", y="count", color="polarity_score", title="Count of each sentiment group/day",pattern_shape="polarity_score", pattern_shape_sequence=[".", "x", "+"],width=1000, height=800)
fig.show()


#print 'df' to see the dataset
