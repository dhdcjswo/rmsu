

#%%
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from urllib import parse
import pandas as pd
# %%
url = 'https://comic.naver.com/webtoon/genre.nhn?genre=' + 'sports'
response = requests.get(url)
dom = BeautifulSoup(response.content, "html.parser")
keywords = dom.select('.list_area > .img_list > li' )
dom.select("dl > dt > a")[0].get('href')[-6:] # uniq_id
keywords[0].select_one("dl > dt > a").text
keywords[0].select_one("dl > dd > a").text
keywords[0].select_one("dl > dd > .rating_type > strong").text
#%%
keywords = dom.select('.list_area > .img_list > li' )
#%%
def crawler(genre):

    dic = {}
    dic['uniq_id'] = []
    dic['title'] = []
    dic['author'] = []
    dic['rating'] = []

    url = 'https://comic.naver.com/webtoon/genre.nhn?genre=' + genre
    response = requests.get(url)
    dom = BeautifulSoup(response.content, "html.parser")
    keywords = dom.select('.list_area > .img_list > li' )
    
    for keyword in keywords:
        dic['title'].append(keyword.select_one("dl > dt > a").text)
        dic['author'].append(keyword.select_one("dl > dd > a").text)
        dic['rating'].append(keyword.select_one("dl > dd > .rating_type > strong").text)
        

    uniq_id = dom.select('li > .thumb > a')
    for i in range(len(uniq_id)):
        dic['uniq_id'].append(uniq_id[i].get('href')[-6:])


    df = pd.DataFrame(dic)
    df[genre] = genre
    return df
#%%
genres = ["episode","omnibus","story","daily","comic",
    "fantasy","action","drama","pure","sensibility","thrill","historical","sports"]

#%%
df = crawler('episode')
# %%
for i in genres[1:]:
    temp = crawler(i)
    df = pd.merge(df, temp, how='outer')


# %%
df = df.fillna("")

# %%
ls = []
for i in range(len(df)):
    ls.append('/'.join(list(filter(lambda x : x != "" , df[genres].loc[i]))))

#%%
df['genres'] = ls
df.drop(columns= genres, axis=1, inplace=True)
# %%



# %% 다음웹툰
driver = webdriver.Chrome("C:/Users/dhdcj/chromedriver.exe")

#%%
genre = "에피소드"
url = "http://webtoon.daum.net/search/total?q=%23" + parse.quote_plus(genre) + "#page=1"
driver.get(url)
html = driver.page_source
dom = BeautifulSoup(html)
#%% 만화제목
keyword = dom.select('.desc_result')
keyword[0].select_one('.tit_wt').text.replace('\n','').replace('\t','')

# %% 만화 세부장르
keyword[0].select_one('dd').text

# %% 작가
keyword[0].select_one('dl > dd > a').text


# %%
def crawler_daum(genre):

    dic = {}
    dic['title'] = []
    dic['author'] = []
    dic['genre'] = []
    

    genre = genre
    url = "http://webtoon.daum.net/search/total?q=%23" + parse.quote_plus(genre) + "#page=1"
    driver.get(url)
    html = driver.page_source
    dom = BeautifulSoup(html)
    
    keywords = dom.select('.desc_result')
    for keyword in keywords:
        dic['title'].append(keyword.select_one('.tit_wt').text.replace('\n','').replace('\t',''))
        dic['author'].append(keyword.select_one('dl > dd > a').text)
        dic['genre'].append(keyword.select_one('dd').text)
        

    df = pd.DataFrame(dic)
    return df


# %%
crawler_daum('공포')


# %%
