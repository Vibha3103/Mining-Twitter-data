from collections import Counter, defaultdict
import json
import math
import operator
import re
import string
from nltk.corpus import stopwords
from preprocess import preprocess

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', '…', '’', '“', '”']

fname = 'tweets.json'
count_stop_single = Counter()
com = defaultdict(lambda: defaultdict(int))
n_docs = 0

with open(fname, 'r', encoding='utf-8') as f:
  for line in f:
    line = line.strip()
    if not line:
      continue
    tweet = json.loads(line)
    text = tweet.get('text') or tweet.get('original_text', '')
    if not text:
      continue

    n_docs += 1
    terms_only = list(
        set([
            term
            for term in preprocess(text)
            if term not in stop and not term.startswith(('http',))
        ])
    )
    count_stop_single.update(terms_only)

    for i in range(len(terms_only) - 1):
      for j in range(i + 1, len(terms_only)):
        w1, w2 = sorted([terms_only[i], terms_only[j]])
        if w1 != w2:
          com[w1][w2] += 1

p_t = {}
p_t_com = defaultdict(lambda: defaultdict(int))

for term, n in count_stop_single.items():
  p_t[term] = n / n_docs
  for t2 in com[term]:
    p_t_com[term][t2] = com[term][t2] / n_docs


positive_vocab = [
    'good', 'nice', 'great', 'awesome', 'outstanding',
    'fantastic', 'terrific', ':)', ':-)', 'like', 'love',
    'safe', 'recover', 'recovered', 'vaccine', 'hope', 'support'
]

negative_vocab = [
    'bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(',
    'death', 'deaths', 'died', 'sick', 'crisis', 'panic', 'lockdown', 'fear'
]

pmi = defaultdict(lambda: defaultdict(int))
for t1 in p_t:
  for t2 in com[t1]:
    denom = p_t[t1] * p_t[t2]
    if denom > 0 and p_t_com[t1][t2] > 0:
      pmi[t1][t2] = math.log2(p_t_com[t1][t2] / denom)

semantic_orientation = {}
for term, n in p_t.items():
  positive_assoc = sum(pmi[term][tx] for tx in positive_vocab)
  negative_assoc = sum(pmi[term][tx] for tx in negative_vocab)
  semantic_orientation[term] = positive_assoc - negative_assoc

semantic_sorted = sorted(
    semantic_orientation.items(), key=operator.itemgetter(1), reverse=True
)

print('Top 10 Positive Terms:')
print(semantic_sorted[:10])

print('\nTop 10 Negative Terms:')
print(semantic_sorted[-10:])

sample_terms = ['#covid19', 'covid', 'vaccine', 'lockdown', 'mask']
print('\nSpecific Term Scores:')
for t in sample_terms:
  if t in semantic_orientation:
    print(f'{t}: {semantic_orientation[t]:.4f}')
