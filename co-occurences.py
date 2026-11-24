import json 
import string 
import operator
from collections import defaultdict
from nltk.corpus import stopwords
from preprocess import preprocess

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', '…', '’', '“', '”', '...', 'amp']

com=defaultdict(lambda:defaultdict(int))

with open('tweets.json','r',encoding='utf-8') as f:
    for line in f:
        tweet=json.loads(line)

        #Exctract clean words only
        terms_only=[
               term
                for term in preprocess(tweet['text'],lowercase='True')
                    if term not in stop
                    and not term.startswith(('#','@','http'))
        ]

        #Build co-occurence matrix
        for i in range(len(terms_only)-1):
            for j in range(i+1,len(terms_only)):
                w1,w2=sorted([terms_only[i],terms_only[j]])
                if w1!=w2:
                    com[w1][w2]+=1

#find 10 most frequent words pair overall
com_max=[]
for t1 in com:
    t1_max_terms=sorted(com[t1].items(),key=operator.itemgetter(1),reverse=True)[:5]
    for t2,t2_count in t1_max_terms:
        com_max.append(((t1,t2),t2_count))

terms_max=sorted(com_max,key=operator.itemgetter(1),reverse=True)

print("---Top-10 co-occuring word pairs---")
for pair,count in terms_max[:10]:
    print(f"{pair[0]}+{pair[1]}:{count}")


#Words most assosciated with a specific search term 
search_word='covid'
if search_word in com:
    count_search = sorted(com[search_word].items(),key=operator.itemgetter(1),reverse=True)
    print(f"\n---top 10 words co-occuring with '{search_word}' ---")
    for word,count in count_search[:10]:
        print(f"{word}:{count}")
else:
    print(f"\n'{search_word}' not found as primary key.Try chnaging search_word to another top term.")
    
