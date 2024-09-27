from google.cloud import bigquery

def load_data_to_bigquery(df, table_name):
    """Load the processed data into BigQuery."""
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )
    client.load_table_from_dataframe(df, table_name, job_config=job_config).result()
