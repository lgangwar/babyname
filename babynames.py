from pandas.io import html
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
import string

def getSubUrlList(page_url:str):
    # creating requests object
    html = requests.get(page_url).content
    
    # creating soup object
    data = soup(html, 'html.parser')
    sub_list = []
    my_find = data.find("div", {"class": "clearfix tc full-width"})
    if my_find:
        for i in my_find.findAll('a'):
            sub_page = i.get('href', None)
            print(sub_page)
            if  sub_page != None and ((page_url + '/' + sub_page) not in sub_list):
                sub_list += [page_url + '/' + sub_page]

    return sub_list
    
def get_char_list():
    return list(string.ascii_lowercase)

def get_all_urls():
    url = 'https://www.prokerala.com/kids/baby-names/hindu/boy/'
    char_list = get_char_list()
    res_url_list = []
    for mychar in char_list:
        first_url_on_char = url + mychar
        res_url_list += [first_url_on_char]
        res_url_list += getSubUrlList(first_url_on_char)
    return res_url_list


url_list = get_all_urls()
print(url_list)

# page_urls = ['./soup.html']
final_df = []
for url in url_list:
    try:
        dfs = pd.read_html(url)
    except:
        print('kuch gadbd hai bhai')
        continue
        
    print(type(dfs))
    data_frame_length = len(dfs)

    df = pd.concat(dfs)
    #df = dfs[0]
    col_list = list(df.columns.values)
    df = df.drop([col_list[1], col_list[2]], axis=1)
    df = df.rename({'Unnamed: 4':'likes'},axis=1)
    dfindex = df[df['Name'] == 'ALSO READ: Popular Hindu Boy Names'].index
    df.drop(dfindex, inplace=True)
    
    dfindex = df[df['Name'] == 'ALSO READ: Hindu Boy Names'].index
    df.drop(dfindex, inplace=True)
    
    final_df += [df]

#baby_name_df = pd.concat(final_df)
#print(baby_name_df.column.dtype)
#print(baby_name_df.sort_values('likes'))
#baby_name_pd = pd.concat(final_df)
#print(type(baby_name_pd))
#baby_name_pd['likes'] = pd.to_numeric(baby_name_pd['likes'])
#final_names = baby_name_pd.sort_values(['likes'], ascending=[False])
#print(type(final_names))
#final_names.to_csv('babyname.csv', index = False)

baby_name_pd = pd.concat(final_df)
print(type(baby_name_pd))
baby_name_pd['likes'] = pd.to_numeric(baby_name_pd['likes'])
final_names = baby_name_pd.sort_values(['likes'], ascending=[False])
print(type(final_names))
final_names.to_csv('babyname.csv', index = False)