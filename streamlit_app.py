import streamlit as st
import zipfile
import os
from pathlib import Path
import instagram_data_class as ig_data_class
import main

# Setting up titles
st.title("Your Instagram Data Visualizer")

instagram_data = st.file_uploader("Please upload your Instagram Data here", accept_multiple_files=True)