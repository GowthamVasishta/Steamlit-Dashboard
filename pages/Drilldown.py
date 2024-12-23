# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 12:07:49 2024

@author: gowth
"""


import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

import streamlit as st
import json
from helpers import common, loaders
st.set_page_config(page_title="Dashboard", layout="wide")

# Call the function to inject the CSS
loaders.load_css("public/css/styles.css")

common.display_sidebar()

common.display_navbar()

# Set the page configuration
#st.set_page_config(page_title="Dashboard", layout="wide")

st.title("Comprehensive Dashboard")

# # Display selected values in Streamlit (to print the selected values)
# selected_values = st.empty()

# # Listen to the selection parameters and display the selected values

# def get_selected_values():
#     selected_businesses = business_select.selected
#     selected_desks = desk_select.selected
#     selected_products = product_select.selected
    
#     return selected_businesses, selected_desks, selected_products

# selected_businesses, selected_desks, selected_products = get_selected_values()

# # Display the selected values in Streamlit
# with selected_values:
#     st.write(f"Selected Businesses: {selected_businesses}")
#     st.write(f"Selected Desks: {selected_desks}")
#     st.write(f"Selected Products: {selected_products}")


@st.cache_data
def get_data():
    # Define constants
    num_days = 10
    businesses = [f"B{i}" for i in range(1, 8)]
    desks = [f"D{i}" for i in range(1, 11)]
    products = [f"P{i}" for i in range(1, 8)]
    traders = [f"T{i}" for i in range(1, 8)]

    # Create a multi-index for all combinations
    unique_combinations = pd.MultiIndex.from_product(
        [
            pd.date_range(start="2023-12-01", periods=num_days),  # Changed to a past date
            businesses,
            desks,
            products,
            traders,
        ],
        names=["Date", "Business", "Desk", "Product", "Trader"],
    )

    # Create a DataFrame from the multi-index
    df_full = pd.DataFrame(index=unique_combinations).reset_index()

    # Add random data for numeric columns
    df_full["Pre"] = np.random.randint(-1000000, 1000000, size=len(df_full))
    df_full["Post"] = np.random.randint(-1000000, 1000000, size=len(df_full))
    df_full["Notional"] = np.random.randint(-20000000, 20000000, size=len(df_full))
    df_full["MV"] = np.random.randint(-20000000, 20000000, size=len(df_full))

    return df_full

# Load data
data = get_data()

# Selections for drill-down
business_select = alt.selection_point(fields=["Business"], empty="all")
desk_select = alt.selection_point(fields=["Desk"], empty="all")
product_select = alt.selection_point(fields=["Product"], empty="all")

#hover = alt.selection_single(fields=["Business"], on="mouseover", nearest=True, init={"Business": "B3"})


# Chart 1: Business-level pie chart with Pre numbers
business_pie = (
    alt.Chart(data)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("sum(Pre):Q", title="Total Pre"),
        color=alt.Color("Business:N", title="Business"),
        tooltip=["Business", "sum(Pre):Q"],
        fillOpacity=alt.condition(business_select, alt.value(1), alt.value(0.3))
    )
    .add_params(business_select)  # Updated to add_params
    .properties(title="Business-Level Pre Numbers", width=400)
    
)

desk_bar2 = (
    alt.Chart(data)
    .mark_bar().encode(
        x = alt.X("Desk:N")  ,
        y = alt.Y("sum(value):Q"),
        color=alt.Color("variable:N", title="Metric"),
        xOffset="variable:N",
        fillOpacity=alt.condition(desk_select, alt.value(1), alt.value(0.3))
    ).transform_fold(
        fold=["Pre", "Post"],  # Folds Pre and Post columns into a single column
        as_=["variable", "value"]
    ).transform_filter(business_select).add_params(desk_select)
    
)

# Chart 2: Desk-level bar chart showing adjacent Pre and Post numbers
desk_bar = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X("Desk:N", title="Desk"),
        y=alt.Y("sum(value):Q", title="Numbers"),
        color=alt.Color("variable:N", title="Metric"),
        column=alt.Column("variable:N", header=alt.Header(title="Pre vs Post", orient="bottom")),
        tooltip=["Desk", "variable:N", "sum(value):Q"],
        fillOpacity=alt.condition(desk_select, alt.value(1), alt.value(0.3))
    )
    .transform_filter(business_select)
    .transform_fold(
        fold=["Pre", "Post"],  # Folds Pre and Post columns into a single column
        as_=["variable", "value"]
    )
    .properties(title="Desk-Level Pre and Post Numbers", width=400)
    .transform_calculate(
        # Order Pre first in the chart
        variable_order="if(datum.variable === 'Pre', 0, 1)"
    )
    .encode(
        column=alt.Column("variable_order:O", sort=[0, 1])  # Sorts the variable_order to show Pre first
    )
    .properties(title="Desk-Level Pre and Post Numbers", width=400)

)


desk_combined = (desk_bar).add_params(desk_select)  # Updated to add_params

# Chart 3: Product-specific pie chart with Pre numbers
product_pie = (
    alt.Chart(data)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("sum(Pre):Q", title="Total Pre"),
        color=alt.Color("Product:N", title="Product"),
        tooltip=["Product", "sum(Pre):Q"]
    )
    .transform_filter(business_select, desk_select)  # Apply the desk filter
    .add_params(product_select)  # Add the product selection
    .properties(title="Product-Level Pre Numbers", width=400)
)



# Capture and display the selected business when user clicks on the pie chart
selected_business = business_select


if selected_business:
    selected_business_value = selected_business
    st.write(f"Business: {selected_business_value}")
else:
    st.write("No business selected")

print(selected_business['Business'])

# Arrange charts in a layout
layout = business_pie |  desk_bar2 | product_pie
#bottom_row = product_pie
layout2 = product_pie

#layout = top_row & bottom_row

st.altair_chart(layout, theme = None, use_container_width=True)

#st.altair_chart(layout2, use_container_width=True)
#st.altair_chart(product_pie)
# & (product_pie | product_pie_duplicate)


