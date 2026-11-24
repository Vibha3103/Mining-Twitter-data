import json 
import string
from collections import Counter
import nltk
from nltk.corpus import stopwords
from preprocess import preprocess

#download nltk
nltk.download('stopwords',quiet=True)

#Define stopwords,punctuations,common twitter artifacts
punctuation=list(string.punctuation)
stop=stopwords.words('english')+punctuation+['rt','via','...','’', '“', '”', '...', 'amp']

count_all=Counter()
count_mentions=Counter()
count_hashtags=Counter()
count_terms_only=Counter()

with open('tweets.json','r',encoding='utf-8') as f:
    for line in f:
        tweet=json.loads(line)

        #All tokens excluding stopwords
        terms_stop = [term for term in preprocess(tweet['text'],lowercase=True)
                      if term not in stop and not term.startswith('http')]

        #Hashtags only
        terms_hash = [term for term in terms_stop if term.startswith('#')]

        #Mentions only
        terms_mentions = [term for term in terms_stop if term.startswith('@')]
        
        # 4. Plain words only (no hashtags, no mentions)
        terms_only = [term for term in terms_stop if not term.startswith(('#', '@'))]

        count_all.update(terms_stop)
        count_hashtags.update(terms_hash)
        count_mentions.update(terms_mentions)
        count_terms_only.update(terms_only)

print("--- Top 10 Overall Terms ---")
for word, count in count_all.most_common(10):
    print(f"{word}: {count}")

print("\n--- Top 10 Hashtags ---")
for tag, count in count_hashtags.most_common(10):
    print(f"{tag}: {count}")

print("\n--- Top 10 Mentions ---")
for user, count in count_mentions.most_common(10):
    print(f"{user}: {count}")

print("\n--- Top 10 Plain Words ---")
for word, count in count_terms_only.most_common(10):
    print(f"{word}: {count}")
