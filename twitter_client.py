import os
import tweepy
from dotenv import load_dotenv

class TwitterClient:
    def __init__(self):
        """
        Initialize the Twitter client.

        Load necessary environment variables for authentication.
        """
        load_dotenv()  # Loading environment variables
        self.CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
        self.CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
        self.ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
        self.ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.client = self.load_twitter_client()

    def load_twitter_client(self):
        """
        Load the Twitter client using environment variables.

        Returns:
            tweepy.Client: The Twitter client instance.

        Description:
            This method initializes and returns the tweepy client using environment variables.
            Note: wait_on_rate_limit sleeps future requests until rate limit is lifted.
        """
        try:
            client = tweepy.Client(
                consumer_key=self.CONSUMER_KEY,
                consumer_secret=self.CONSUMER_SECRET,
                access_token=self.ACCESS_TOKEN,
                access_token_secret=self.ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            return client
        except tweepy.TweepyException as e:
            print("Tweepy Exception:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)
        return None

    def post_tweet(self, text):
        """
        Post the provided text to Twitter.

        Args:
            text (str): The text to be posted to Twitter.

        Returns:
            None

        Description:
            This method creates a tweet on Twitter using the provided text.
        """
        try:
            self.client.create_tweet(text=text)
            print(f"Tweeted: {text}")
        except tweepy.TweepyException as e:
            print("Tweepy Exception:", e)
        except Exception as e:
            print("An unexpected error occurred:", e)

# Example usage:
# twitter_client = TwitterClient()
# twitter_client.post_tweet("Hello, Twitter!")
