#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging.handlers
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool

from crawlerBot_pack_SCI_2019.crawlerbots import db_mysql_connection_SCI
global returnValue_kks_CSVData
global returnValue_kks_singleData
global hereWork

hereWork = 'Instagram'

currentTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

# logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger(hereWork+'_logging')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# fileHandler 와 StreamHandler 를 생성
file_max_bytes = 10*1024*1024   # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler('C:/python_project/log/' + hereWork + '_crawlerbot_logging_' + currentTime, maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler 에 formatter 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

# Handler 를 logging 에 추가
logger.addHandler(fileHandler)


def feed(user):
    print('feed 시작 ', '-'*50)
    # 크롤링할 주소
    url = 'https://www.instagram.com/'+user+'/'

    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    driver.implicitly_wait(4)

    print("Searching " + url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 게시물 수
    content_cnt = soup.select("li:nth-of-type(1) > a > span")[0].text.replace(',', '')
    # 팔로워 수
    follower_cnt = soup.select("li:nth-of-type(2) > a > span")[0]['title'].replace(',', '')
    # 팔로우 수
    follows_cnt = soup.select("li:nth-of-type(3) > a > span")[0].text.replace(',', '')
    # # 이미지
    # image = soup.select('div > div:nth-of-type(1) > div:nth-of-type(1) > a > div > div.KL4Bh > img')[0]['src']
    try:
        # 이름
        name = soup.select("div.-vDIg > h1")[0].text
    except Exception as e:
        name = ''
        print('이름 없음 :', e)

    try:
        # 소개
        intro = soup.select("div.-vDIg > span")[0].text
    except Exception as e:
        intro = ''
        print('소개 없음 :', e)

    try:
        # 홈페이지
        homepage = soup.select("div.-vDIg > a")[0].text
    except Exception as e:
        homepage = ''
        print('홈페이지 없음 :', e)

    print("닉네임 : " + user)
    print("게시물 수 : " + content_cnt)
    print("팔로워 : " + follower_cnt)
    print("팔로우 : " + follows_cnt)
    print("이름 : " + name)
    print("소개 : " + intro)
    print("홈페이지 : " + homepage)
    # print("이미지 : " + image)
    # image = driver.find_element_by_css_selector('div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div.KL4Bh > img').get_attribute('src')
    # tag_cnt = driver.find_element_by_css_selector('main > header > div.f7QXd.SM9CE > div > span > span').text

    # 스크롤내리는 횟수
    scroll_count = 2
    # 중복 href 카운트
    same_count = 0
    # 게시물마다 href 를 담을 리스트
    href = []

    # 스크롤 내릴 때마다 페이지 소스를 가져와서 href 속성만 가져오기
    for i in range(0, scroll_count):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        href_html = soup.select('div > div > div.v1Nh3 > a')
        for href_list in href_html:
            # href 리스트 안에 hrefLIST['href'] 가 들어 있으면 중복
            if href_list['href'] in href:
                # print(str(href_list['href']) + '중복')
                same_count += 1
            # href 리스트 안에 hrefLIST['href'] 가 없으면 넣음
            else:
                # print(href_list['href'])
                href.append(href_list['href'])
        time.sleep(1)
        print("Scrolling... "+str(i+1)+"/"+str(scroll_count) + ", 현재: " + str(len(href)) + ", 중복: " + str(same_count))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(str(len(href)) + "개의 결과를 찾았습니다.")

    href_slide = list_slide(href, 8)
    driver.close()

    return href_slide


# 리스트 나누기
def list_slide(href, n):
    for i in range(0, len(href), n):
        yield href[i:i + n]
# 왜냐하면 pool.map() 메소드에는 실행시킬 함수와 리스트(반복가능객체)를 넣는다.
# 그래서 리스트의 값으로 함수를 여러 프로세스로 나눠서 실행하는데 i


def info(href):
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(chrome_options=options)

    # 게시물 마다 DB에 insert 해줘야 하기때문에 for 문으로 돌림
    for i in href:
        # 크롤링할 주소
        user_url = "https://www.instagram.com" + i
        driver.get(user_url)
        driver.implicitly_wait(2)

        source2 = driver.page_source
        soup = BeautifulSoup(source2, 'html.parser')

        # # 닉네임
        # nickname = driver.find_element_by_css_selector('article > header > div.o-MQd > div.PQo_0 > div.e1e1d > h2 > a').text
        try:
            # 본문
            content = soup.select('div.KlCQn.EtaWk > ul > li:nth-of-type(1) > div > div > div > span')[0].text
        except Exception as e:
            content = ''
            print('본문 없음 :', e)
        try:
            # 본문태그
            tag = soup.select('div.KlCQn.EtaWk > ul > li > div > div > div > span > a')
        except Exception as e:
            tag = ''
            print('태그 없음 :', e)
        try:
            # 좋아요 or 조회수
            like_cnt = soup.select('section.EDfFK.ygqzn > div span')[0].text
        except Exception as e:
            like_cnt = '0'
            print('좋아요 없음 :', e)
        try:
            # 좋아요, 조회수 체크
            like_check = soup.select('section.EDfFK.ygqzn > div ')[0].text
        except Exception as e:
            like_check = ''
            print('체크 에러 :', e)

        # @태그 pass
        tag_list = ''
        for j in tag:
            if '#' in j.text:
                tag_list += j.text
            elif '@' in j.text:
                pass
            else:
                pass

        # url_pattern = "(/p/)([0-9a-zA-Z|_|-]*)(/\?tagged=)([0-9a-zA-Z가-힣ㄱ-ㅎ]*)"
        # main_re = re.compile(url_pattern)
        # main_tag = main_re.findall(i)

        # 사진인지 동영상인지 체크
        if '좋아' in like_check:
            like = like_cnt.replace(',', '')
            view = '0'
        elif '조회' in like_check:
            like = '0'
            view = like_cnt.replace(',', '').replace('조회 ', '').replace('수', '')
        else:
            like = '0'
            view = '0'

        # print('main_tag :' + str(main_tag))
        print('본문 : ' + content)
        print('태그 : ' + str(tag_list))
        print('좋아요 : ' + like)
        print('조회수 : ' + view)
        print('주소 : ' + i)
        print()
    driver.close()

    '''
    expression_negative
    expression_positive
    following_cnt
    follower_cnt
    like_cnt
    comment_cnt
    share_cnt
    place_add
    post_cnt
    photo_cnt
    video_cnt
    friends_continuous_exchange
    friends_rating_index
    contents_regular
    '''

    # DB insert
    try:
        # Server Connection to MySQL
        db = db_mysql_connection_SCI.DatabaseConnection()
        db.kakao_insert(
            'instagram',  # platform
            user,  # page_id
            str(user_info['이름']),  # username
            str(user_info['성별']),  # gender
            str(user_info['거주지']),  # address
            str(user_info['생일']),  # birthday
            str(user_info['직장']),  # company1
            str(user_info['학교']),  # university1
            'expression_negative',
            'expression_positive',
            str(user_info['소식받는수']),  # take_news
            str(user_info['관심글']),  # post_interest
            str(user_info['up한글']),  # post_up
            str(generateNumKakaoResult[0]),  # feeling_cnt
            str(generateNumKakaoResult[1]),  # reply_cnt
            str(all_share_cnt),  # share_cnt
            str(generateNumKakaoResult[2]),  # place_cnt
            str(all_place_cnt),  # place_add
            str(user_info['스토리'].replace(",", "").replace("개", "")),  # post_cnt
            str(user_info['사진']),  # photo_cnt
            str(generateNumKakaoResult[3]),  # video_cnt
            'operation_year_period',
            'friends_continuous_exchange',
            'friends_rating_index',
            'friends_correlation_score',
            'contents_regular'
            # user_info['한줄소개']
            # user_info['한줄음악']
            # user_info['up']
        )
    except Exception as e_maria:
        logger.error(msg=e_maria)


if __name__ == "__main__":
    start_time_all = time.time()
    user_list = ['jelly_jilli', '3.48kg', '4x2a', '0.94k', 'helenwoooo', 'shuni_kaeun', 'haneul__haneul', 'yoou.ch',
                 'soy.oon', 'oao.v']
    for user in user_list:
        # 멀티 프로세싱
        pool = Pool(processes=8)
        pool.map(info, feed(user))

    end_time = time.time() - start_time_all
    print()
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)






