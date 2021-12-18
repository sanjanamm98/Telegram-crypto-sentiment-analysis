# Telegram-crypto-sentiment-analysis
Sentimental analysis using Telegram's 'crypto' group text messages 

## **Language Used:**

Python 3.8.8

## **Requirements:**

Mentioned in requirements.txt

## **Introduction**

Sentimental Analysis is a powerful marketing tool and extremely useful in monitoring social media and understanding emotions/opinions behind every comment. It is an essential factor when it comes to customer satisfaction, advertising, current trend, understanding product success etc. 

## **Project Description**

In this project, I aim to crawl messages from telegram's crypo group for a certain duration, compute sentiment scores, analyze and plot data using plotly visualization library to understand average sentiments. 


## **Process:**
- Data craweling
- Preprocess
- Compute Sentimental score
- Analysis & plotting

## **Project Breakdown**

1) I crawl data from the 'crypto' group on telegram (May 1 2021 - May 15 2021) and export the data as JSON. 
2) During preprocessing, non-english messages are removed using 'SpaCy' library. Only data that is of type 'text' is considered. Any links, mentions (tags), photos etc are excluded. Also, only messages that mention 'SHIB' or 'DOGE' coins are considered.
3) Using NLTK's pretrained sentiment analyzer called 'VADER', I compute sentiment scores for each message. 'Compound score' is used to calculate the sentiment score of each message (compound score explained in Results & Findings section)
4) Data is plotted to analyze average sentiments per day. 

## **Choice of Python Packages:**

#### **SpaCy**
SpaCy is a python library used in some Natural language processing tasks. It deloys a 'spacy_langdetect' library model in a SpaCy NLP pipeline. 
I choose SpaCy library to remove non-english messages because of its good prediction accuracy with short messages. Since, most of the messages were short, this library gave good results. SpaCy returns detected language and accuracy in the detect_language variable. SpaCy does not work very well with sentences containing multiple languages. In this case, it returns detected language of the longer sentences. But, multiple language was not an issue with our data. 
Alternatively, Pycld2 can be used when there are multiple languages in a sentence. 
However, comparing SpaCy and Pycld2, SpaCy gave better results for our data.

#### **NLTK's pretrained sentiment analyzer called 'VADER'**
'VADER' is a rule-based sentiment analysis tool which are generally labeled according to their semantic orientation as either positive or negative. VADER not only tells about the Positivity and Negativity score but also tells us about how positive or negative a sentiment is (percentage).
Since VADER is pretrained, results can be generated quickly than many other analyzers. However, VADER is best suited for language used in social media, like short sentences with some slang and abbreviations. It’s less accurate when rating longer, structured sentences but this doesn't affect the data used for this project. 

## **Results & Findings**
1) From the analysis, it can be concluded that the average sentiment on each day is between neutral and positive (mostly neutral) towards SHIB and DOGE coins. 'Compound' score from VADER is used to calculate the sentiment of each message. The compound score is the sum of positive, negative & neutral scores which is then normalized between -1(most extreme negative) and +1 (most extreme positive). The compound score is averaged/ per day and the results are slightly greater than 0 (neutral to positive). This is shown in the plot named 'average_sentiment_per_day.png'

2) No.of messages/per day was plotted to get an idea of how the data was distributed. This is shown in the plot named 'no_of_messages_per_day.png'

3) Count of each sentiment group (Positive, Negative, Neutral) was plotted for each day. It can be concluded that most messages had a neutral response to SHIB and DOGE coins, followed by positive reactions. Comparatively, very few negative comments except on May 8 2021 and May 10 2021 when positive and negative responses were almost proportional. This is true people's opinion which shows that majority favour SHIB and DOGE coins in crypto. This is shown in the plot named 'count_of_each_sentiment_group_per_day.png'


## **Instructions**
- requirements.txt contains all the packages and versions required to run the project.
- To run the project, execute run.py file. It will result in 3 plots whose screenshots are added to the repository. 'df' can be printed to see the dataset.
- result.json contains the crawled data in JSON format that was used for analysis using python. 
