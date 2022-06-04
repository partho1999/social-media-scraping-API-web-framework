import numpy as np
import pandas as pd

import re
import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

all_stopwords = stopwords.words('english')
all_stopwords.remove('not')


nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# from google.colab import drive
# drive.mount('/content/drive')

def text_analysis():
  df = pd.read_csv('media/facebook_post.csv')
  #df.shape[0]

  corpus=[]

  for i in range(0, df.shape[0]):
    post = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', str(df['Post'][i]))
    post = post.split("https")[0]
    post = post.lower()
    post = post.split()
    post = [ps.stem(word) for word in post if not word in set(all_stopwords)]
    post = ' '.join(post)
    corpus.append(post)


  df['text'] = corpus

  df['scores'] = df['text'].apply(lambda Text: sid.polarity_scores(Text))

  df = df[['Post','scores']]

  df = pd.concat([df, df['scores'].apply(pd.Series)], axis=1)

  df = df[['Post','neg', 'neu', 'pos', 'compound']]

  df.to_csv("media/analysis.csv")

#text_analysis()
