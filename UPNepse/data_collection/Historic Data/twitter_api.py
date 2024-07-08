import tweepy
import pandas as pd
import os 
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv("TWITTER_API_KEY")
consumer_secret = os.getenv("TWITTER_API_SECRET_KEY")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(
    consumer_key,consumer_secret,access_token,access_token_secret

)

api = tweepy.API(auth,wait_on_rate_limit=True)
print(api)
