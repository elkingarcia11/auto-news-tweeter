import os
import pandas as pd
from google.cloud import storage
from dotenv import load_dotenv

class TweetCSVManager:
    def __init__(self, file_path: str="tweet_history.csv", key_path: str="service_account_credentials.json", column_name: str = "tweet"):
        load_dotenv()
        self.file_path = file_path
        self.bucket_name = os.getenv("GOOGLE_CLOUD_BUCKET_NAME")
        self.column_name = column_name
        self.df = None
        self.storage_client = self._initialize_storage_client(key_path)

    def _initialize_storage_client(self, key_path: str):
        """
        Initializes and returns the Google Cloud Storage client.
        """
        try:
            if not self.bucket_name:
                raise ValueError("Environment variable 'GOOGLE_CLOUD_BUCKET_NAME' is not set.")
            return storage.Client.from_service_account_json(key_path)
        except Exception as e:
            print(f"Error initializing Google Cloud Storage client: {e}")
            return None

    def fetch_csv(self):
        """
        Fetches the CSV file from Google Cloud Storage and saves it locally.
        """
        if not self.storage_client:
            print("Google Cloud Storage client is not initialized.")
            return

        try:
            print("Fetching CSV from Google Cloud Storage...")
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_path)
            blob.download_to_filename(self.file_path)
            print(f"File downloaded from bucket '{self.bucket_name}' to '{self.file_path}'")
        except Exception as e:
            print(f"Error fetching CSV from Google Cloud Storage: {e}")

    def upload_csv(self):
        """
        Uploads the local CSV file to Google Cloud Storage.
        """
        if not self.storage_client:
            print("Google Cloud Storage client is not initialized.")
            return

        try:
            print("Uploading CSV to Google Cloud Storage...")
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_path)
            blob.upload_from_filename(self.file_path)
            print("File uploaded successfully.")
        except Exception as e:
            print(f"Error uploading CSV to Google Cloud Storage: {e}")

    def load_csv(self) -> pd.DataFrame:
        """
        Loads the local CSV file into a DataFrame object.
        """
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"The file '{self.file_path}' does not exist.")
            
            self.df = pd.read_csv(self.file_path)

            if self.column_name not in self.df.columns:
                raise ValueError(f"'{self.column_name}' column not found in the CSV file.")
            
            print("CSV file loaded successfully.")
            return self.df
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        except ValueError as val_error:
            print(val_error)
        except Exception as e:
            print(f"An error occurred while loading the CSV: {e}")
            return pd.DataFrame()

    def add_new_item_to_csv(self, item: str):
        """
        Adds a new tweet to the CSV file, saves it locally, and uploads it to Google Cloud Storage.
        """
        try:
            if self.df is None or self.df.empty:
                self.fetch_csv()
                self.load_csv()

            if self.column_name not in self.df.columns:
                raise ValueError("DataFrame is not loaded or column is missing.")

            new_item = pd.DataFrame([{self.column_name: item}])
            self.df = pd.concat([self.df, new_item], ignore_index=True)
            self.df.to_csv(self.file_path, index=False)
            print("New item added to CSV and file saved successfully.")
            self.upload_csv()
        except ValueError as val_error:
            print(val_error)
        except Exception as e:
            print(f"An error occurred while adding a new item to the CSV: {e}")

    def does_exist_in_latest_items(self, item: str, x: int = 10) -> bool:
        """
        Checks if the specified item exists within the last x entries in the CSV file.
        """
        try:
            if self.df is None or self.df.empty:
                self.fetch_csv()
                self.load_csv()

            if self.column_name not in self.df.columns:
                raise ValueError(f"'{self.column_name}' column not found in the loaded DataFrame.")

            last_x_items = set(self.df[self.column_name].tail(x).astype(str))
            return item in last_x_items
        except Exception as e:
            print(f"An error occurred while checking for the item: {e}")
            return False
