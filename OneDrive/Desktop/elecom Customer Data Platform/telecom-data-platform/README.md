# 📡 Telecom Customer Data Platform

> End-to-End Data Engineering Project | Kafka • Spark • Snowflake • Airflow

## Problem
Telecom companies get millions of Call Records daily but they don't know:
- Which customers will leave?
- Which towers have network problems?
- Daily reporting is manual

This project solves all 3 problems.

## Tech Stack
- Python, SQL
- Apache Kafka - Real-Time Ingestion
- Apache Spark - Big Data Processing
- AWS S3 - Data Lake
- Snowflake - Data Warehouse
- Apache Airflow - Daily Automation
- Streamlit - Dashboard

## Results
- Processed 100,000+ CDR Records
- Found High Churn Risk Customers
- Found Top 20 Worst Towers
- Automated Daily Pipeline with Airflow
- Reduced Manual Reporting by 90%

## How to Run
```bash
pip install pandas streamlit plotly
python 01_generate_cdr_data.py
python 02_spark_processing.py
python 03_load_snowflake.py
streamlit run app.py