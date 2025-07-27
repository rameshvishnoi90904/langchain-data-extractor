import streamlit as st
import pandas as pd

from data_extractor import extract

# This function will handle the logic of cleaning up the keys
def cleanup_keys():
    if 'num_keys' in st.session_state:
        keys_from_last_run = [st.session_state.get(f"key_{i}", "") for i in range(st.session_state.num_keys)]
        valid_keys = [key for key in keys_from_last_run if key]

        # Clean up old keys from session state
        for i in range(st.session_state.num_keys):
            if f"key_{i}" in st.session_state:
                del st.session_state[f"key_{i}"]

        # Set the new state for the widgets
        st.session_state.num_keys = len(valid_keys)
        for i, key in enumerate(valid_keys):
            st.session_state[f"key_{i}"] = key

# This block will run at the start of a rerun triggered by the extract button
if st.session_state.get('extract_clicked'):
    st.session_state.extract_clicked = False  # Reset the flag
    cleanup_keys()

# 1. Title
st.title("Financial Data Extractor")

# 2. Input box
input_paragraph = st.text_area("Enter a paragraph from a news article", height=200)

# 3. Button
extract_button = st.button("Extract")

# Initialize the number of keys in session state if it doesn't exist
if 'num_keys' not in st.session_state:
    st.session_state.num_keys = 1

# Button to add a new key
if st.sidebar.button("Add New Key"):
    st.session_state.num_keys += 1
    if 'extracted_df' in st.session_state:
        del st.session_state.extracted_df
    st.rerun()

# Create a list to store the keys
keys = []
for i in range(st.session_state.num_keys):
    key = st.sidebar.text_input(f"Enter Key to be extracted {i+1}", key=f"key_{i}" ,placeholder="e.g., 'Revenue', 'Profit', 'Loss'")
    keys.append(key)

# 4. Upon clicking the button, show a table
if extract_button:
    st.session_state.extract_clicked = True

    if input_paragraph:
        valid_keys = [key for key in keys if key]
        if valid_keys:
            extracted_data = extract(input_paragraph, valid_keys)
            data = {
                'Measure': valid_keys,
                'Value': [extracted_data.get(key) for key in valid_keys]
            }
            st.session_state.extracted_df = pd.DataFrame(data)
        else:
            st.warning("Please enter at least one key to extract.")
            if 'extracted_df' in st.session_state:
                del st.session_state.extracted_df
    else:
        st.warning("Please enter a paragraph to extract data from.")
        if 'extracted_df' in st.session_state:
            del st.session_state.extracted_df
    st.rerun()

# Display the table if it exists in the session state
if 'extracted_df' in st.session_state:
    st.table(st.session_state.extracted_df)
