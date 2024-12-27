import streamlit as st

st.write("# Please drag and drop your followers_and_following folder below")
uploaded_files = st.file_uploader("followers_and_following", accept_multiple_files=True)