import pandas as pd
import string
import json
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from preprocess import preprocess

punctuation = list(string.punctuation)
stop=stopwords.words('english')+punctuation+['rt','via','…', '’', '“', '”', '...', 'amp']

count_terms=Counter()
dates=[]

with open('tweets.json','r',encoding='utf-8') as f:
    for line in f:
        tweet = json.loads(line)
        terms=[t for t in preprocess(tweet['text'],lowercase=True)
               if t not in stop and not t.startswith (('#','@','http'))]
        count_terms.update(terms)

        if tweet.get('created_at'):
            dates.append(tweet['created_at'])

top_words=count_terms.most_common(15)
words,counts=zip(*top_words)
plt.figure(figsize=(10,6))
plt.barh(words[::-1],counts[::-1],color='#1DA1F2')
plt.title('Top 15 most frequent terms in Covid-19 Tweets')
plt.xlabel('frequency')
plt.savefig('top_terms_chart.png',dpi=300)
plt.tight_layout()
plt.close()
print("Saved chart 1:top_terms_chart.png")

if dates:
    idx=pd.to_datetime(dates,errors='coerce').dropna()

    if len(idx)>0:
        ones=[1]*len(idx)
        series=pd.Series(ones,index=idx)

        per_day=series.resample('1D').sum().fillna(0)
        plt.figure(figsize=(10,5))
        per_day.plot(color='#E0245E',linewidth=2)
        plt.title('COVID-19 Tweet activity over time')
        plt.xlabel('Date')
        plt.ylabel('Numer of Tweets')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('time_series_chart.png', dpi=300)
        plt.close()
        print("Saved Chart 2: time_series_chart.png")
    else:
        print("Could not parse time stamp for time series chart.")
else:
    print("No 'created_at' timestamps found in tweets.json")



