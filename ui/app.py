#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import subprocess
import os

import streamlit as st
import pandas as pd
from db import *

st.set_page_config(
    page_title="Opus digital mission control",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
        

import base64
def sidebar_bg(side_bg):

   side_bg_ext = 'gif'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
side_bg = os.path.join("ui", "background.png")
sidebar_bg(side_bg)


#######################
# Sidebar
compiles = False
with st.sidebar:
    st.title('🌍 OpusDigital: market making democratized')
    with st.expander('Powered by', expanded=True):
        st.page_link("https://opusdigital.io/#", label="Homepage", icon="🏠")
        st.page_link("https://opusdigital.io/team/", label="Team", icon="👨‍👨‍👦‍👦")
        st.page_link("https://opusdigital.io/wp-content/uploads/2024/09/OpusDigital-Marketing-Presentation.pdf", label="Pitchdeck", icon="🧑‍🏫")
        st.page_link("https://opusdigital.io/contact-us/", label="Contact us", icon="📧")

with st.sidebar:
    st.title('Pick portfolio you want to view')
    option = st.selectbox(
        'Choose a portfolio:',
        [el[0] for el in get_portfolio_list().all()]
    )
# URL of the rainbowkit deployment to embed
website_url = "http://localhost:3000"  # Replace with the URL of the website you want to embed

st.title("Portfolio management")

# Retrieve data from PostgreSQL
df = get_portfolio_details(option)

# Display the dataframe in Streamlit
st.dataframe(df)
