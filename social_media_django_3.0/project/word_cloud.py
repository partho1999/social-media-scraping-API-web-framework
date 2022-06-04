import pandas as pd
import numpy as np
from wordcloud import WordCloud


def word_cloud():
    df = pd.read_csv('media/analysis.csv')

    df.isna().sum()
    #Removing NaN Values
    df.dropna(inplace = True)


    neg_avg = df["neg"].mean()
    neu_avg = df["neu"].mean()
    pos_avg = df["pos"].mean()

    avg =[neg_avg, neu_avg, pos_avg]
    print(avg)

    # df.isna().sum()
    #Removing NaN Values
    # df.dropna(inplace = True)
    #Creating the text variable
    text = " ".join(cat.split()[1] for cat in df.Post)
    # Creating word_cloud with text as argument in .generate() method
    word_cloud = WordCloud(collocations = False, background_color = 'black').generate(text)
    word_cloud.to_file('static/img/image.png')


