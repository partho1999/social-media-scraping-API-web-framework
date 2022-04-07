from . tokens import generate_token
import os
import json
import pandas as pd
from wordcloud import WordCloud
from analysis import *
from word_cloud import *

from nltk import tokenize
from operator import itemgetter
import math
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english'))

def sentiment_analysis():
    data = pd.read_csv()    
    data.isna().sum()
    #Removing NaN Values
    data.dropna(inplace = True)


    neg_avg = data["neg"].mean()
    neu_avg = data["neu"].mean()
    pos_avg = data["pos"].mean()

    avg =[neg_avg, neu_avg, pos_avg]
    print(avg)

    word_cloud()


    #2. Loading Data
    doc_csv = pd.read_csv('media/analysis.csv')
    #take it to list
    doc_list = doc_csv['Post'].tolist()
    #print(doc_list)
    #Convert Data list to str
    doc = ''.join(str(e) for e in doc_list)

    #3. Remove stopwords
    #4. Find total words in the document 
    total_words = doc.split()
    total_word_length = len(total_words)
    #print(total_word_length)

    #5. Find the total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    #print(total_sent_len)

    #6. Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        each_word = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', each_word)
        
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
    #print(tf_score)

    #7. Function to check if the word is present in a sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    #8. Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    #print(idf_score)

    #9. Calculate TF * IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    #print(tf_idf_score)

    #10. Create a function to get N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result
    #11. Get the top 5 words of significance
    print(get_top_n(tf_idf_score, 10))

    dic = get_top_n(tf_idf_score, 10)

    df=pd.DataFrame()
    df['Keyword']=dic.keys()
    df['Score']=dic.values()

    #print(df)

    df_label = df['Keyword'].tolist()
    df_score = df['Score'].tolist()

    print(df_label)
    print(df_score)    
    