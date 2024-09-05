import logging
import flask
import os
import gspread
import pandas as pd

from google.cloud import storage
from google.oauth2.service_account import Credentials
from datetime import datetime as dt

app = flask.Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_credentials():
    # Get credentials from service account key
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/devstorage.read_write']
    return Credentials.from_service_account_file(os.environ["GCP_SERVICE_ACCOUNT_KEY"], scopes=scopes)


class GoogleSheetsImport:
    def __init__(self, sheet_id: str, bucket_name: str, file_name: str):
        # Get Google credentials for bucket and sheet client
        credentials = get_credentials()
        storage_client = storage.Client(credentials=credentials)

        self.bucket_client = storage_client.bucket(bucket_name)
        self.sheet_client = gspread.authorize(credentials)
        self.file_name = file_name
        self.sheet_id = sheet_id

    def sheet_updated(self, spreadsheet: gspread.Spreadsheet) -> bool:
        # Get Sheet last modified time
        sheet_last_updated = dt.strptime(spreadsheet.lastUpdateTime, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Get GCS file last modified time
        blob = self.bucket_client.blob(self.file_name)
        if not blob.exists():
            return True  # If file does not exist, return True to upload

        # Reload blob to get the updated timestamp
        blob.reload()
        blob_last_updated = blob.updated

        # Check Sheet was modified after file was last updated
        logging.info(f"Sheet modified: {sheet_last_updated} Blob modified: {blob_last_updated}")
        return sheet_last_updated > blob_last_updated if blob_last_updated else True

    def process_sheet(self):
        # Open Google Sheet
        logging.info(f"Processing {self.file_name}...")
        spreadsheet = self.sheet_client.open_by_key(self.sheet_id)
        if not self.sheet_updated(spreadsheet):
            logging.info(f"No updates found for {self.file_name}\n")
            return

        # Create DataFrame from Google Sheet
        df = pd.DataFrame(spreadsheet.sheet1.get_all_records())

        # Save df as file to temporary location
        temp_path = f"/tmp/{self.file_name}"
        if self.file_name.endswith('.csv'):
            df.to_csv(temp_path, index=False, header=True)
        elif self.file_name.endswith('.json'):
            df.to_json(temp_path, index=False)
        else:
            logging.error(f"Unsupported file format: {self.file_name}")
            return

        # Upload local file to GCS
        self.bucket_client.blob(self.file_name).upload_from_filename(temp_path)
        logging.info(f"Uploaded to GCS")


@app.route('/process_sheet', methods=['POST'])
def process_sheet():
    data = flask.request.json
    processor = GoogleSheetsImport(**data)
    processor.process_sheet()
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)