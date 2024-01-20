import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from streamlit_option_menu import option_menu
from data_process.vis_im_event_log import plot_horizontal_bar_chart_activity, plot_start_activities, plot_end_activities, plot_activity_boxplot, plot_activity_distribution

if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('./data/data.csv')
df = st.session_state.df
if 'select_event_log_to_process' in st.session_state:
    del st.session_state.select_event_log_to_process
manual_select = 0

with st.sidebar:
    selected = option_menu("Dashboard", ["Log Summary", "Throughput Time",'Variant Explorer', 'Process Map'], 
    icons=['table', 'clock','stack', 'map'], menu_icon="inbox", manual_select= manual_select)


if 'selected_event_log' not in st.session_state:
    st.toast("Vui lòng chọn event log!!!!!")
elif selected == 'Log Summary':
        with st.container():
            st.header(f"Log Summary", divider='gray')
        if 'converted_event_log' in st.session_state:
            matching_workspace = df[df['name'] == st.session_state.selected_event_log]
            log_summary = st.session_state.converted_event_log

            with st.container():
                col1, col2, col3 = st.columns(3)
                with col1:
                    plot_horizontal_bar_chart_activity(log_summary,matching_workspace.iloc[0]['activity_column'])
                with col2: 
                    plot_start_activities(log_summary, matching_workspace.iloc[0]['timestamp_column']
                                          ,matching_workspace.iloc[0]['case_column']
                                          ,matching_workspace.iloc[0]['activity_column'] )
                with col3:
                    plot_end_activities(log_summary, matching_workspace.iloc[0]['timestamp_column']
                                          ,matching_workspace.iloc[0]['case_column']
                                          ,matching_workspace.iloc[0]['activity_column'] )
            with st.container():
                col4, col5 = st.columns(2)
                with col4:
                    plot_activity_distribution(log_summary, matching_workspace.iloc[0]['timestamp_column']
                                          ,matching_workspace.iloc[0]['case_column']
                                          ,matching_workspace.iloc[0]['activity_column'] )
                with col5:
                    plot_activity_boxplot(log_summary, matching_workspace.iloc[0]['timestamp_column']
                                          ,matching_workspace.iloc[0]['case_column']
                                          ,matching_workspace.iloc[0]['activity_column'] )
        else:
            st.session_state.converted_event_log = ''
elif selected == "Throughput Time":
    st.header("Throughput Time", divider='gray')
    st.session_state
elif selected == "Variant Explorer":
    st.header("Variant Explorer", divider='gray')
elif selected == "Process Map":
    st.header("Process Map", divider='gray')
