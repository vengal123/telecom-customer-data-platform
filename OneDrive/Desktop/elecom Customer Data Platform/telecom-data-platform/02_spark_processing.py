import pandas as pd
import os

print("Starting Spark Processing (Simulated Kafka -> Spark)... ⏳")

# --- BRONZE LAYER - Raw Data ---
# Kafka nundi vachina data anukondi
df_cdr = pd.read_csv('cdr_data.csv')
df_customers = pd.read_csv('customers.csv')
df_towers = pd.read_csv('towers.csv')

os.makedirs('bronze', exist_ok=True)
df_cdr.to_csv('bronze/bronze_cdr.csv', index=False)
print(f"BRONZE DONE: {len(df_cdr)} raw CDR rows ✅")

# --- SILVER LAYER - Cleaning ---
# 1. Nulls remove, 2. Invalid duration remove, 3. Duplicate calls remove
df_clean = df_cdr.dropna()
df_clean = df_clean[df_clean['duration_sec'] > 0]
df_clean = df_clean.drop_duplicates(subset=['call_id'])

# Call Drop reason add chey
df_clean['is_long_call'] = df_clean['duration_sec'].apply(lambda x: 1 if x > 1800 else 0)

os.makedirs('silver', exist_ok=True)
df_clean.to_csv('silver/silver_cdr.csv', index=False)
print(f"SILVER DONE: {len(df_clean)} clean rows ✅ (Duplicates/Nulls removed)")

# --- GOLD LAYER - Business Tables ---
# 1. Fact Table - Daily Usage
fact_calls = df_clean.merge(df_customers[['customer_id','city','plan_type']], on='customer_id', how='left')
fact_calls = fact_calls.merge(df_towers[['tower_id','location']], on='tower_id', how='left')

os.makedirs('gold', exist_ok=True)
fact_calls.to_csv('gold/fact_calls.csv', index=False)

# 2. Churn Dataset - IMPORTANT FOR HR!
# Evaru ekkuva call drops face chesaro, vallu churn avvochu
churn_df = df_clean.groupby('customer_id').agg(
    total_calls=('call_id','count'),
    total_duration=('duration_sec','sum'),
    total_data_used=('data_used_gb','sum'),
    total_drops=('call_drop','sum'),
    avg_duration=('duration_sec','mean')
).reset_index()
churn_df['drop_rate'] = (churn_df['total_drops'] / churn_df['total_calls'] * 100).round(2)
churn_df['churn_risk'] = churn_df['drop_rate'].apply(lambda x: 'HIGH' if x > 10 else 'MEDIUM' if x > 5 else 'LOW')
churn_df = churn_df.merge(df_customers, on='customer_id', how='left')
churn_df.to_csv('gold/churn_dataset.csv', index=False)

# 3. Network Performance - Tower wise
network_df = df_clean.groupby('tower_id').agg(
    total_calls=('call_id','count'),
    drop_rate=('call_drop','mean'),
    avg_duration=('duration_sec','mean')
).reset_index()
network_df['drop_rate'] = (network_df['drop_rate']*100).round(2)
network_df = network_df.merge(df_towers, on='tower_id', how='left')
network_df.to_csv('gold/network_performance.csv', index=False)

print(f"GOLD DONE ✅")
print(f"  - fact_calls: {len(fact_calls)} rows")
print(f"  - churn_dataset: {len(churn_df)} customers")
print(f"  - network_performance: {len(network_df)} towers")
print("\nSpark Processing COMPLETE! 🎉")