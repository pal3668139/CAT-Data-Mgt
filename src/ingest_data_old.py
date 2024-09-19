import pandas as pd
import io
from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Define the scopes your function will need
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']

# Load service account credentials (update this to the path of your service account JSON file)
SERVICE_ACCOUNT_FILE = 'D:/Users/peter/PythonProjects/PandasTest/neat-simplicity-425622-v1-b1e259b0c18a.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Initialize Google Sheets and Google Drive API services
drive_service = build('drive', 'v3', credentials=credentials)
sheets_service = build('sheets', 'v4', credentials=credentials)

@app.route('/read-google-sheet', methods=['GET'])
def read_google_sheet():
    """HTTP route to read a Google Sheets file from Google Drive, convert it to a Pandas DataFrame, and return some results."""

    # Google Sheets file ID (update this with your file ID)
    sheet_file_id = '1wHrRNJgkitDfBjBACh5LThrdX08QqhM-OsepG_M2HJg'

    # Fetch the content of the sheet using Google Sheets API
    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_file_id, range='Sheet1').execute()
    values = result.get('values', [])

    if not values:
        return jsonify({'error': 'No data found in the Google Sheet.'}), 404
    
    # Assuming the first row contains headers
    headers = values[0]
    data = values[1:]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)

    df.info()
    df

    # Convert processed DataFrame to HTML or JSON for response
    return df.to_html()

if __name__ == '__main__':
    app.run(debug=True)
