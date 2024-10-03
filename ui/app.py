#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import subprocess
import os
from PIL import Image  # Import Pillow for image handling

import streamlit as st
import pandas as pd
from db import *
from service import *

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
    st.title('Using 🌍OpusDigital® services:')
    st.text('Data Model')
    st.text('Pricer')
    st.text('Automated Risk Manager')
    st.text('Intelligent Market Maker')
# URL of the rainbowkit deployment to embed
website_url = "http://localhost:3000"  # Replace with the URL of the website you want to embed

st.title("Portfolio management")

# Retrieve data from PostgreSQL
df = get_portfolio_details(option)

# Display the dataframe in Streamlit
st.dataframe(df)


# Button to open the form
if st.button("Book trade"):
    # Create the form after button is clicked
    with st.form("book_trade"):
        # Add form elements
        option = st.selectbox(
            'Trade type:',
            [el[0] for el in sorted(get_trade_type().all()[1:])], index=1
            
        )
        age = st.number_input("Age", min_value=0)
        favorite_color = st.color_picker("Pick a color")
        
        # Add a submit button
        #get_quote = st.button("Get Quote") # will be calling the pricer
        submit = st.form_submit_button("Book (confirmation button)")

    # Process the form submission
    if submit:
        st.write(f"Hello {name}, you are {age} years old, and your favorite color is {favorite_color}.")


import streamlit as st

# Title of the app
st.title("Streamlit developer helper")

# Create tabs
tabs = st.tabs(["Service API", "Entity Relationship Diagram", "UI Design"])
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)

    # Add content to each column
    with col1:
        st.header("Pricer method list:")
        for item in get_pricer_method_list(base_url_pricer):
            st.json(item)

    with col2:
        st.header("Intelligent Market Makert method list:")
        for item in get_pricer_method_list(base_url_imm):
            st.json(item)

    with col3:
        st.header("Automated Risk Manager method list:")
        for item in get_pricer_method_list(base_url_arm):
            st.json(item)

    with col4:
        st.header("Database Model method list:")
        for item in get_pricer_method_list(base_url_database_prod):
            st.json(item)


with tabs[1]:
    st.header("This is Entity Relationship Diagram of OpusDigital Data Model")
    st.write("Supported by PostgresDB")
    st.write("WIP: Goal - interactive graph")
    st.write("Example of goal visuals: https://schemascope.dcc.sib.swiss/")
    #st.line_chart([1, 2, 3, 4, 5])
    #get_erd_graph(st)
    image_path = os.path.join('ui', 'od_erd.png')  # Replace with your image path or URL
    image = Image.open(image_path)
    st.image(image)



with tabs[2]:
    st.header("Random Quote")
    st.text("Our deepest fear is not that we are inadequate. Our deepest fear is that we are powerful beyond measure")
    # Embed Excalidraw using an iframe
    excalidraw_room_url = "https://excalidraw.com/#room=1da649cb038c3dc89a65,kRBSasixyV172S99-WKR9Q"
    
    iframe_code = f"""
    <iframe 
        src="{excalidraw_room_url}",
        width="100%" 
        height="600px" 
        style="border: none;">
    </iframe>
    """
    # Display the iframe in the Streamlit app
    st.markdown(f"{excalidraw_room_url}")
    #st.markdown(iframe_code, unsafe_allow_html=True)
    st.image(os.path.join('ui', 'od_des.png'))
