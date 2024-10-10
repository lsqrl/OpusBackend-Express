import streamlit as st
import pandas as pd
import altair as alt
import os
from PIL import Image  # Import Pillow for image handling
from datetime import datetime
from db import *
from service import *
from erd import *

pd.options.mode.chained_assignment = None

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


########################################################################################################################################################################################
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
    st.text('@localhost:5000 - Data Model')
    st.text('@localhost:5001 - Pricer')
    st.text('@localhost:5002 - Automated Risk Manager ')
    st.text('@localhost:5003 - Intelligent Market Maker')

st.title("Portfolio management")
########################################################################################################################################################################################
# Retrieve data from PostgreSQL
df = get_portfolio_details(option)
df_portfolio_details = df

# Display each type of trade from the selected protfolio
st.dataframe(df)
trade_types = list(set(df['instrument_name'].to_list()))
if len(trade_types) > 0:
    columns = st.columns(len(trade_types))
    for i in range(len(trade_types)):
        # Add content to each column
        with columns[i]:
            st.header(trade_types[i])
            trade_ids = df[df['instrument_name'] == trade_types[i]]['trade_id'].to_list()
            trade_ids = list(map(str, trade_ids))
            df_detail = get_trade_detail(trade_ids, trade_types[i])
            st.dataframe(df_detail.iloc[:, 1:])

########################################################################################################################################################################################

columns = st.columns(4)
with columns[0]:
    # Define a function to be called
    def get_adjusted_price(trade_id):
        if len(df_portfolio_details) > 0:
            st.write("This is the adjusted price")
            st.text("Demo for: FXOption trade_id " + str(trade_id))
            with st.spinner("Processing..."):
                test_fx_option = get_trade_detail([str(trade_id), ], 'FXOption')
                #st.success(test_fx_option)
                data = test_fx_option.iloc[0]
                data["expiry_time"] = str(data["expiry_time"])
                data["expiry_time"] = data["expiry_time"].replace(' ', 'T') + 'Z' # to get '%Y-%m-%dT%H:%M:%SZ')
                URL, status, response = call_imm('displayAdjustedPrice', 'POST', data.to_json())
            st.text(URL + " " + str(status))
            st.write(response)
        else:
            st.write("This portfolio is empty. Please book a trade first before requesting the adjusted price.")
    if len(df_portfolio_details) > 0:
        trade_id = st.selectbox(
            'Choose a trade_id:',
            df[df['instrument_name'] == 'FXOption']['trade_id'].to_list())
        if st.button("Display adjusted price"):
            # Call the function when the button is clicked
            get_adjusted_price(trade_id)

with columns[1]:
    option = st.selectbox(
                'Trade type:',
                ["FXOption", "FXSpot", "FiatFunding"], #[el[0] for el in sorted(get_trade_type().all()[1:])], 
                index=1
                
            )
    # Button to open the form
    if st.button("Book trade"):
        # Create the form after button is clicked
        with st.form("book_trade"):
            # Add form elements
            st.text("Selected option is: " + option)
            
            df = pd.DataFrame(
                [
                {"command": "st.selectbox", "rating": 4, "is_widget": True},
                {"command": "st.balloons", "rating": 5, "is_widget": False},
                {"command": "st.time_input", "rating": 3, "is_widget": True},
            ]
            )
            edited_df = st.data_editor(df)

            favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
            st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

            st.write("Table details")
            details = get_table_details(option).all()
            st.data_editor(pd.DataFrame(details, columns=["name", "type", "relationship"]))
            #get_quote = st.button("Get Quote") # will be calling the pricer
            submit = st.form_submit_button("Book (confirmation button)")
        # Process the form submission
        if submit:
            st.write(f"Booking {option}")

# Title of the app
st.title("Streamlit developer helper")

# Create tabs
tabs = st.tabs(["Service API", "Entity Relationship Diagram", "UI Design"])
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)

    # Add content to each column
    with col1:
        st.header("Pricer method list:")
        for item in get_service_method_list(base_url_pricer):
            st.json(item)
        if len(df) > 0:
            st.header("Method call example:")
            URL, status, response = call_pricer('calculatePrice', 'GET', dict())
            st.text(URL + " " + str(status))
            st.write(response)
            URL, status, response = call_pricer('calculateGreeks', 'GET', dict())
            st.text(URL + " " + str(status))
            st.write(response)

    with col2:
        st.header("Intelligent Market Makert method list:")
        for item in get_service_method_list(base_url_imm):
            st.json(item)
        if len(df) > 0:
            st.header("Method call example:")
            df = df_portfolio_details
            trade_id = df[df['instrument_name'] == 'FXOption'].iloc[-1]['trade_id']
            st.text("Demo for: FXOption trade_id " + str(trade_id))
            test_fx_option = get_trade_detail([str(trade_id), ], 'FXOption')
            data = test_fx_option.iloc[0]
            data["expiry_time"] = str(data["expiry_time"])
            data["expiry_time"] = data["expiry_time"].replace(' ', 'T') + 'Z' # to get '%Y-%m-%dT%H:%M:%SZ')
            URL, status, response = call_imm('displayAdjustedPrice', 'POST', data.to_json())
            st.text(URL + " " + str(status))
            st.write(response)

    with col3:
        st.header("Automated Risk Manager method list:")
        for item in get_service_method_list(base_url_arm):
            st.json(item)

    with col4:
        st.header("Database Model method list:")
        for item in get_service_method_list(base_url_database_prod):
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
    #get_erd(st)