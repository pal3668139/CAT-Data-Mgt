from log_event import log_event
import pandas as pd

def clean_data(df):
    """Clean data by removing nulls and duplicates."""
    try:
        initial_row_count = len(df)
        df.dropna(inplace=True)
        final_row_count = len(df)
        log_event('INFO', 'transform', 'Cleaned data', {'initial_rows': initial_row_count, 'final_rows': final_row_count})
        return df
    except Exception as e:
        log_event('ERROR', 'transform', f"Error cleaning data: {str(e)}")
        raise

def normalize_data(df):
    """Normalize data formats such as dates and numeric conversions."""
    try:
        df['Date'] = pd.to_datetime(df['Date'])
        log_event('INFO', 'transform', 'Normalized data')
        return df
    except Exception as e:
        log_event('ERROR', 'transform', f"Error normalizing data: {str(e)}")
        raise

def calculate_metrics(df):
    """Add calculated columns or metrics."""
    try:
        df['Total'] = df['Value'].astype(float) * df['Quantity'].astype(int)
        log_event('INFO', 'transform', 'Calculated metrics', {'new_columns': ['Total']})
        return df
    except Exception as e:
        log_event('ERROR', 'transform', f"Error calculating metrics: {str(e)}")
        raise
