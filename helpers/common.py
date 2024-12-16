# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:33:35 2024

@author: gowth
"""
import streamlit as st


def display_sidebar():
    
    # Sidebar Content
    st.sidebar.markdown("""
        <div class="sidebar-logo">
        <span style='font-size:90px; text-align: center; margin-right: 5px;'>&#8493;</span>    
        <h1> Dashboard Name</h1>
        </div>
        <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Sub title 1")
    st.sidebar.page_link("app.py", label="Home", icon =":material/home:")
    st.sidebar.page_link("pages/Analysis.py", label="Page 2", icon =":material/monitoring:")
    
    st.sidebar.title("sub title 2")
    st.sidebar.page_link("pages/Analysis.py", label="Page 3", icon =":material/donut_small:")
    st.sidebar.page_link("pages/Analysis.py", label="Page 4", icon =":material/person:")
    



def display_navbar():
    st.markdown('''
        <div class="navbar">
            <div class="navbar-logo">Dashboard Name</div>
            <div class="navbar-links">
                <a href="#reports"> <span class="material-symbols-rounded">summarize</span> Reports</a>
                <a href="/Analysis"> <span class="material-symbols-rounded">settings</span> Settings</a>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    

