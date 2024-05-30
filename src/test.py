import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def analyze_scrap_code_correlations(df):
    # Replace NaN and infinite values
    df = df.replace([np.inf, -np.inf], np.nan).fillna(0)

    # Ensure the columns are properly formatted
    df['SO #'] = df['SO #'].astype(int)
    df['Code ID'] = df['Code ID'].astype(int)
    df['Scrap Qty'] = df['Scrap Qty'].astype(float)

    # Pivot the data
    pivot_df = df.pivot_table(index='SO #', columns='Code ID', values='Scrap Qty', fill_value=0)

    # Calculate the correlation matrix
    corr_matrix = pivot_df.corr()

    # Visualize the correlation matrix
    plt.figure(figsize=(14, 12))  # Increase figure size
    sns.heatmap(corr_matrix, annot=True, cmap='cividis', fmt='.2f', linewidths=.5, annot_kws={"size": 10})
    plt.title('Correlation Matrix of Scrap Codes', fontsize=18, fontweight='bold')
    plt.xticks(fontsize=12, rotation=45, ha='right')  # Adjust x-axis labels
    plt.yticks(fontsize=12)  # Adjust y-axis labels
    plt.tight_layout()
    plt.show()

def check_data_distribution(df):
    # Count occurrences of each scrap code
    scrap_code_counts = df['Code ID'].value_counts()
    
    plt.figure(figsize=(12, 6))
    scrap_code_counts.plot(kind='bar')
    plt.title('Distribution of Scrap Codes')
    plt.xlabel('Scrap Code')
    plt.ylabel('Count')
    plt.show()

def check_pivot_table(df):
    # Pivot the data
    pivot_df = df.pivot_table(index='SO #', columns='Code ID', values='Scrap Qty', fill_value=0)
    print(pivot_df.head())
    return pivot_df