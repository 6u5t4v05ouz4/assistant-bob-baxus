import pandas as pd
import io
import requests
import logging

logger = logging.getLogger(__name__)

def load_whisky_data():
    """
    Load whisky data from the Google Sheets URL
    
    Returns:
        DataFrame: Pandas DataFrame containing whisky data
    """
    try:
        # Google Sheets URL
        sheet_url = "https://docs.google.com/spreadsheets/d/1yXIJo5f00clyrFHlRyKuIwrNCQw_cNcoVbSvtKO_bTs/export?format=csv"
        
        # Download the CSV data
        response = requests.get(sheet_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Read the CSV data into a DataFrame
        data = pd.read_csv(io.StringIO(response.text))
        
        # Clean and preprocess the data
        data = preprocess_whisky_data(data)
        
        logger.info(f"Successfully loaded whisky data with {len(data)} bottles")
        return data
        
    except Exception as e:
        logger.error(f"Error loading whisky data: {e}")
        raise

def preprocess_whisky_data(data):
    """
    Clean and preprocess the whisky data
    
    Args:
        data (DataFrame): Raw whisky data
    
    Returns:
        DataFrame: Cleaned and preprocessed whisky data
    """
    # Convert column names to lowercase and remove spaces
    data.columns = [col.lower().replace(' ', '_') for col in data.columns]
    
    # Ensure essential columns exist
    essential_columns = ['id', 'name', 'brand', 'spirit', 'price', 'proof']
    missing_columns = [col for col in essential_columns if col not in data.columns]
    
    if missing_columns:
        logger.warning(f"Missing essential columns: {missing_columns}")
        # Add missing columns with default values
        for col in missing_columns:
            data[col] = None
    
    # Convert numeric columns
    if 'price' in data.columns:
        data['price'] = pd.to_numeric(data['price'], errors='coerce')
    
    if 'proof' in data.columns:
        data['proof'] = pd.to_numeric(data['proof'], errors='coerce')
    
    if 'age' in data.columns:
        data['age'] = pd.to_numeric(data['age'], errors='coerce')
    
    # Fill missing values
    data['price'].fillna(0, inplace=True)
    data['proof'].fillna(0, inplace=True)
    data['age'].fillna(0, inplace=True)
    
    # Generate unique IDs if missing
    if 'id' not in data.columns or data['id'].isna().any():
        logger.warning("Some or all ID values are missing, generating unique IDs")
        missing_id_mask = data['id'].isna() if 'id' in data.columns else pd.Series([True] * len(data))
        data.loc[missing_id_mask, 'id'] = [f"gen_{i}" for i in range(sum(missing_id_mask))]
    
    return data
