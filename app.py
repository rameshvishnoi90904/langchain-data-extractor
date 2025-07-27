import streamlit as st
import pandas as pd

from  data_extractor import extract 
# 1. Title
st.title("Financial Data Extractor")

# 2. Input box
input_paragraph = st.text_area("Enter a paragraph")

# 3. Button
extract_button = st.button("Extract")

# 4. Upon clicking the button, show a table
if extract_button and input_paragraph:
    # Call the extract function
    extracted_data = extract(input_paragraph)
    
    # Create the DataFrame from the extracted data
    data = {
        'Measure': ['Revenue', 'Eps'],
        'Estimated': [extracted_data.get('revenue_expected'), extracted_data.get('eps_expected')],
        'Actual': [extracted_data.get('revenue_actual'), extracted_data.get('eps_actual')]
    }
    df = pd.DataFrame(data)
    st.table(df)
elif extract_button:
    st.warning("Please enter a paragraph to extract data from.")
