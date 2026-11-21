import tweepy 

#api key tokens
bearer_token = "AAAAAAAAAAAAAAAAAAAAALqnAQIAAAAA2cn5Adjv9O5JxgCUG7EqI59wexk%3DedwivkdBBoFlWax5TJhfzORj82DUHzKgsyULC5NOSwwYNSGCLL"
consumer_key = "6VOMjLtlgrATfUds1rhwAf3bi"
consumer_key_secret = "LBQYJj8ajSz0HT5V4TDhAkWKtGae8NdO1tzEEYTCQ8rQEtRFI5"
access_token = "1595392163978018816-CShMuu3gTPomol50x6lYpuVwIdxCwZ"
access_token_secret = "ImTDOuJzmicnbD57cx9TbWymu7XIW44T1AekSRiMKA1Kw"

#connect to x api
client = tweepy.client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

try:
    me = client.get_me()
    print("Connection successful!",me.data.username)
except Exception as e:
    print("Connection failed:", e)

try:
    tweets = client.search_recent_tweets(query="#python -is:retweet",max_results=10)
    print("Fetched tweets successfully!")
    for tweet in tweets.data:
        print("-", tweet.text[:60], "...")
except Exception as e:
    print("Search error(Expected on Free Tier):",e)

