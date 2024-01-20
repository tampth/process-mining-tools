import pandas as pd
import plotly.express as px
import streamlit as st

def visualize_activity_counts(dataframe, case_count, activity_count, activity_column):
    # Group the data by the 'activity' column and count the occurrences
    activity_counts = dataframe[f"{activity_column}"].value_counts().reset_index(name='activity_count')

    # Calculate the percentage of each activity
    activity_counts['percentage'] = (activity_counts['activity_count'] / activity_counts['activity_count'].sum()) * 100

    # Round the percentages to 2 digits
    activity_counts['percentage'] = activity_counts['percentage'].round(2)

    # Create a bar chart using Plotly Express
    fig = px.bar(activity_counts, x=f'{activity_column}', y='activity_count',
                 labels={'index': 'Activity', 'activity_count': 'Count'},
                 text=activity_counts['percentage'].map('{:.2f}%'.format),  # Format text as percentage
                 height=630,  # Increase the height
                 category_orders={"index": activity_counts[f'{activity_column}'].tolist()}  # Ensure the correct order
                 )

    fig.update_layout(title_text=f"Tổng cộng <span style='color:red;'>{case_count}</span> trường hợp và <span style='color:red;'>{activity_count}</span> hoạt động được phát hiện")

    # Adjust text position to be outside the bars
    fig.update_traces(textposition='outside')

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
    # return activity_counts

def plot_horizontal_bar_chart_activity(df, activity_column):
    # Count occurrences of each activity
    activity_counts = df[f'{activity_column}'].value_counts()

    # Calculate the percentage of each activity
    activity_percentages = (activity_counts / len(df)) * 100

    # Create a new DataFrame to store the results
    result_df = pd.DataFrame({'Activity': activity_counts.index, 'Count': activity_counts.values, 'Percentage': activity_percentages.values})

    # Sort the DataFrame based on the 'Count' column
    result_df = result_df.sort_values(by='Count', ascending=True)

    fig = px.bar(result_df, y='Activity', x='Count', text='Percentage',
                 title='ACTIVITIES',
                 labels={'Count': 'Activity Count'},
                 orientation='h')

    # Add percentage text outside the bars
    fig.update_traces(texttemplate='%{text:.2f}%')

    # Set automargin to True for both x-axis and y-axis
    fig.update_layout(xaxis=dict(automargin=True, side='top', title=''),  # Remove x-axis label
                      yaxis=dict(automargin=True, title=''),  # Remove y-axis label
                      height=500)  # Set the fixed height

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

def plot_start_activities(df, timestamp_column, case_column, activity_column):
    # Convert 'timestamp' column to datetime format
    df[f'{timestamp_column}'] = pd.to_datetime(df[f'{timestamp_column}'])

    # Sort the DataFrame by 'case_id' and 'timestamp'
    df_sorted = df.sort_values(by=[f'{case_column}', f'{timestamp_column}'])

    # Find the starting activity for each case_id
    starting_activities = df_sorted.groupby(f'{case_column}').first().reset_index()[[f'{case_column}', f'{activity_column}']]

    # Calculate the count and percentage of each starting activity
    activity_counts = starting_activities[f'{activity_column}'].value_counts().reset_index()
    activity_counts.columns = [f'{activity_column}', 'count']
    activity_counts['percentage'] = activity_counts['count'] / activity_counts['count'].sum() * 100

    # Create a bar chart with annotations at the end of bars
    fig = px.bar(activity_counts, 
                 x='count', 
                 y=f'{activity_column}', 
                 text='percentage',
                 orientation='h',
                 labels={'activity': 'Starting Activity', 'count': 'Count', 'percentage': 'Percentage (%)'},
                 title='START ACTIVITIES')

    # Add percentage text outside the bars
    fig.update_traces(texttemplate='%{text:.2f}%')

    # Set automargin to True for both x-axis and y-axis
    fig.update_layout(xaxis=dict(automargin=True, side='top', title=''),  # Remove x-axis label
                      yaxis=dict(automargin=True, title='')
                      ,height=500)  # Remove y-axis label

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)


def plot_end_activities(df, timestamp_column, case_column, activity_column):
    # Convert 'timestamp' column to datetime format
    df[f'{timestamp_column}'] = pd.to_datetime(df[f'{timestamp_column}'])

    # Sort the DataFrame by 'case_id' and 'timestamp'
    df_sorted = df.sort_values(by=[f'{case_column}', f'{timestamp_column}'])

    # Find the ending activity for each case_id
    ending_activities = df_sorted.groupby(f'{case_column}').last().reset_index()[[f'{case_column}', f'{activity_column}']]

    # Calculate the count and percentage of each ending activity
    activity_counts = ending_activities[f'{activity_column}'].value_counts().reset_index()
    activity_counts.columns = [f'{activity_column}', 'count']
    activity_counts['percentage'] = activity_counts['count'] / activity_counts['count'].sum() * 100

    # Sort activities from max to min based on counts
    activity_counts = activity_counts.sort_values(by='count', ascending=True)

    # Create a bar chart with annotations at the end of bars
    fig = px.bar(activity_counts, 
                 x='count', 
                 y=f'{activity_column}', 
                 text='percentage',
                 orientation='h',
                 labels={'activity': 'Ending Activity', 'count': 'Count', 'percentage': 'Percentage (%)'},
                 title='END ACTIVITIES')

    # Add percentage text outside the bars
    fig.update_traces(texttemplate='%{text:.2f}%')

    # Set automargin to True for both x-axis and y-axis
    fig.update_layout(xaxis=dict(automargin=True, side='top', title=''),  # Remove x-axis label
                      yaxis=dict(automargin=True, title='')
                      ,height=500)  # Remove y-axis label
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

def plot_activity_distribution(df, timestamp, case_id, activity):
    # Assuming 'timestamp' is a column in the DataFrame
    df[f'{timestamp}'] = pd.to_datetime(df[f'{timestamp}'])

    # Count the number of activities for each case_id
    activity_count = df.groupby(f'{case_id}')[f'{activity}'].count().reset_index()

    # Group case_ids based on the number of activities and count the number of case_ids in each group
    grouped_cases = activity_count.groupby(f'{activity}')[f'{case_id}'].count().reset_index()

    # Rename the columns for clarity
    grouped_cases.columns = [f'{activity}', 'case_id_count']

    # Plotly Bar Chart
    fig = px.bar(grouped_cases, x=f'{activity}', y='case_id_count',
                 labels={'activity': 'Number of Event', 'case_id_count': 'Number of Case'},
                 title='EVENT PER CASE')
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

def plot_activity_boxplot(df, timestamp, case_id, activity):
    # Assuming 'timestamp' is a column in the DataFrame
    df[f'{timestamp}'] = pd.to_datetime(df[f'{timestamp}'])
    # Count the number of activities for each case_id
    activity_count = df.groupby(f'{case_id}')[f'{activity}'].count().reset_index()

    # Plotly Box Plot
    fig = px.box(activity_count, y=f'{activity}',
                 labels={'activity': 'Number of Event'},
                 title='BOXPLOT OF EVENT PER CASE',
                 points='all',  # Display all data points
                 custom_data=[f'{case_id}'])  # Include case_id in custom data for reference

    # Update hover information
    fig.update_traces(
        hovertemplate='<b>Number of Event</b>: %{y}<br><b>Case ID</b>: %{customdata[0]}'
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_case_count_over_time(df, time_start, time_end):
    # Convert the 'timestamp' column to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group by 'timestamp' and count the number of unique 'case_id'
    df_count = df.groupby('timestamp')['case_id'].nunique().reset_index(name='case_count')

    # Plot using Plotly
    fig = px.line(df_count, x='timestamp', y='case_count',
                  labels={'case_count': 'Number of Case IDs', 'timestamp': 'Timestamp'}, height=600)

    
    fig.update_layout(title_text=f"Thời gian diễn ra từ <span style='color:red;'>{time_start}</span> đến <span style='color:red;'>{time_end}</span>")
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)