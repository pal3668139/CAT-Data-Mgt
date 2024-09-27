from googleapiclient.discovery import build
import pandas as pd

def fetch_sheet_id(sheet_name, drive_service):
    """Fetch Google Sheets file ID based on metadata."""
    response = drive_service.files().list(q=f"name contains '{sheet_name}'").execute()
    files = response.get('files', [])
    sheet_id = files[0]['id'] if files else None
    return sheet_id

def extract_data(sheet_id, sheets_service):
    """Extract data from Google Sheets into a DataFrame."""
    result = sheets_service.spreadsheets().values().get(spreadsheetId=sheet_id, range='Sheet1').execute()
    data = result.get('values', [])
    df = pd.DataFrame(data[1:], columns=data[0])  # Convert to DataFrame
    return df
