import pandas as pd
from sqlalchemy import create_engine
from mlxtend.frequent_patterns import fpgrowth, association_rules
import joblib

DB_URI = 'postgresql://admin:adminpassword@localhost:5432/nbo_database'

def fetch_basket_data(engine):
    # Fetch transaction subset joined with products to get categories
    query = """
    SELECT t.basket_id, p.sub_commodity_desc
    FROM transactions t
    JOIN products p ON t.product_id = p.product_id
    LIMIT 500000 
    """
    return pd.read_sql(query, engine)

def prepare_market_basket(df):
    # Filter out obvious staple items to find deeper purchasing patterns
    staple_items = ['FLUID MILK PRODUCTS', 'BAKED BREAD/BUNS/ROLLS', 'BANANAS', 'EGGS']
    df_filtered = df[~df['sub_commodity_desc'].isin(staple_items)]
    
    basket = (df_filtered.groupby(['basket_id', 'sub_commodity_desc'])['sub_commodity_desc']
              .count().unstack().reset_index().fillna(0)
              .set_index('basket_id'))
    
    basket_sets = (basket > 0).astype(int)
    return basket_sets

def train_association_rules(basket_sets):
    # Lowered support threshold to 0.2% to capture niche associations
    frequent_itemsets = fpgrowth(basket_sets, min_support=0.002, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.5)
    
    rules = rules.sort_values(by=['lift'], ascending=False)
    return rules

def main():
    engine = create_engine(DB_URI)
    
    print("Fetching transaction data...")
    df = fetch_basket_data(engine)
    
    print("Preparing basket matrix...")
    basket_sets = prepare_market_basket(df)
    
    print("Training FP-growth model and generating rules...")
    rules = train_association_rules(basket_sets)
    
    print("Top 5 product associations:")
    print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())
    
    print("Saving NBO rules artifact...")
    joblib.dump(rules, 'nbo_rules.joblib')
    print("Process completed.")

if __name__ == "__main__":
    main()