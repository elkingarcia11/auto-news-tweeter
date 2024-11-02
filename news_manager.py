import os
import logging
import requests
from dotenv import load_dotenv
from twitter_client import TwitterClient
from tweet_csv_manager import TweetCSVManager

class NewsManager:
    def __init__(self, language='en'):
        load_dotenv()
        self.language = language
        self.api_key = os.getenv("NEWS_API_KEY")
        logging.basicConfig(level=logging.INFO)

    def fetch_news(self) -> requests.Response | None:
        # Fetch news using the News API
        try:
            url = f'https://newsapi.org/v2/top-headlines?language={self.language}&apiKey={self.api_key}'
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            logging.info(f"Fetched news successfully from {url}")
            return response
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err} (Status code: {http_err.response.status_code})")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred while fetching news: {req_err}")
            return None

    def process_news(self, news: requests.Response | None) -> list[str]:
        # Process news response to trim source from headlines
        if not news:
            logging.warning("No news to process.")
            return []
        
        try:
            news_data = news.json()
            headlines = [
                article['title'].rsplit(" - ", 1)[0]
                for article in news_data.get('articles', [])
            ]
            logging.info("Processed news successfully.")
            return headlines
        except ValueError as json_err:
            logging.error(f"Error decoding JSON: {json_err}")
            return []
        except KeyError as key_err:
            logging.error(f"Missing expected key in news data: {key_err}")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred while processing news: {e}")
            return []
        
    def fetch_process_and_tweet_news(self):
        # Fetch, process, and tweet headlines
        news = self.fetch_news()
        headlines = self.process_news(news)
        tweet_csv_manager = TweetCSVManager()
        tweet_csv_manager.fetch_csv()
        tweet_csv_manager.load_csv()
        for headline in headlines:
            # Check if the headline already exists in the last 10 items
            if not tweet_csv_manager.does_exist_in_latest_items(headline):
                self.tweet_headline(headline)
                tweet_csv_manager.add_new_item_to_csv(headline)
                tweet_csv_manager.upload_csv()
                logging.info(f"Tweeted: {headline}")
                break  # Exit after tweeting the first new headline

    def tweet_headline(self, headline):
        # Post the tweet if it’s new
        try:
            self.twitter_manager = TwitterClient()
            self.twitter_manager.post_tweet(headline)
            logging.info(f"Tweeted: {headline}")
        except Exception as e:
            logging.error(f"Error tweeting headline: {e}")

# Example usage:
news_manager = NewsManager(language='en')
news_manager.fetch_process_and_tweet_news()
