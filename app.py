# pip install transformers
# pip install streamlit
# pip install torch

import streamlit as st
from transformers import pipeline

# Title for the app
st.title('Fill in the Blank Bot')

# Load the fill-mask pipeline 
fill_mask = pipeline('fill-mask')

# Text area for the user input
user_input = st.text_area("Enter a sentence with a <mask> in place of the missing word")

# Button to trigger the fill-mask function
if st.button('Fill the Blank'):
    # Predict the missing words 
    results = fill_mask(user_input)

    # Display the top 5 predictions 
    st.write("Top predictions:")
    for result in results:
        st.write(f"Prediction: {result['token_str']}, Confidence: {round(result['score'], 4)}")
