import os 
import pandas as pd 
from functions import *
from test import *

# os.system('cls')
os.system('clear')

# file_list = ['ScrapLog_2019', 'ScrapLog_2020', 'ScrapLog_2021', 'ScrapLog_2022', 'ScrapLog_2023', 'ScrapLog_2024']
# file_list = ['ScrapLog_2022', 'ScrapLog_2023', 'ScrapLog_2024']
file_list = 'ScrapLog_2024'

shoporder = 1522860
scrapcode_id = 322
start_date = '1/1/2024'
end_date = '05/29/2024'
recentlots_num = 50


df = load_data(file_list)


# a = search_shoporder(df, shoporder)
# b = search_scrapcode(df, scrapcode_id)

# c = searchfilter_recentlots(df, recentlots_num)
d = searchfilter_daterange(df, start_date, end_date)
print(d)


# print(d)
# graph_imr(d, 'Scrap Rate', 'SO #')


# swag_1 = check_data_distribution(d)
# swag_2 = pivot_df = check_pivot_table(d)
swag_ult = analyze_scrap_code_correlations(d)