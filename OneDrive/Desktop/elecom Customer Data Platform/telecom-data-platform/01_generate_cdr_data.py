import pandas as pd
import random
from datetime import datetime, timedelta
import os

print("Generating Telecom CDR Data... ⏳")

# 1. Customers - 10,000 Customers
customers = []
cities = ['Hyderabad', 'Vijayawada', 'Visakhapatnam', 'Guntur', 'Warangal', 'Chennai', 'Bangalore', 'Mumbai']
plans = ['Prepaid', 'Postpaid']
for i in range(1, 10001):
    customers.append({
        'customer_id': f'CUST_{i:05d}',
        'customer_name': f'Customer_{i}',
        'city': random.choice(cities),
        'plan_type': random.choice(plans),
        'age': random.randint(18, 65),
        'join_date': (datetime.now() - timedelta(days=random.randint(30, 1000))).date()
    })
df_customers = pd.DataFrame(customers)
df_customers.to_csv('customers.csv', index=False)
print(f"Customers DONE: {len(df_customers)} rows ✅")

# 2. Towers - 500 Towers
towers = []
for i in range(1, 501):
    towers.append({
        'tower_id': f'TWR_{i:03d}',
        'location': random.choice(cities),
        'city': random.choice(cities),
        'signal_strength': random.choice(['Excellent', 'Good', 'Average', 'Poor'])
    })
df_towers = pd.DataFrame(towers)
df_towers.to_csv('towers.csv', index=False)
print(f"Towers DONE: {len(df_towers)} rows ✅")

# 3. CDR - 1 Lakh Call Records - MAIN DATA
cdr_data = []
call_types = ['Voice', 'Data', 'SMS']
for i in range(1, 100001):
    duration = random.randint(10, 3600)
    data_used = round(random.uniform(0.1, 5.0), 2) if random.random() > 0.3 else 0
    call_drop = 1 if random.random() < 0.05 else 0  # 5% Call Drops
    
    cdr_data.append({
        'call_id': f'CALL_{i:06d}',
        'customer_id': f'CUST_{random.randint(1, 10000):05d}',
        'tower_id': f'TWR_{random.randint(1, 500):03d}',
        'call_type': random.choice(call_types),
        'duration_sec': duration,
        'data_used_gb': data_used,
        'call_drop': call_drop,
        'call_date': (datetime.now() - timedelta(days=random.randint(0, 30))).date()
    })

df_cdr = pd.DataFrame(cdr_data)
df_cdr.to_csv('cdr_data.csv', index=False)
print(f"CDR DONE: {len(df_cdr)} rows ✅")
print("\nAll Files Created! 🎉")
print("customers.csv, towers.csv, cdr_data.csv")