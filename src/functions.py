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

def searchfilter_daterange(df, start, end):
    try:
        # Ensure that the date column is properly formatted
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
    except Exception as e:
        print(f"Error converting dates: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there is an error

    # Convert start and end dates to datetime
    start_date = pd.to_datetime(start, format='%m/%d/%Y')
    end_date = pd.to_datetime(end, format='%m/%d/%Y')

    # Filter the dataframe based on the date range
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    new_df = df.loc[mask]

    return new_df

# def searchfilter_daterange(df, start, end):
#     df['Date'] = pd.to_datetime(df['Date'], '%m/%d/%Y')

#     start_date = datetime.strptime(start, '%m/%d/%Y')
#     end_date = datetime.strptime(end, '%m/%d/%Y')

#     new_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

#     return new_df

def searchfilter_recentlots(df, shopordernum):
    df = df.dropna()
    new_df = df[-int(shopordernum):]
    
    return new_df
    
def graph_imr(df, measurement_col, x_col):
    df[measurement_col] = df[measurement_col].str.rstrip('%').astype('float')
    df['Individual'] = df[measurement_col]
    df['Moving Range'] = df['Individual'].diff().abs()
    X_bar = df['Individual'].mean()
    MR_bar = df['Moving Range'].mean()
    UCL_I = X_bar + 2.66 * MR_bar
    LCL_I = X_bar - 2.66 * MR_bar
    UCL_MR = 3.267 * MR_bar

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    ax1.plot(df[x_col].astype(str), df['Individual'], marker='o', linestyle='-', color='blue')
    ax1.axhline(X_bar, color='green', linestyle='--', linewidth=1)
    ax1.axhline(UCL_I, color='pink', linestyle='--', linewidth=1)
    ax1.axhline(LCL_I, color='pink', linestyle='--', linewidth=1)
    ax1.set_title('Individuals (I) Chart', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Scrap Rate (%)', fontsize=12, fontweight='bold')
    
    ax2.plot(df[x_col].astype(str), df['Moving Range'], marker='o', linestyle='-', color='purple')
    ax2.axhline(MR_bar, color='orange', linestyle='--', linewidth=1)
    ax2.axhline(UCL_MR, color='pink', linestyle='--', linewidth=1)
    ax2.set_title('Moving Range (MR) Chart', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Shop Order', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Moving Range', fontsize=12, fontweight='bold')

    ax2.set_xticks(range(len(df[x_col])))
    ax2.set_xticklabels(df[x_col].astype(str), rotation=45, ha='right')

    overall_title = f"IMR Control Chart - {df.iloc[0]['Code Description']}"
    fig.suptitle(overall_title, fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# def graph_scatter(df):
    # x = np.array(df['SO #'], dtype='str')
    # y = np.array(df['Scrap Rate'].str.rstrip('%').astype('float'))

    # plt.scatter(x, y, color = 'blue')
    # plt.plot(x, y, linestyle = '-', color = 'blue', alpha = 0.7)

    # plt.title(f"Scrap Code: {df.iloc[0]['Code Description']}", fontweight='bold')
    # plt.xlabel('Shop Orders', fontweight='bold')
    # plt.ylabel('Scrap Rate (%)', fontweight='bold')

    # plt.xticks(rotation = 35, ha = 'right')
    # plt.tight_layout()
    
    # plt.show()