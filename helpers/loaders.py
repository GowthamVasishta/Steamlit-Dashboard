# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 09:48:53 2024

@author: gowth
"""
import streamlit as st

def load_css(file_path):
    with open(file_path, "r") as css_file:
        css = css_file.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)