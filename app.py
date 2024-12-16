# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:35:56 2024

@author: gowtham
"""
import streamlit as st
from helpers import common, loaders

# Set the page configuration
st.set_page_config(page_title="Dashboard", layout="wide")


# load custom css style
loaders.load_css("public/css/styles.css")

# render common sidebar
common.display_sidebar()

# render common nav bar
common.display_navbar()



# Main Content
st.title("Dashboard")
st.header("Welcome to the Interactive Dashboard!")

# KPI Section
st.header("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", "$500K", "5%")
col2.metric("Total Users", "12,000", "1.2%")
col3.metric("Customer Satisfaction", "89%", "-0.5%")

# Visualization Section
st.header("Visualizations")

# Example Line Chart
import pandas as pd
import numpy as np

data = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["Metric A", "Metric B", "Metric C"]
)
st.line_chart(data)


# Footer
st.markdown("""
    <div class="footer">
        <p> &copy; Footer information</p>
    </div>
""", unsafe_allow_html=True)
