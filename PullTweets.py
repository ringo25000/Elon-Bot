from dotenv import load_dotenv
import os
import tweepy
import time


load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_key = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Function to extract tweets
def get_tweets(username):
    if not bearer_token:
        raise ValueError("Bearer token is not set. Please check your environment variables.")
    
    client = tweepy.Client(bearer_token=bearer_token)
    query = f'from:{username} -is:reply'
    
    retries = 3
    for i in range(retries):
        try:
            tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=10)
            for tweet in tweets.data:
                print(tweet.text)
            break
        except tweepy.errors.TooManyRequests as e:
            print(f"Rate limit exceeded. Retrying in {2 ** i} seconds...")
            time.sleep(2 ** i)
        except tweepy.errors.Unauthorized as e:
            print("Unauthorized error: Please check your credentials and access level.")
            print(e)
            break

get_tweets("elonmusk")