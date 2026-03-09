from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sqlalchemy import create_engine
import os

app = FastAPI(title="NBO Engine ML API", version="1.0.0")

DB_URI = os.getenv('DB_URI', 'postgresql://admin:adminpassword@localhost:5432/nbo_database')
engine = create_engine(DB_URI)

# Load ML artifacts globally on startup
kmeans_model = joblib.load('kmeans_model.joblib')
scaler = joblib.load('scaler.joblib')
nbo_rules = joblib.load('nbo_rules.joblib')

class NBORequest(BaseModel):
    basket_items: list[str]

@app.get("/api/segmentation/{household_key}")
def get_customer_segment(household_key: int):
    # Fetch customer RFM metrics and predict segment
    query = f"""
    WITH max_day_cte AS (SELECT MAX(day) AS current_day FROM transactions)
    SELECT 
        (m.current_day - MAX(t.day)) AS recency,
        COUNT(DISTINCT t.basket_id) AS frequency,
        SUM(t.sales_value) AS monetary
    FROM transactions t
    CROSS JOIN max_day_cte m
    WHERE t.household_key = {household_key}
    GROUP BY m.current_day
    """
    df = pd.read_sql(query, engine)
    
    if df.empty or df['monetary'].isnull().all():
        raise HTTPException(status_code=404, detail="Customer not found or no transactions")
        
    features = df[['recency', 'frequency', 'monetary']]
    scaled_features = scaler.transform(features)
    cluster = kmeans_model.predict(scaled_features)[0]
    
    return {
        "household_key": household_key,
        "segment": int(cluster),
        "metrics": features.iloc[0].to_dict()
    }

@app.post("/api/nbo")
def get_next_best_offer(request: NBORequest):
    items = set(request.basket_items)
    matching_rules = nbo_rules[nbo_rules['antecedents'].apply(lambda x: x.issubset(items))]
    
    # Fallback strategy when no specific association rules are met
    if matching_rules.empty:
        fallback_recommendations = ["PREMIUM COFFEE", "GREEK YOGURT", "FRESH BERRIES"]
        return {"recommendations": fallback_recommendations}
        
    top_rules = matching_rules.sort_values('lift', ascending=False).head(3)
    recommendations = []
    
    for _, row in top_rules.iterrows():
        consequents = list(row['consequents'])
        recommendations.extend(consequents)
        
    unique_recommendations = list(dict.fromkeys(recommendations))
    
    return {"recommendations": unique_recommendations[:3]}