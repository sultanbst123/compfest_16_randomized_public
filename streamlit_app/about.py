import streamlit as st
import pandas as pd
import numpy as np

# clear cache
st.cache_data.clear()

# layout config
st.set_page_config(page_title="Burnout Report", 
                   layout="wide", 
                   page_icon="📊")

# st.error("⛔️ development mode⛔️")


st.markdown("<h2 style='text-align: center;'>Employees Burning Out</h2>", unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("""
                <h6 style='text-align: center;'>
                    We created this application to help companies assess employee burnout and raise awareness about mental health among our users.
                    <br>
                    *The prediction results may not be accurate.
                    <br><br>
                </h6>

                There are 2 sections in the navigation: Insights and Predictions.
                <br>
                1. The Insights section provides insight into how employees can experience burnout.
                <br>
                2. The Predictions section offers predictions on how big employee burnout can be based on features.
                <br><br>

                You can provide feedback to help us improve our application by creating a pull request 
                <a href="https://github.com/sultanbst123/compfest_16_randomized/pulls">here</a>.

                <h6 style='text-align: center;'> 
                    Good Luck 😁 
                </h6>
                """, unsafe_allow_html = True)

