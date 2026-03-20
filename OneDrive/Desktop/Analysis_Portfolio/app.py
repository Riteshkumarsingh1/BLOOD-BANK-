import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.set_page_config(page_title="Customer Analysis", layout="wide")
st.title("Customer Shopping Behaviour Analysis")
st.markdown("---")

engine = create_engine(
    "postgresql+psycopg://postgres:12345@localhost:5432/Data_Analytics_db"
)

@st.cache_data
def load_data():
    df = pd.read_sql('SELECT * FROM customer', engine)
    return df

df = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", len(df))
col2.metric("Avg Purchase", f"${df['purchase amount'].mean():.2f}")
col3.metric("Total Revenue", f"${df['purchase amount'].sum():.2f}")

st.markdown("---")

gender = st.sidebar.selectbox("Select Gender", ["All"] + list(df['gender'].unique()))
if gender != "All":
    df = df[df['gender'] == gender]

st.subheader("Revenue by Category")
cat_rev = df.groupby('category')['purchase amount'].sum().reset_index()
st.bar_chart(cat_rev.set_index('category'))

st.subheader("Raw Data")
st.dataframe(df)