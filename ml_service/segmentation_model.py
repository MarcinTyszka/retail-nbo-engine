import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import joblib

DB_URI = 'postgresql://admin:adminpassword@localhost:5432/nbo_database'

def fetch_rfm_data(engine):
    # Fetch aggregated RFM metrics directly from PostgreSQL
    query = """
    WITH max_day_cte AS (
        SELECT MAX(day) AS current_day FROM transactions
    )
    SELECT 
        t.household_key,
        (m.current_day - MAX(t.day)) AS recency,
        COUNT(DISTINCT t.basket_id) AS frequency,
        SUM(t.sales_value) AS monetary
    FROM transactions t
    CROSS JOIN max_day_cte m
    GROUP BY t.household_key, m.current_day
    """
    return pd.read_sql(query, engine)

def preprocess_data(df):
    # Standardize features because K-Means is sensitive to variance in data scales
    scaler = StandardScaler()
    rfm_features = df[['recency', 'frequency', 'monetary']]
    scaled_features = scaler.fit_transform(rfm_features)
    return scaled_features, scaler

def train_kmeans(scaled_features, n_clusters=4):
    # Train the K-Means clustering model
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(scaled_features)
    return kmeans

def main():
    engine = create_engine(DB_URI)
    
    print("Fetching data from the database...")
    rfm_df = fetch_rfm_data(engine)
    
    print("Preprocessing data...")
    scaled_features, scaler = preprocess_data(rfm_df)
    
    print("Training K-Means model...")
    kmeans_model = train_kmeans(scaled_features)
    
    rfm_df['cluster'] = kmeans_model.labels_
    print("Sample of clustered customers:")
    print(rfm_df.head())
    
    print("Saving model artifacts for FastAPI deployment...")
    joblib.dump(kmeans_model, 'kmeans_model.joblib')
    joblib.dump(scaler, 'scaler.joblib')
    print("Process completed successfully.")

if __name__ == "__main__":
    main()