import pandas as pd

def clean_data(df):
    """Clean data by removing nulls and duplicates."""
    df.dropna(inplace=True)
    return df

def normalize_data(df):
    """Normalize data formats such as dates and numeric conversions."""
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def calculate_metrics(df):
    """Add calculated columns or metrics."""
    df['Total'] = df['Value'].astype(float) * df['Quantity'].astype(int)
    return df
