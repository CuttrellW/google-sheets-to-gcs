# google-sheets-to-gcs
A simple python program to upload Google Sheets directly to Google Cloud Storage (GCS), checking for updates and converting data into CSV or JSON format.

## Features
- Automatically checks if a Google Sheet has been updated since the last file upload to GCS.
- Processes the sheet's data into a `csv` or `json` file format.
- Uploads the processed file to a specified GCS bucket.

## Requirements

To install the required dependencies, run:
```bash
pip install -r requirements.txt
```
## Required Libraries

- Flask: for creating the web application
- gspread: for accessing Google Sheets
- pandas: for manipulating and saving data
- google-cloud-storage: for uploading files to Google Cloud Storage
- google-auth: for handling Google service account authentication

## Environment Variables

The application requires a Google Cloud service account key to authenticate API calls. Set the following environment variable:

`GCP_SERVICE_ACCOUNT_KEY`: Path to your Google Cloud service account key file (JSON).

As an alternative, you can also use `Credentials.from_service_account_file()` to load the service account key details directly

## Endpoints

### `POST /process_sheet`
Processes a Google Sheet and uploads the data to GCS.

#### Request Body:
```json
{
  "sheet_id": "your-google-sheet-id",
  "bucket_name": "your-gcs-bucket-name",
  "file_name": "output-file.csv or output-file.json"
}
```
## How It Works
1. **Authentication**: The app uses Google service account credentials to access both Google Sheets and GCS.
2. **Checking for Updates**: It compares the last modified time of the Google Sheet with the last modified time of the file in GCS.
3. **Data Processing**: If the sheet has been updated, the app fetches the data, converts it into a `pandas` DataFrame, and saves it locally as either a `.csv` or `.json` file.
4. **Uploading to GCS**: The file is then uploaded to the specified GCS bucket.

## Running the Application

To run the app locally, execute:

```bash
python app.py
```
