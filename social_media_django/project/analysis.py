def text_analysis():
    import numpy as np
    import pandas as pd
    import re
    import nltk

    df = pd.read_csv('media/Facebook_post.csv')
    #print(df)

 

    df.columns

    print(df.shape[0])

    df.head()

    import re
    import nltk

    nltk.download('stopwords')

    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()

    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')

    corpus=[]

    for i in range(0, 42):
        post = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', df['Post'][i])
        post = post.split("https")[0]
        post = post.lower()
        post = post.split()
        post = [ps.stem(word) for word in post if not word in set(all_stopwords)]
        post = ' '.join(post)
        corpus.append(post)

    df['post'] = corpus
    df.head()

    import nltk
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()

    df['scores'] = df['post'].apply(lambda Text: sid.polarity_scores(Text))
    df.head()

    df = df[['Post','scores']]

    df

    df = pd.concat([df, df['scores'].apply(pd.Series)], axis=1)

    df = df[['Post','neg', 'neu', 'pos', 'compound']]

    df
    df.to_csv("media/analysis-text.csv")


text_analysis()