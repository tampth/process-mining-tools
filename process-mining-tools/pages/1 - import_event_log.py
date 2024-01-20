import streamlit as st
import numpy as np

import pandas as pd
import pm4py
import time
import re
from data_process.vis_im_event_log import visualize_activity_counts, plot_case_count_over_time
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
def save_to_workspace(data):
    return data.to_csv('./data/data.csv',index=False)

def save_data(csv, key):
    return csv.to_csv(f'./data/eventlog{key}.csv',index=False)

def add_new_event_log(df, df_exp, path):
    add_name = df_exp['name']
    add_description = df_exp['description']
    created_by= df_exp['created_by']
    create_at = df_exp['created_at']
    event_log_id = path
    case_column = st.session_state.case_id
    activity_column = st.session_state.activity
    timestamp_column = st.session_state.timestamp
    add_status='Ready'

    form=st.form("Add_Event_Log",clear_on_submit=True)
    with form:
        st.write("Thực hiện chuyển đổi thành công, bạn có muốn lưu lại nhật ký?")
        col1, col2 = st.columns(2)
        with col1:
            submitted=st.form_submit_button("Save", type="primary")
        with col2:
            cancelled=st.form_submit_button("Cancel")
        if submitted:
            for i, workspace in df.iterrows():
                if workspace['name'] == df_exp['name']:
                    df.loc[i]=[add_name,add_description,created_by, create_at, event_log_id,case_column,activity_column,timestamp_column ,add_status]
                    st.subheader("Add Event Log Successful!")
                    st.write("```Saved```")
                    st.session_state.df = df
                    save_to_workspace(df)
                    del st.session_state.select_event_log_to_process
                    switch_page('workspace')
        elif cancelled:
            st.write("```Cancelled```")
            ### If after submission you want to reset, go to the len(df) and delete that row###


header = st.container()

col1, col2 = st.columns(2)

if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('./data/data.csv')
df = st.session_state.df

if 'import_event' not in st.session_state:
    st.session_state.import_event = ''
    with header:
        st.header(f"Import event log", divider='gray')
else:
    # Assuming st.session_state["import_event"] contains the string "add event log 1"
    event_string = st.session_state["import_event"]

    # Extracting the numeric value using regular expression
    numeric_value = re.search(r'\b\d+\b', event_string).group()

    # Converting the numeric value to an integer
    numeric_value = int(numeric_value)

    for index, row in df.iterrows():
        if index == numeric_value:
            st.session_state["select_event_log_to_process"] = row[0]
            break
    with header:
        st.header(f"Import event log for process {st.session_state.select_event_log_to_process}", divider='gray')

with st.sidebar:
    uploaded_files = st.file_uploader("Choose a CSV file")


if uploaded_files is not None:
    with st.expander("Preview and Mapping data", expanded=False):
        col1, col2 = st.columns(2)
        event_log = pd.read_csv(uploaded_files)

        with col1:
            # Function to highlight selected column
            def highlight_column(s, column_name, color):
                if s.name == column_name:
                    return [f'background-color: {color}'] * len(s)
                return [''] * len(s)
            def form_callback():
                selected_column1 = st.session_state.case_id
                selected_column2 = st.session_state.activity
                selected_column3 = st.session_state.timestamp
            if 'case_id' not in st.session_state:
                st.dataframe(event_log.head(100))
            else: 
                st.dataframe(event_log.head(100).style.apply(highlight_column, column_name=st.session_state.case_id, color='lightgreen', axis=0)
                                                    .apply(highlight_column, column_name=st.session_state.activity, color='violet',axis=0)
                                                    .apply(highlight_column, column_name=st.session_state.timestamp, color='skyblue',axis=0))

            
        with col2:
            with st.container(border=True):
                st.write("Attribute mapping")
                #Case select
                case = st.selectbox(":green[Case ID:]", event_log.columns, index=None, placeholder="Select attribute", key="case_id", on_change=form_callback)

                #Activity select
                activity = st.selectbox(":violet[Activity Name:]", event_log.columns, index=None, placeholder="Select attribute", key="activity", on_change=form_callback)

                #Timestamp select
                timestamp = st.selectbox(":blue[Timestamp:]", event_log.columns, index=None, placeholder="Select attribute",key="timestamp", on_change=form_callback)

                submited = st.button("Start Convert")
    if submited:
        col1, col2 = st.columns(2)
        if 'convert_event_log' not in st.session_state:
            st.session_state.convert_event_log = event_log
        with st.sidebar:
            text_bar = st.info('Starting import eventlog...', icon="ℹ️")
            # Add a placeholder
            latest_iteration = st.empty()
            bar = st.progress(0)

            for i in range(100):
                # Update the progress bar with each iteration.
                bar.progress(i + 1)
                time.sleep(0.01) 
            time.sleep(1)
            text_bar.empty()
            bar.empty()
        
        #Case explore
        if 'case_id' and 'acitivity' != None:
            with col1:
                visualize_activity_counts(event_log, event_log[st.session_state.case_id].nunique()
                                      , event_log[st.session_state.activity].nunique()
                                      , st.session_state.activity)
        #Timestamp explore
        if 'timestamp' != None:
            with col2:
                event_log[st.session_state.timestamp] = pd.to_datetime(event_log[st.session_state.timestamp], errors='coerce')
                min_date = event_log[st.session_state.timestamp].min().date()
                max_date = event_log[st.session_state.timestamp].max().date()
                plot_case_count_over_time(event_log, min_date, max_date)

    with st.sidebar:
        if 'convert_event_log' in st.session_state:
            matching_workspace = df[df['name'] == st.session_state.select_event_log_to_process]
            path = f'./data/eventlog{st.session_state.select_event_log_to_process}.csv'
            save_data(event_log, st.session_state.select_event_log_to_process)
            add_new_event_log(df, matching_workspace.iloc[0], path)

                                                                                                                                   
            