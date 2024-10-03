import pandas as pd
from sqlalchemy import create_engine, MetaData
"""
import erdantic 
from db import *
import base64
from io import BytesIO

def get_erd(st):
    metadata = MetaData(bind=engine)
    metadata.reflect()

    # Step 2: Create Entity Classes
    entities = []
    for table in metadata.sorted_tables:
        entities.append(erdantic.Entity(table.name, **{col.name: col.type for col in table.columns}))

    # Step 3: Generate ERD
    erd = erdantic.render(entities)

    # Convert the ERD to image
    image_bytes = BytesIO()
    erd.savefig(image_bytes, format='png')
    image_bytes.seek(0)

    # Encode the image for Streamlit
    img_base64 = base64.b64encode(image_bytes.getvalue()).decode()
    img_html = f'<img src="data:image/png;base64,{img_base64}" />'

    # Display in Streamlit
    st.markdown(img_html, unsafe_allow_html=True)
"""