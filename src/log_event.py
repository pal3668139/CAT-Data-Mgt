from google.cloud import logging as cloud_logging
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# Set up Google Cloud Logging Client
cloud_logger = cloud_logging.Client().logger("etl_pipeline_logs")

# Set up Google Drive API credentials
SCOPES = ['https://www.googleapis.com/auth/drive.file']
creds = Credentials.from_service_account_file('D:/Users/peter/PythonProjects/PandasTest/neat-simplicity-425622-v1-b1e259b0c18a.json', scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Define the Google Drive file ID for the JSON log file
LOG_FILE_ID = 'your-log-file-id'  # Replace with actual file ID on Google Drive

def log_event(log_level, component, message, additional_data=None, log_to_cloud=True):
    """Logs events to Google Cloud Logging and optionally to a JSON file on Google Drive."""
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "log_level": log_level,
        "component": component,
        "message": message,
        "additional_data": additional_data or {}
    }

    # Log to Google Cloud Logging
    if log_to_cloud:
        severity = log_level.upper()
        cloud_logger.log_struct(log_entry, severity=severity)
        print(f"Logged to Cloud Logging: {log_entry}")

    # Optional: Log to Google Drive JSON file
    try:
        request = drive_service.files().get_media(fileId=LOG_FILE_ID)
        response = request.execute()
        existing_logs = json.loads(response) if response else []
        existing_logs.append(log_entry)

        # Write back the updated logs to Google Drive
        media = MediaFileUpload('log.json', mimetype='application/json', resumable=True)
        drive_service.files().update(fileId=LOG_FILE_ID, media_body=media).execute()
        print(f"Log entry added to Google Drive: {log_entry}")

    except Exception as e:
        print(f"Failed to log to Google Drive: {e}")

def log_api_error(component, error):
    """Logs errors related to Google Cloud APIs, capturing metadata and error details."""
    error_message = {
        "error_type": type(error).__name__,
        "message": str(error),
        "component": component
    }
    # Use Google Cloud Logging to capture API errors with metadata
    cloud_logger.log_struct(error_message, severity="ERROR")
    print(f"Logged API error: {error_message}")
