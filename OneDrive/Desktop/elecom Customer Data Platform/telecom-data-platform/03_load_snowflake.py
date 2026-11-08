import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print("Loading Gold Data to Warehouse... ⏳")

# NEE PASSWORD IKKADA - 2 chotla undi, rendu marchu
MY_PASSWORD = "1234"

# Step 1: telecom_db create chey (ledante)
conn0 = psycopg2.connect(host="localhost", database="postgres", user="postgres", password=MY_PASSWORD)
conn0.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur0 = conn0.cursor()
cur0.execute("SELECT 1 FROM pg_database WHERE datname='telecom_db'")
if not cur0.fetchone():
    cur0.execute("CREATE DATABASE telecom_db")
    print("Database telecom_db Created ✅")
else:
    print("Database telecom_db already exists ✅")
cur0.close()
conn0.close()

# Step 2: telecom_db ki connect avvu
conn = psycopg2.connect(host="localhost", database="telecom_db", user="postgres", password=MY_PASSWORD)
cur = conn.cursor()

# 1. Dim Customer
df_cust = pd.read_csv('customers.csv')
cur.execute("DROP TABLE IF EXISTS dim_customer")
cur.execute("CREATE TABLE dim_customer (customer_id VARCHAR(20) PRIMARY KEY, customer_name VARCHAR(100), city VARCHAR(50), plan_type VARCHAR(20))")
for _, r in df_cust.iterrows():
    cur.execute("INSERT INTO dim_customer VALUES (%s,%s,%s,%s)", tuple(r[['customer_id','customer_name','city','plan_type']]))
print(f"Dim Customer DONE: {len(df_cust)} rows ✅")

# 2. Fact Calls - 20k rows demo kosam
df_fact = pd.read_csv('gold/fact_calls.csv')
cur.execute("DROP TABLE IF EXISTS fact_calls")
cur.execute("CREATE TABLE fact_calls (call_id VARCHAR(20) PRIMARY KEY, customer_id VARCHAR(20), tower_id VARCHAR(20), duration_sec INT, data_used_gb FLOAT, call_drop INT, call_date DATE)")
for _, r in df_fact.head(20000).iterrows():
    cur.execute("INSERT INTO fact_calls VALUES (%s,%s,%s,%s,%s,%s,%s)", (r['call_id'], r['customer_id'], r['tower_id'], int(r['duration_sec']), float(r['data_used_gb']), int(r['call_drop']), str(r['call_date'])))
print(f"Fact Calls DONE: 20000 rows ✅")

# 3. Churn Dataset
df_churn = pd.read_csv('gold/churn_dataset.csv')
cur.execute("DROP TABLE IF EXISTS churn_dataset")
cur.execute("CREATE TABLE churn_dataset (customer_id VARCHAR(20), total_calls INT, total_drops INT, drop_rate FLOAT, churn_risk VARCHAR(20))")
for _, r in df_churn.iterrows():
    cur.execute("INSERT INTO churn_dataset VALUES (%s,%s,%s,%s,%s)", (r['customer_id'], int(r['total_calls']), int(r['total_drops']), float(r['drop_rate']), r['churn_risk']))
print(f"Churn Dataset DONE: {len(df_churn)} rows ✅")

# 4. Network Performance
df_net = pd.read_csv('gold/network_performance.csv')
cur.execute("DROP TABLE IF EXISTS network_performance")
cur.execute("CREATE TABLE network_performance (tower_id VARCHAR(20), total_calls INT, drop_rate FLOAT, location VARCHAR(50))")
for _, r in df_net.iterrows():
    cur.execute("INSERT INTO network_performance VALUES (%s,%s,%s,%s)", (r['tower_id'], int(r['total_calls']), float(r['drop_rate']), str(r['location'])))
print(f"Network Performance DONE: {len(df_net)} rows ✅")

conn.commit()
conn.close()
print("\nSnowflake/Warehouse Load DONE! 🎉")
print("All 4 Tables Loaded Successfully!")