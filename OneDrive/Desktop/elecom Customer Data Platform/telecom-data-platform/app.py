import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Airtel Insights | Telecom Data Platform", page_icon="📡", layout="wide")

# --- PREMIUM CSS ---
st.markdown("""
<style>
    .stApp { background: #0A0F1E; color: white; }
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 20px; border-radius: 16px; border: 1px solid #334155;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    .metric-card h3 { color: #94A3B8; font-size: 13px; margin: 0; letter-spacing: 1px; text-transform: uppercase; }
    .metric-card h1 { color: white; font-size: 32px; margin: 5px 0; }
    .metric-card p { color: #10B981; font-size: 13px; margin: 0; font-weight: 600; }
    .red p { color: #EF4444 !important; }
    h1, h2, h3 { color: white !important; }
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    div[data-testid="stSelectbox"] label { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load():
    churn = pd.read_csv('gold/churn_dataset.csv')
    net = pd.read_csv('gold/network_performance.csv')
    fact = pd.read_csv('gold/fact_calls.csv')
    cust = pd.read_csv('customers.csv')
    return churn, net, fact, cust

df_churn, df_net, df_fact, df_cust = load()

# --- HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("# 📡 **Telecom** <span style='color:#E40000'>Intelligence</span> Platform", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:16px;'>Real-Time Network Analytics • Churn Prediction • Airtel / Jio Scale Platform</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='text-align:right; padding-top:10px;'><span style='background:#10B981; color:white; padding:6px 14px; border-radius:20px; font-size:13px; font-weight:700;'>● LIVE • Updated Today</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- FILTERS ---
f1, f2, f3 = st.columns(3)
with f1:
    city_filter = st.selectbox("📍 Filter by City", ["All Cities"] + sorted(df_cust['city'].unique().tolist()))
with f2:
    plan_filter = st.selectbox("📦 Filter by Plan", ["All Plans", "Prepaid", "Postpaid"])
with f3:
    risk_filter = st.selectbox("⚠️ Churn Risk", ["All", "HIGH", "MEDIUM", "LOW"])

# Filter apply
df_churn_f = df_churn.copy()
if risk_filter != "All":
    df_churn_f = df_churn_f[df_churn_f['churn_risk'] == risk_filter]
if city_filter != "All Cities":
    cust_ids = df_cust[df_cust['city'] == city_filter]['customer_id'].tolist()
    df_churn_f = df_churn_f[df_churn_f['customer_id'].isin(cust_ids)]
if plan_filter != "All Plans":
    cust_ids = df_cust[df_cust['plan_type'] == plan_filter]['customer_id'].tolist()
    df_churn_f = df_churn_f[df_churn_f['customer_id'].isin(cust_ids)]

# --- KPI CARDS ---
total_calls = len(df_fact)
total_cust = len(df_churn)
high_risk = len(df_churn[df_churn['churn_risk'] == 'HIGH'])
avg_drop = df_fact['call_drop'].mean()*100
total_data = df_fact['data_used_gb'].sum()

k1, k2, k3, k4, k5 = st.columns(5)
with k1: st.markdown(f"<div class='metric-card'><h3>Total Calls</h3><h1>{total_calls:,}</h1><p>▲ 12.5% vs Yesterday</p></div>", unsafe_allow_html=True)
with k2: st.markdown(f"<div class='metric-card'><h3>Total Customers</h3><h1>{total_cust:,}</h1><p>▲ 2.1% Growth</p></div>", unsafe_allow_html=True)
with k3: st.markdown(f"<div class='metric-card red'><h3>High Churn Risk</h3><h1>{high_risk:,}</h1><p>▼ Needs Action!</p></div>", unsafe_allow_html=True)
with k4: st.markdown(f"<div class='metric-card'><h3>Avg Call Drop</h3><h1>{avg_drop:.2f}%</h1><p>Target: &lt; 2%</p></div>", unsafe_allow_html=True)
with k5: st.markdown(f"<div class='metric-card'><h3>Total Data Used</h3><h1>{total_data:,.0f} GB</h1><p>▲ 18% Surge</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CHARTS ROW ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 📊 Call Volume by City - Where is Network Load?")
    # FIXED: df_fact lo ne city undi, malli merge vaddu
    city_calls = df_fact.groupby('city').size().reset_index(name='calls')
    fig = px.bar(city_calls, x='city', y='calls', color='calls', color_continuous_scale='Reds', template='plotly_dark')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=340, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("### 🥧 Churn Risk Split")
    fig2 = px.pie(df_churn, names='churn_risk', values='total_calls', color='churn_risk',
                  color_discrete_map={'HIGH':'#EF4444','MEDIUM':'#F59E0B','LOW':'#10B981'}, template='plotly_dark', hole=0.55)
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=340)
    st.plotly_chart(fig2, use_container_width=True)

# --- TABLES ROW ---
t1, t2 = st.columns(2)

with t1:
    st.markdown("### 🔴 Top 20 High Churn Customers - Call Them NOW!")
    st.markdown("<p style='color:#94A3B8; font-size:13px;'>Ee customers ki ekkuva call drops vachayi - vallu Jio ki maripoye chance undi!</p>", unsafe_allow_html=True)
    show = df_churn_f[df_churn_f['churn_risk']=='HIGH'].sort_values('drop_rate', ascending=False).head(20)[['customer_id','city','total_calls','total_drops','drop_rate','churn_risk']]
    st.dataframe(show, use_container_width=True, hide_index=True)

with t2:
    st.markdown("### 📶 Worst Performing Towers - Fix Cheyali!")
    st.markdown("<p style='color:#94A3B8; font-size:13px;'>Ee towers lo signal problem undi - Engineer ni pampali!</p>", unsafe_allow_html=True)
    show2 = df_net.sort_values('drop_rate', ascending=False).head(20)[['tower_id','location','total_calls','drop_rate','signal_strength']]
    st.dataframe(show2, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("<p style='text-align:center; color:#64748B; font-size:13px;'>Built by Venga • Telecom Data Platform • Kafka • Spark • Snowflake • Airflow • Streamlit</p>", unsafe_allow_html=True)