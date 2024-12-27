import streamlit as st
import pandas as pd
from pathlib import Path
from instagram_data_class_st import InstagramData_ST

# Setting up titles
st.title("Your Instagram Data Visualizer")

uploaded_files = st.file_uploader("Please drag and drop your followers_and_following and liked folder here", accept_multiple_files=True)
# Dictionary to store uploaded files by their names
file_dict = {}

if uploaded_files:
    # Iterate through uploaded files
    for uploaded_file in uploaded_files:
        # Save the file in a dictionary with its name as the key
        file_dict[uploaded_file.name] = uploaded_file

    # Match specific files by name
    followers_file = file_dict.get('followers_1.json', None)
    following_file = file_dict.get('following.json', None)
    liked_comments_file = file_dict.get('liked_comments.json', None)
    liked_posts_file = file_dict.get('liked_posts.json', None)
    post_comments_file = file_dict.get('post_comments.json', None)

    # Load each file if it exists
    if followers_file:
        followers_data = pd.read_json(followers_file)
        st.write("Followers Data", followers_data.head())
    
    if following_file:
        following_data = pd.read_json(following_file)
        st.write("Following Data", following_data.head())
    
    if liked_comments_file:
        liked_comments_data = pd.read_json(liked_comments_file)
        st.write("Liked Comments Data", liked_comments_data.head())
    
    if liked_posts_file:
        liked_posts_data = pd.read_json(liked_posts_file)
        st.write("Liked Posts Data", liked_posts_data.head())
    
    if post_comments_file:
        post_comments_data = pd.read_json(post_comments_file)
        st.write("Post Comments Data", post_comments_data.head())

# Handle missing files
    missing_files = [
        name for name in ['followers_1.json', 'following.json', 
                          'liked_comments.json', 'liked_posts.json', 
                          'post_comments.json']
        if name not in file_dict
    ]

    if missing_files:
        st.warning(f"Missing files: {', '.join(missing_files)}")

    userInstagramDataClass = InstagramData_ST(following_file, followers_file, liked_comments_file, liked_posts_file, post_comments_file)
