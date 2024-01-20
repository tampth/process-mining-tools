import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd



# 1. as sidebar menu
with st.sidebar:
    selected = option_menu("Workspace", ["Workspace Explorer", 'Add New Workspace', 'Edit Workspace'], 
        icons=['folder', 'folder-plus', 'pencil'], menu_icon="inbox", default_index=1)
    selected
# 4. Manual item selection
st.write(st.session_state)
if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 0) + 1) % 4
    manual_select = st.session_state['menu_option']
else:
    manual_select = None
    
selected4 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    orientation="horizontal", manual_select=manual_select, key='menu_4')
st.button(f"Move to Next {st.session_state.get('menu_option', 1)}", key='switch_button')
selected4


# Sample DataFrame for demonstration
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 22],
    'City': ['New York', 'San Francisco', 'Chicago']
}

df = pd.DataFrame(data)

# Function to highlight a specific column
def highlight_column(s, column_name, color='lightgreen'):
    if s.name == column_name:
        return [f'background-color: {color}'] * len(s)
    return [''] * len(s)

# Streamlit app
st.title('DataFrame Column Highlighter')

# Create a select box to choose the column to highlight
selected_column = st.selectbox('Select Column to Highlight', df.columns)

# Display the DataFrame with highlighting based on the selected column
st.dataframe(df.style.apply(highlight_column, column_name=selected_column, axis=0))

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

if st.button('Trial'):
    switch_page('import_event_log')
