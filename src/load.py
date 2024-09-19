from log_event import log_event
from google.cloud import bigquery

def load_data_to_bigquery(df, table_name):
    """Load the processed data into BigQuery."""
    try:
        client = bigquery.Client()
        job_config = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )
        client.load_table_from_dataframe(df, table_name, job_config=job_config).result()
        log_event('INFO', 'load', 'Data loaded into BigQuery', {'table_name': table_name, 'rows_loaded': len(df)})
    except Exception as e:
        log_event('ERROR', 'load', f"Error loading data to BigQuery: {str(e)}")
        raise
