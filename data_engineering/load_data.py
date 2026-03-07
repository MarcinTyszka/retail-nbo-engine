import pandas as pd
from sqlalchemy import create_engine
import os

DB_URI = 'postgresql://admin:adminpassword@localhost:5432/nbo_database'

def load_csv_to_postgres(file_path, table_name, engine):
    # Validates file existence and loads data into PostgreSQL in chunks
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Loading {file_path} into {table_name}...")
    
    chunk_size = 100000
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        chunk.columns = [col.lower() for col in chunk.columns]
        chunk.to_sql(table_name, engine, if_exists='append', index=False)
        
    print(f"Finished loading {table_name}.")

def main():
    # Establishes DB connection and processes the required dataset files
    engine = create_engine(DB_URI)
    dataset_dir = 'dataset'
    
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