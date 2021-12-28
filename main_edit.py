# 필요한 라이브러리 불러오기
from konlpy.tag import Okt

okt = Okt()

import pandas as pd
import warnings

warnings.filterwarnings(action='ignore')

from selenium import webdriver as wd
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
import re

# 드라이버 경로 정의해주기
driver = wd.Chrome(executable_path='/home/lifeofpy/Desktop/chromedriver')

# In[2]:


# 불용어 사전 불러오기
with open('/home/lifeofpy/PycharmProjects/pythonProject/AmazonProject/Comments-Crawler/Melon-Crawler/stop_words.txt', 'r') as file:
    stop_word = file.readline()
    stop_word = str(stop_word)

stop_word = stop_word.replace("\ufeff", '').replace("'", '').replace(",", '').replace('\n', '').replace("’",
                                                                                                        '').replace("‘",
                                                                                                                    '')
stop_words = stop_word.split()


# In[3]:


# 멜론 페이지 url 전처리해주기 >> url 로 만들기
def find_str_to_change(url):
    url = str(url)
    try:
        if 'cmtpgn' not in url:
            real_url = url + '#cmtpgn=&pageNo={}&sortType=0&srchType=2&srchWord='
            return real_url

        else:  # cmtpgn 이 있는 경우
            url = url.split('&')  # & 기준으로 나누기
            real_url = url[0] + '&pageNo={}&' + url[2] + '&' + url[3] + '&' + url[4]

            return real_url

    except:
        if 'cmtpgn' not in url:
            real_url = url + 'cmtpgn=&pageNo={}&sortType=0&srchType=2&srchWord='
            return real_url

        else:  # cmtpgn 이 있는 경우
            url = url.split('&')  # & 기준으로 나누기
            real_url = url[0] + '&pageNo={}&' + url[2] + '&' + url[3] + '&' + url[4]

            return real_url


# In[4]:


# 페이지 개수 가져오는 함수
# 페이지 개수를 가져오기 위해서는 댓글 개수가 필요하다.
# (하나의 페이지에 댓글 10개가 있기 때문에 댓글 개수 나누기 10 = 페이지 개수)

def find_page_num(url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('span', {'class': 'd_cmtpgn_srch_cnt'})[0]

    # 일단 추출된 태그를 문자열로 바꾸기
    pages = str(pages)

    # 정규식을 통해 태그에서 숫자(=댓글 개수)만 추출하기
    cmt_num = re.findall('\d+', pages)
    page_num = "".join(cmt_num)
    page_num = int(page_num)
    page_num = page_num // 10

    # 일단 추출된 태그를 문자열로 바꾸기
    pages = str(pages)

    # 정규식을 통해 태그에서 숫자(=댓글 개수)만 추출하기
    cmt_num = re.findall('\d+', pages)

    for i in cmt_num:
        page_num = int(i) // 10

    return page_num


# In[5]:


# 댓글을 크롤링해와 리스트로 저장하는 함수
def crawl_the_cmts(url):
    comments = []
    real_url = find_str_to_change(url)
    page_number = find_page_num(url)

    for i in range(0, page_number + 2):
        link = real_url.format(i)
        driver.get(link)
        driver.implicitly_wait(4)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        comment = soup.find_all('div', {'class': 'd_cmtpgn_cmt_full_contents'})

        for r in comment:
            comments.append(r.get_text().strip())

    return comments


# In[6]:


# 필요 없는 문자 전처리 후, melon_comments 에 반환하는 함수
def pre_process_cmts(url):
    cmts = crawl_the_cmts(url)
    melon_comments = cmts

    # 댓글이 모인 comments 리스트에서 필요없는 문자 처리하기
    for j in range(len(melon_comments)):
        if '내용' in melon_comments[j]:
            melon_comments[j] = melon_comments[j].replace('내용', '').replace(' \t', '').replace('\t', '')

    return melon_comments


# In[7]:


# 댓글 리스트에서 감정단어(형용사)만 추출하는 함수
def extract_emo_words(url):
    melon_comments = pre_process_cmts(url)

    okts = []
    adj = []
    real_adj = []

    for i in range(len(melon_comments)):
        okts.append(okt.pos(melon_comments[i]))

    for i in range(len(okts)):
        for j in range(len(okts[i])):
            if okts[i][j][1] == 'Adjective' and len(okts[i][j][0]) > 1:
                adj.append(okts[i][j][0])

    for w in adj:
        if w not in stop_words:
            real_adj.append(w)

    real_adj = str(set(real_adj)).replace("'", '')

    return real_adj


def extract_singer(url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    singer = soup.find(attrs={'class':'artist_name'}).find('span').text
    singer = str(singer)
    singer = singer.split()
    print(singer)
    for i in range(len(singer)):
        if "'" in singer[i]:
            real_singer = str(singer[0:-1]).replace('[', '').replace(']', '').replace(',', '').replace("'", '')
        elif "(" in singer[i]:
            real_singer = singer[i-1]
            break
        else:
            # 리스트에 있는 원소를 공백 없이 하나로 합쳐야함
            real_singer = "".join(singer)

    return real_singer



def extract_title(url):
    title_lst = []
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('div', {'class': 'song_name'})
    for r in title:
        title_lst.append(r.get_text().strip())

    title_lst[0] = title_lst[0].replace('곡명', '').replace('\n', '').replace('\t', '')
    real_title = title_lst[0]
    print(real_title)
    return real_title



def make_complete_dataframe(data_df):
    for i in range(len(data_df)):
        link = str(data_df.iloc[i, 1])
        driver.get(link)
        link_with_alert = Alert(driver)
        driver.implicitly_wait(0.5)
        try:
            if len(crawl_the_cmts(link)) == 0:
                pass
            else:
                if len(link_with_alert.text) != 0:
                    link_with_alert.accept()
                    driver.quit()
                else:
                    data_df.iloc[i, 2] = extract_singer(data_df.iloc[i, 1])
                    data_df.iloc[i, 3] = extract_title(data_df.iloc[i, 1])
                    data_df.iloc[i, 4] = extract_emo_words(data_df.iloc[i, 1])
                    pass
            if i % 100 == 0:
                print(f'crawling has processed... {i} musics.')
        except:
            pass
    return data_df


dataset = pd.read_excel('./dataset.xlsx', engine='openpyxl')
make_complete_dataframe(dataset).to_excel('new_dataframe.xlsx')
