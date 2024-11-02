# Project: Automated News Fetching and Tweeting System

This project automates the process of fetching top headlines, filtering recent headlines to avoid duplicates, and posting new ones to Twitter. News articles are retrieved from NewsAPI, managed locally and in Google Cloud Storage, and posted using the Twitter API.

## Project Structure

- **news_manager.py**: Manages fetching and processing of news headlines.
- **tweet_csv_manager.py**: Manages loading, saving, and checking tweet history in a CSV file stored in Google Cloud Storage.
- **twitter_client.py**: Handles authentication and tweet posting to Twitter.

## Setup Guide

### Step 1: Install Dependencies

1. Install the dependencies by running:

    ```bash
    pip install -r requirements.txt
    ```

### Step 2: Set Up NewsAPI

1. Sign up on [NewsAPI](https://newsapi.org/) and get your API key.
2. Add the API key to a `.env` file to keep it secure:

    ```plaintext
    NEWS_API_KEY=your_api_key
    ```

### Step 3: Google Cloud Project Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a New Project**.
3. **Switch to your new project** in the Cloud Console.
4. **Enable Billing** for the project.

### Step 4: Create a Google Cloud Storage Bucket

1. Navigate to **Cloud Storage** in the Google Cloud Console.
2. **Create a New Bucket** and name it appropriately.
3. In your `.env` file, add the bucket name:

    ```plaintext
    GOOGLE_CLOUD_BUCKET_NAME=your-bucket-name
    ```

4. Upload your starter data file, `tweet_history.csv`, to this bucket.

### Step 5: Set Up a Google Cloud Service Account

1. In the Google Cloud Console, go to **IAM & Admin > Service Accounts**.
2. **Create a Service Account** for your Python application to access the bucket.
3. **Grant Storage Admin Permissions** to this service account for your bucket.
4. Create and download the **service account key** JSON file.
5. Place this file in your project directory and rename it:

    ```plaintext
    service_account_credentials.json
    ```

---

Your project is now configured to securely use NewsAPI and Google Cloud Storage.

### Step 6: Set Up Twitter API

1. Create a Twitter Developer Account and get API keys and access tokens for your app.
2. Add the following keys to your `.env` file:

    ```plaintext
    TWITTER_CONSUMER_KEY=your_twitter_consumer_key
    TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
    TWITTER_ACCESS_TOKEN=your_twitter_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
    ```

Your project is now configured to securely use NewsAPI, Twitter API, and Google Cloud Storage.

**Note**: Keep the `.env` file and `service_account_credentials.json` out of version control by adding them to `.gitignore`:

```plaintext
.env
service_account_credentials.json
```

## Running the Application

The main entry point is the `NewsManager` class in `news_manager.py`, which handles fetching, processing, and tweeting news headlines.

1. Run the following script:

    ```python
    # Example usage
    from news_manager import NewsManager

    news_manager = NewsManager(language='en')
    news_manager.fetch_process_and_tweet_news()
    ```