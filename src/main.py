import os 
import pandas as pd 
from functions import *

os.system('cls')

file_list = ['ScrapLog_2019', 'ScrapLog_2020', 'ScrapLog_2021', 'ScrapLog_2022', 'ScrapLog_2023', 'ScrapLog_2024']

df = load_data(file_list)
# load_scrapcodes(df)


# print(load_scrapcodes(df))


shoporder = 1507458
scrapcode_id = 58
start_date = '1/1/2023'
end_date = '05/29/2024'
recent_num = 30

a = search_shoporder(df, shoporder)
# print(a)

b = search_scrapcode(df, scrapcode_id)
# print(b)

c = trace_daterange(b, start_date, end_date)
# print(c)

d = trace_recent(df, recent_num)
# print(d)
print(len(d))