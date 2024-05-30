import os 
import numpy as np
import pandas as pd 
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt 

def load_data(data):
    df = pd.DataFrame()

    if isinstance(data, list):
        for i in range(len(data)):
            file_name = f"{data[i]}.csv"
            file_dir = os.path.join(os.getcwd(), 'data', file_name)
            new_df = pd.read_csv(file_dir)
            df = pd.concat([df, new_df], ignore_index = True)
    elif isinstance(data, str):
        file_name = f"{data}.csv"
        file_dir = os.path.join(os.getcwd(), 'data', file_name)
        df = pd.read_csv(file_dir)
        
    return df

def load_scrapcodes(df, update = False):
    df = df.dropna(subset=['Code ID', 'Code Description'])
    data = df.drop_duplicates(subset=['Code ID']).set_index('Code ID')['Code Description'].to_dict()
    data = {int(k): v for k, v in data.items()}

    new_df = pd.DataFrame.from_dict(data, orient='index', columns=['Code Description'])
    new_df.reset_index(inplace=True)
    new_df.rename(columns={'index': 'Code ID'}, inplace=True)
    new_df = new_df.sort_values(by='Code ID').reset_index(drop=True)

    if update:
        file_name = 'ScrapCodesInfo.csv'
        save_path = os.path.join(os.getcwd(), 'resources', file_name)
        new_df.to_csv(save_path, index = False)

    return new_df

def search_shoporder(df, shopordernum):
    new_df = df.loc[df['SO #'] == shopordernum].reset_index(drop=True)
    
    int_cols = ['SO #', 'SO P/N', 'Scrap P/N', 'Code ID']
    new_df[int_cols] = new_df[int_cols].astype('int')

    return new_df

def search_scrapcode(df, scrapcodeid):
    new_df = df[(df['SO P/N'] == df['Scrap P/N']) & (df['Code ID'] == scrapcodeid)].reset_index(drop=True)

    int_cols = ['SO #', 'SO P/N', 'Scrap P/N', 'Code ID']
    new_df[int_cols] = new_df[int_cols].astype('int')

    new_df = new_df.sort_values(by = 'SO #')

    return new_df

def trace_daterange(df, start, end):
    df['Date'] = pd.to_datetime(df['Date'], format = '%m/%d/%Y')

    start_date = datetime.strptime(start, '%m/%d/%Y')
    end_date = datetime.strptime(end, '%m/%d/%Y')

    new_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    return new_df

def trace_recent(df, recent):
    new_df = df[-int(recent):]
    
    return new_df


def graph_history(df):
    pass

def graph_imr(df):
    pass


    

    # if graph:
    #     x = np.array(new_df['SO #'], dtype='str')
    #     y = np.array(new_df['Scrap Rate'].str.rstrip('%').astype('float'))

    #     plt.scatter(x, y, color = 'blue')
    #     plt.plot(x, y, linestyle = '-', color = 'blue', alpha = 0.7)

    #     plt.title(f"Scrap Code: {new_df.iloc[0]['Code Description']}", fontweight='bold')
    #     plt.xlabel('Shop Orders')
    #     plt.ylabel('Scrap Rate (%)')

    #     plt.xticks(rotation = 35, ha = 'right')
    #     plt.tight_layout()
        
    #     plt.show()