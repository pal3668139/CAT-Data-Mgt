from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from ingest_data import fetch_sheet_id, extract_data
from transform import clean_data, normalize_data, calculate_metrics
from load import load_data_to_bigquery
from log_event import log_event, log_api_error
from datetime import datetime

# Set up Google Cloud credentials and services
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets.readonly']
creds = Credentials.from_service_account_file('D:/Users/peter/PythonProjects/PandasTest/neat-simplicity-425622-v1-b1e259b0c18a.json', scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)

def main(sheet_name):
    try:
        # Step 1: Extract data
        log_event('INFO', 'main', 'Starting data extraction', {'sheet_name': sheet_name})
        sheet_id = fetch_sheet_id(sheet_name, drive_service)
        df = extract_data(sheet_id, sheets_service)
        log_event('INFO', 'ingest_data', 'Data fetched successfully', {'sheet_name': sheet_name, 'rows': len(df)})

        # Step 2: Transform data
        log_event('INFO', 'main', 'Starting data transformation', {'sheet_name': sheet_name})
        df = clean_data(df)
        df = normalize_data(df)
        df = calculate_metrics(df)
        log_event('INFO', 'transform', 'Data transformed successfully', {'row_count': len(df)})

        # Step 3: Load data
        log_event('INFO', 'main', 'Starting data load to BigQuery', {'sheet_name': sheet_name})
        load_data_to_bigquery(df, table_name=f'processed_{sheet_name}')
        log_event('INFO', 'load', 'Data loaded into BigQuery', {'table_name': f'processed_{sheet_name}', 'rows_loaded': len(df)})

    except Exception as e:
        log_api_error('main', e)
        log_event('ERROR', 'main', f'Error occurred during ETL process: {str(e)}')
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Example execution with sheet name as a parameter
    main(sheet_name='week05')
