import pandas as pd
from sqlalchemy import create_engine
import os
import zipfile

DB_URI = os.getenv('DB_URI', 'postgresql://admin:adminpassword@localhost:5432/nbo_database')

def extract_dataset(dataset_dir):
    # Extracts data.zip if transaction_data.csv is missing
    zip_path = os.path.join(dataset_dir, 'data.zip')
    test_file = os.path.join(dataset_dir, 'transaction_data.csv')
    
    if not os.path.exists(test_file):
        if os.path.exists(zip_path):
            print(f"Extracting {zip_path}...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_dir)
            print("Extraction complete.")
        else:
            print(f"Warning: Missing both CSV files and {zip_path} in {dataset_dir}.")

def load_csv_to_postgres(file_path, table_name, engine):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Loading {file_path} into {table_name}...")
    
    chunk_size = 100000
    first_chunk = True
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk.columns = [col.lower() for col in chunk.columns]
        
        # Replace table on the first chunk, append subsequent chunks
        if first_chunk:
            chunk.to_sql(table_name, engine, if_exists='replace', index=False)
            first_chunk = False
        else:
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
            
    print(f"Finished loading {table_name}.")

def main():
    engine = create_engine(DB_URI)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_dir = os.path.join(base_dir, 'dataset')
    
    extract_dataset(dataset_dir)
    
    files_to_load = {
        'hh_demographic.csv': 'households',
        'product.csv': 'products',
        'transaction_data.csv': 'transactions',
        'campaign_desc.csv': 'campaign_descriptions',
        'campaign_table.csv': 'campaigns',
        'coupon.csv': 'coupons',
        'coupon_redempt.csv': 'coupon_redemptions'
    }
    
    for file_name, table_name in files_to_load.items():
        file_path = os.path.join(dataset_dir, file_name)
        load_csv_to_postgres(file_path, table_name, engine)

if __name__ == "__main__":
    main()