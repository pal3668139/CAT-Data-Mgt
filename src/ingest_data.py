from googleapiclient.discovery import build
from log_event import log_event
import pandas as pd

def fetch_sheet_id(sheet_name, drive_service):
    """Fetch Google Sheets file ID based on metadata."""
    try:
        response = drive_service.files().list(q=f"name contains '{sheet_name}'").execute()
        files = response.get('files', [])
        sheet_id = files[0]['id'] if files else None
        log_event('INFO', 'ingest_data', 'Fetched sheet ID', {'sheet_name': sheet_name, 'sheet_id': sheet_id})
        return sheet_id
    except Exception as e:
        log_event('ERROR', 'ingest_data', f"Error fetching sheet ID: {str(e)}")
        raise

def extract_data(sheet_id, sheets_service):
    """Extract data from Google Sheets into a DataFrame."""
    try:
        result = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range='Sheet1').execute()
        data = result.get('values', [])
        df = pd.DataFrame(data[1:], columns=data[0])  # Convert to DataFrame
        log_event('INFO', 'ingest_data', 'Data extracted successfully', {'rows': len(df)})
        return df
    except Exception as e:
        log_event('ERROR', 'ingest_data', f"Error extracting data: {str(e)}")
        raise
