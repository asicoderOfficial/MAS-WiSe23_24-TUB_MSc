import os
from typing import Union

import pandas as pd
import plotly.graph_objects as go

from src.utils.files import search_files_recursively


def general_styling(fig:go.Figure) -> go.Figure:
    # set x axis 45 degree
    fig.update_layout(xaxis_tickangle=-45)
    # make it bigger
    fig.update_layout(
        autosize=False,
        width=1000,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
    )

    return fig  


def number_of_messages_by_type(csvs_path: str, store_path:str) -> Union[int, pd.DataFrame]:
    csv_files = [f for f in search_files_recursively(csvs_path, '.csv')  if 'messages' in f]
    dfs = [pd.read_csv(csv_file) for csv_file in csv_files]

    n_messages = {csv_files[i].split('/')[-2].split('-')[0]: df.shape[0] for i, df in enumerate(dfs)}

    n_intermediate_pickup_requests = {csv_files[i].split('/')[-2].split('-')[0]: df[(df['Sender ID'].str.contains('ChainAgent')) & ((df['Destination ID'].str.contains('broker') | (df['Destination ID'].str.contains('recruiter'))))]['Type'].value_counts().get('delivery_notify', 0) for i, df in enumerate(dfs)}
    n_ending_pickup_requests = {csv_files[i].split('/')[-2].split('-')[0]: df[(df['Sender ID'].str.contains('broker')) & ((df['Destination ID'].str.contains('broker') | (df['Destination ID'].str.contains('recruiter'))))]['Type'].value_counts().get('pickup_request', 0) for i, df in enumerate(dfs)}

    n_ending_acceptances = {csv_files[i].split('/')[-2].split('-')[0]: df['Type'].value_counts().get('delivery_accepted', 0) for i, df in enumerate(dfs)}

    messages_data = [n_messages, n_intermediate_pickup_requests, n_ending_pickup_requests, n_ending_acceptances]
    messages_df = pd.DataFrame(messages_data).T.rename(columns={'index':'experiment', 0:'n_messages', 1:'n_intermediate_pickup_requests', 2:'n_ending_pickup_requests', 3:'n_ending_acceptances'})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=messages_df.index, y=messages_df['n_intermediate_pickup_requests'], mode='lines+markers', name='Intermediate pickup requests'))
    fig.add_trace(go.Scatter(x=messages_df.index, y=messages_df['n_ending_pickup_requests'], mode='lines+markers', name='Ending pickup requests'))
    fig.add_trace(go.Scatter(x=messages_df.index, y=messages_df['n_ending_acceptances'], mode='lines+markers', name='Ending acceptances'))

    fig.update_layout(title_text='Number of messages per experiment and situation')
    fig.update_xaxes(title_text="Experiment")
    fig.update_yaxes(title_text="Number of messages by type")
    fig.update_layout(legend_title_text='Message type')
    fig = general_styling(fig)
    fig.write_image(store_path)


def total_number_of_messages(csvs_path: str, store_path:str) -> Union[int, pd.DataFrame]:
    csv_files = [f for f in search_files_recursively(csvs_path, '.csv')  if 'messages' in f]
    dfs = [pd.read_csv(csv_file) for csv_file in csv_files]

    n_messages = {csv_files[i].split('/')[-2].split('-')[0]: df.shape[0] for i, df in enumerate(dfs)}

    messages_data = [n_messages]
    messages_df = pd.DataFrame(messages_data).T.rename(columns={'index':'experiment', 0:'n_messages'})

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=messages_df.index, y=messages_df['n_messages'], mode='lines+markers', name='Total messages'))

    fig.update_layout(title_text='Total number of messages per experiment')
    fig.update_xaxes(title_text="Experiment")
    fig.update_yaxes(title_text="Number of messages")
    fig = general_styling(fig)
    fig.write_image(store_path)

total_number_of_messages('logs/', 'totalnumber_of_messages.png')