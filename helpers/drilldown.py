# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:43:13 2025

@author: gowth
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to SQLite Database
def get_connection():
    return sqlite3.connect("price_testing.db", check_same_thread=False)

# Fetch available dates
def get_dates():
    conn = get_connection()
    query = "SELECT DISTINCT date FROM price_testing ORDER BY date DESC"
    dates = pd.read_sql(query, conn)['date'].tolist()
    conn.close()
    return dates

# Fetch dropdown options dynamically
def get_dropdown_options(column):
    conn = get_connection()
    query = f"SELECT DISTINCT {column} FROM price_testing ORDER BY {column}"
    options = pd.read_sql(query, conn)[column].dropna().tolist()
    conn.close()
    return options

# Fetch data based on filters
def get_filtered_data(current_date, previous_date, region, business, desk, product):
    conn = get_connection()
    query = """
        SELECT * FROM price_testing 
        WHERE date IN (?, ?) 
        AND (? IS NULL OR region = ?)
        AND (? IS NULL OR business = ?)
        AND (? IS NULL OR desk = ?)
        AND (? IS NULL OR product = ?)
    """
    df = pd.read_sql(query, conn, params=[current_date, previous_date, region, region, business, business, desk, desk, product, product])
    conn.close()
    return df

# Streamlit UI
st.title("Price Testing Drill-Down Dashboard")

# Date selection
dates = get_dates()
current_date = st.selectbox("Select Current Date", dates, index=0)
previous_date = st.selectbox("Select Previous Date", dates, index=1)

# Filters
region = st.selectbox("Select Region", [None] + get_dropdown_options("region"))
business = st.selectbox("Select Business", [None] + get_dropdown_options("business"))
desk = st.selectbox("Select Desk", [None] + get_dropdown_options("desk"))
product = st.selectbox("Select Product", [None] + get_dropdown_options("product"))

# Fetch and display data
df = get_filtered_data(current_date, previous_date, region, business, desk, product)
if not df.empty:
    st.write("Filtered Data:", df)
    
    # Aggregated summary
    summary = df.groupby(["date", "region", "business", "desk", "product"]).agg({
        "pre_variance": "sum", "post_variance": "sum"
    }).reset_index()
    st.write("Aggregated Summary:", summary)
    
    # Variance Comparison Plot
    fig = px.bar(summary, x="product", y=["pre_variance", "post_variance"], barmode="group",
                 title="Pre vs Post Variance", labels={"value": "Variance"})
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected criteria.")
