import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def plot_columns_overview(df):
    # Convert 'HighPercentageFlag' to numeric for plotting
    df['HighPercentageFlag'] = df['HighPercentageFlag'].astype(int)

    # Filter values with percentage more than 80%
    #filtered_df = df[df[['NaN_Percentage']] > 80]
    filtered_df = df[df[['NaN_Percentage']] > 0]

    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = np.where(filtered_df['NaN_Percentage'] > 0, 'blue', '0')
    colors = np.where(filtered_df['NaN_Percentage'] > 80, 'red', 'blue')

    filtered_df.plot(kind='bar', y=['NaN_Percentage'], color=colors, ax=ax)

    # Adding labels and title
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Column')
    ax.set_title('Overview of Columns with High Percentage Flag')

    # Highlighting columns with True value in HighPercentageFlag
    #for i, value in enumerate(filtered_df['NaN_Percentage']):
    #    if value > 80 and not pd.isna(filtered_df.iloc[i]['NaN_Percentage']):
    #        ax.text(i, filtered_df.iloc[i]['NaN_Percentage'] + 2, 'High', color='red', ha='center')

    for column, row in filtered_df.iterrows():
      value = row['NaN_Percentage']
      if not pd.isna(value):
        if value > 80:
            label = 'High'
        else:
            label = column
        ax.text(filtered_df.index.get_loc(column), value + 2, label, color='red', ha='center')

    # Add a threshold line
    ax.axhline(y=80, color='red', linestyle='--', label=f'Threshold 80%')

    st.pyplot(fig)

def show_zero_nan_percentage(df, threshold=80):
    # Calculate the percentage of zero values for each column
    zero_percentage = (df == 0).mean() * 100

    # Calculate the percentage of NaN values for each column
    nan_percentage = (df.isna().mean()) * 100

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        'Zero_Percentage': zero_percentage,
        'NaN_Percentage': nan_percentage
    })
    summary_df['NaN_Percentage'] = np.where((summary_df['NaN_Percentage'] == 0), summary_df['Zero_Percentage'], summary_df['NaN_Percentage'])
    #Drop column
    summary_df = summary_df.drop(['Zero_Percentage'], axis=1)

    # Add a flag column indicating whether any percentage is greater than the threshold
    summary_df['HighPercentageFlag'] = (summary_df['NaN_Percentage'] > threshold)

    return summary_df

def drop_columns(df, threshold=0.8):

    # Drop columns with a percentage of NaN values greater than the threshold
    df = df.dropna(axis=1, thresh=int(threshold * len(df)))

    # Drop columns with a percentage of zero values greater than the threshold
    df = df.loc[:, (df == 0).mean() < threshold]

    return df