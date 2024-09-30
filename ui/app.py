#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import random
import subprocess
import os
import sys
from datetime import datetime

#######################
# Page configuration
st.set_page_config(
    page_title="Opus digital mission control",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

path = 'history.csv'
citations = []
file_size = 0
# run build lake at startup
result = subprocess.call(["lake", "build"])
        

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
side_bg = 'background.png'
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
        st.page_link("https://opusdigital.io/contact-us/", label="Filecoin", icon="📧")

# URL of the rainbowkit deployment to embed
website_url = "http://localhost:3000"  # Replace with the URL of the website you want to embed

with st.expander('Connect your wallet', expanded=True):
    # Embed the website using an iframe
    st.components.v1.iframe(website_url, width=800, height=500)#, scrolling=True)
# wallet_address = st.text_input("Copy-paste the author's address:")

uploaded_files = st.file_uploader("Choose a .lean file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    file_size = sys.getsizeof(bytes_data)
    file_name = uploaded_file.name
    st.write("Reviewing: ", uploaded_file.name + "...")
    st.markdown("<div style=\"border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;\"><p style=\"color:green;\">" + bytes_data.decode("utf-8").replace('\n', '<br>') + "</p></div>", unsafe_allow_html=True)
    with open(os.path.join("Leanproject", file_name), "wb") as f:
        f.write(bytes_data)
    # add a new line for the new file
    with open('Leanproject.lean', 'r') as f:
        last_line = f.readlines()[-1]
    with open('Leanproject.lean', 'a') as file:
        file.write(str(last_line).partition(".")[0] + "." + file_name.partition(".")[0] + "\n")
    #result = subprocess.call(["lean", "--run", "my_file.lean"])
    result = subprocess.call(["lake", "build"])
    if result:
        st.markdown("<p style=\"color:red;\">⛔ Review failed</p>", unsafe_allow_html=True)
        os.remove(os.path.join("Leanproject", file_name))
        # File was faulty so remove it from the list to not break future builds
        with open('Leanproject.lean', 'r') as f:
            all_but_last_line = f.readlines()[:-1]
        with open('Leanproject.lean', 'w') as f:
            f.writelines(all_but_last_line)
    else:
        st.markdown("<p style=\"color:green;\">🏆 Review succeeded</p>", unsafe_allow_html=True)
        st.markdown("<p style=\"color:green;\">🌸 Your article has been published with id 12, citing articles with id 1 and 3</p>", unsafe_allow_html=True)
        wallet_address = "0x2F983dbe1c1ebeAd744eE6211F5CCF84E76A98D3"
        # st.markdown("<p style=\"color:green;\">🌸 Your article has been published with id 11, citing articles with id 10</p>", unsafe_allow_html=True)
        # wallet_address = "0x2F983dbe1c1ebeAd744eE6211F5CCF84E76A98D3"

        st.write("Citations: ", str(bytes_data).count('Leanproject'))
        citations = list(map(str, random.sample(range(400, 9000), str(bytes_data).count('Leanproject')))) # should have as many elements as there are Leanproject imports
        result = subprocess.call(["node", os.path.join("scripts", "publish.js"), "--author", wallet_address, "--citations", "1", "3"])
        result = subprocess.call(["node", "uploadFile.js", "--path", os.path.join("Leanproject", file_name)])
        # result = subprocess.call(["node", os.path.join("scripts", "publish.js"), "--author", wallet_address, "--citations", "10"])
        #st.write("I plan to execute:")
        #st.write(" ".join(["node", "os.path.join(\"scripts\", \"publish.js\")", "--author", wallet_address, "--citations", citations]))
        compiles = True

def publish_history():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    header = ["Timestamp", "WalletAddress", "FileSize [Byte]"]
    df = pd.DataFrame(data = [(dt_string, wallet_address, file_size)], columns = header)
    if not os.path.isfile(path):
        df.to_csv(path, columns = header)
    else:
        df.to_csv(path, mode='a', header=False)
    #st.write(pd.read_csv(path))
    #os.environ["LIGTHOUSE_API_KEY"]=TODO
    result = subprocess.call(["node", "uploadFile.js", "--path", os.path.join("Leanproject", file_name)])
    #st.write("Uploading ", os.path.join("Leanproject", file_name))
    #st.write(result)
    article_id = "1"
    # result = subprocess.call(["node", os.path.join("scripts", "activateArticle.js"), "--articleId", str(article_id)])
    #st.write("I plan to execute:")
    #st.write(" ".join(["node", "os.path.join(\"scripts\", \"activateArticle.js\")", "--articleId", "str(article_id)"]))
    compiles = False
    
if compiles:
    # if the file compiles we would like to know what is the price for publishing it and also
    # who to reward for the citations
    
    # we need to mint an NFT in order to retrieve the PoDSIs from the network
    # so we will have the address of the authors and list of PoDSIs to award them
    publishing_cost = 25
    # publishing_cost = 15
    st.write("Esimated cost of publishing: " + str(publishing_cost) + " SKR")
    # st.button("Publish", on_click=publish_history)

