import pandas as pd

df = pd.read_csv('Covid-19 Twitter Dataset.csv')
print("Columns in dataset:", df.columns.tolist())

rename_map = {}
if 'original_text' in df.columns:
    rename_map['original_text'] = 'text'
elif 'clean_tweet' in df.columns:
    rename_map['clean_tweet'] = 'text'

df = df.rename(columns=rename_map)

df = df.dropna(subset=['text'])

possible_columns = [
    'created_at', 'text', 'Location', 'place', 
    'user_name', 'user_followers_count', 'sentiment'
]
cols_to_keep = [c for c in possible_columns if c in df.columns]

df[cols_to_keep].to_json('tweets.json', orient='records', lines=True)

print(f"Converted {len(df)} COVID-19 tweets using columns {cols_to_keep} to tweets.json")
