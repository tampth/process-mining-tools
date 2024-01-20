import datetime
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from streamlit_extras.switch_page_button import switch_page
import re

def check_password():
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] == st.secrets["username"] # if username is included in secrets file
            and st.session_state["password"] == st.secrets["passwords"] # if password under the username is matching the one given
        ):
            st.session_state["password_correct"] = True # if those conditions are met then our password is correct
            del st.session_state["password"]  # delete the password from session state
            del st.session_state["username"]  # delete the username from session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.set_page_config(page_title="Login", layout="wide", initial_sidebar_state= "collapsed")
        # First run, show inputs for username + password
        st.header("Login 👤")
        st.text_input("Username 👤", on_change=password_entered, key="username")
        st.text_input(
            "Password 🔑", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.header("Login")
        st.text_input("Username 👤", on_change=password_entered, key="username")
        st.text_input(
            "Password 🔑", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True
    
def save_data(data):
    return data.to_csv('./data/data.csv',index=False)
    
def cancel_data(data,id):
    data=data.drop(axis=0,index=id)
    
def add_new_workspace(df,df_exp): 
    id=len(df_exp)
    created_by= st.secrets["username"]
    event_log_id = None
    case_column = None
    activity_column = None
    timestamp_column = None
    add_status='Not have event log'

    form=st.form("Add_New_Workspace",clear_on_submit=True)
    with form:
        add_name=st.text_input(label='Name',value="")
        add_description=st.text_area(label='Description',value="")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            submitted=st.form_submit_button("Submit", type="primary")
        with col2:
            cancelled=st.form_submit_button("Cancel")
        if submitted:
            if add_name in list(df.name):
                st.write('```Workspace already exist```')
            elif add_name!=None and add_description!=0:
                df_exp.loc[id]=[add_name,add_description,created_by, datetime.datetime.now(), event_log_id,case_column,activity_column,timestamp_column,add_status]
                st.subheader("Data Added Successful!")
                preview=df_exp.style.apply(lambda x: ['background-color: green' if (i == id) else '' for i in x.index.values], axis=0)
                st.dataframe(preview,width=4000)
                st.write("```Saved```")
                st.session_state.df = df_exp
                save_data(df_exp)
            else:
                st.write("```Input Boxes are empty...```")
        elif cancelled:
            st.write("```Cancelled```")
            ### If after submission you want to reset, go to the len(df) and delete that row###

def form_callback():
    for index, row in df.iterrows():
        if st.session_state[f"add event log {index}"]:
            st.session_state['import_event'] = f"add event log {index}"
            break

def change_page():
    session_statements = st.session_state
    # Get integer values where selected_event_log has a value of True
    true_values = [int(key.split()[-1]) for key, value in session_statements.items() if "selected_event_log" in key and value]

    if len(true_values) > 1:
        st.toast('Bạn chỉ được phép chọn 1 workspace')
        # You can show an alert or take other actions here
    else:
        df = pd.DataFrame(st.session_state.df)
        column_name = 'event_log_id'
        path = df.loc[true_values, column_name]
        if 'converted_event_log' not in st.session_state:
            if 'selected_event_log' not in st.session_state:
                selected_event = df.loc[true_values, 'name']
                st.session_state.selected_event_log = selected_event.iloc[0]
            st.session_state.converted_event_log = pd.read_csv(f"{path.iloc[0]}")

if __name__ == "__main__":
    if True:
        #config
        st.set_page_config(page_title="Workspace Explorer", page_icon=":inbox_tray:", layout="wide", initial_sidebar_state= "expanded")
    
        hide_streamlit_style = """
                <head>
                <style>
                #MainMenu{visibility: hidden;}
                .css-fk4es0{display:none;}
                .css-1lsmgbg {display: none;}
                .myFooter{color:rgba(250, 250, 250, 0.6); margin-top: 150px; text-align: center;}
                .myFooter a{color: rgb(255, 75, 75); font-weight: bolder;}
                .css-10trblm{color:rgb(255, 75, 75); text-align:center;}
                .css-16huue1 {color:rgb(255, 75, 75); font-size:18px;}
                .css-v37k9u p{color:#edf5e1; font-size: 18px;}
                .css-1q8dd3e{color:rgb(255, 75, 75);}
                .css-1q8dd3e:hover{color:#edf5e1; border-color:rgb(255, 75, 75);}
                .css-17ziqus {background-color: brown; visibility: visible}
                .css-ffhzg2 {text-align: center;}
                </style>
                <title> Process Mining Tool </title>
                </head>
                <script>document.getElementById("demo").innerHTML = new Date().getFullYear();</script>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        
        # 1. as sidebar menu
        if 'df' not in st.session_state:
            st.session_state.df = pd.read_csv('./data/data.csv')
        df = st.session_state.df

        #df=pd.read_csv('./data/data.csv')
        df_exp=df.copy()

        ##FIXBUG
        ##st.write(st.session_state)

        if st.session_state.get('add_new_workspace', False):
            manual_select = 1
        else:
            manual_select = 0
        
        with st.sidebar:
            selected = option_menu("Workspace", ["Workspace Explorer", 'Add New Workspace', 'Edit Workspace'], 
            icons=['folder', 'folder-plus', 'pencil'], menu_icon="inbox", manual_select= manual_select)

        if selected == "Workspace Explorer":
            st.header(":open_file_folder: Workspace Explorer", divider='gray')
            with st.container():
                col1, col2, col3 = st.columns([5,7,12])
                with col1:
                    st.button(":heavy_plus_sign: Add new workspace", type="primary", key="add_new_workspace")
                with col2:
                    change = st.button(":star2: Select a process to execute PM", key="select_event_log_to_process", on_click=change_page)
                    if change and 'converted_event_log' in st.session_state:
                        switch_page('process_discovery')
                with col3:
                    st.empty()
            with st.container():    
                #style
                html_divider = """<style>.divider {border-bottom: 1px solid black;margin-bottom: 0px;}</style><div class="divider"></div>"""

                st.markdown(html_divider, unsafe_allow_html=True)

                col0, col1, col2, col3, col4, col5, col6 = st.columns([1,3,4,2,2,2,3])
                with col0:
                    st.empty()
                with col1:
                    st.write("Name")
                with col2:
                    st.write("Description")
                with col3:
                    st.write("Create By")
                with col4:
                    st.write("Create At")
                with col5:
                    st.write("Status")
                with col6:
                    st.empty()

                st.markdown(html_divider, unsafe_allow_html=True)

            with st.container():
                for index, row in df.iterrows():
                    check, name, description, create_by, create_at, status, action = st.columns([1,3,4,2,2,2,3])
                    with check:
                        if row[8] != "Ready":
                            select = st.checkbox(label='',key=f"selected_event_log {index}", disabled=True)
                        else:
                            select = st.checkbox(label='',key=f"selected_event_log {index}")
                    with name:
                        st.write(f"{row[0]}")
                    with description:
                        st.write(f"{row[1]}")
                    with create_by:
                        st.write(f"{row[2]}")
                    with create_at:
                        datetime_create_at = pd.to_datetime(row[3])
                        formatted_date = datetime_create_at.strftime("%Y/%m/%d")
                        st.write(formatted_date)
                    with status:
                        if row[8] != "Ready":
                            st.markdown(":large_orange_circle: :orange[Not ready]")
                        else:
                            st.markdown(":large_green_circle: :green[Ready]")
                    with action:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            import_event = st.button(":heavy_plus_sign:", key=f"add event log {index}", on_click=form_callback)
                            if import_event:
                                switch_page('import_event_log')
                        with col2:
                            st.button(":pencil2:", key=f"edit {index}")
                        with col3:
                            st.button(":heavy_minus_sign:", key=f"delete {index}")
                              
        elif selected == "Add New Workspace":
            st.header(":inbox_tray: Add New Workspace", divider='gray')
            add_new_workspace(df,df_exp)
        
    