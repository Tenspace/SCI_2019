#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging.handlers
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawlerbots import db_mysql_connection_SCI

global returnValue_kks_CSVData
global returnValue_kks_singleData
global hereWork
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def feed(user_list):
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")

    path = r"C:\Users\tenspace\Desktop\crawlerBot_package_SCI\chromedriver.exe"
    driver = webdriver.Chrome(options=options, executable_path=path)

    for user in user_list:
        r = open('instagram_user.txt', mode='rt', encoding='utf-8')
        user_txt = r.read()
        r.close()
        if '_' + user + '_' not in user_txt:
            try:
                url = 'https://www.instagram.com/' + user + '/'
                driver.get(url)
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.DINPA")))

                result_dict = dict()
                result_dict['이름'] = ''
                result_dict['팔로잉'] = ''
                result_dict['팔로워'] = ''
                result_dict['좋아요'] = ''
                result_dict['장소추가'] = ''
                result_dict['총포스트'] = ''
                result_dict['사진'] = ''
                result_dict['동영상'] = ''

                print('feed 시작 ', '-' * 50)
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
                result_dict['이름'] = name
                result_dict['팔로잉'] = follows_cnt
                result_dict['팔로워'] = follower_cnt
                result_dict['총포스트'] = content_cnt
                print("닉네임 : " + user)
                print("게시물 수 : " + content_cnt)
                print("팔로워 : " + follower_cnt)
                print("팔로우 : " + follows_cnt)
                print("이름 : " + name)
                print("소개 : " + intro)
                print("홈페이지 : " + homepage)
                print()
                # print("이미지 : " + image)
                # image = driver.find_element_by_css_selector('div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div.KL4Bh > img').get_attribute('src')
                # tag_cnt = driver.find_element_by_css_selector('main > header > div.f7QXd.SM9CE > div > span > span').text

                # 스크롤내리는 횟수
                scroll_count = 5
                # 중복 href 카운트
                same_count = 0
                # 게시물마다 href 를 담을 리스트
                href = []

                for i in range(0, scroll_count):
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    href_html = soup.select('div > div > div.v1Nh3 > a')
                    for href_list in href_html:
                        if href_list['href'] in href:
                            same_count += 1
                        else:
                            href.append(href_list['href'])
                    time.sleep(1)
                    print("Scrolling... "+str(i+1)+"/"+str(scroll_count) + ", 현재: " + str(len(href)) + ", 중복: " + str(same_count))
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print(str(len(href)) + "개의 결과를 찾았습니다.")
                print()
                place_add = 0
                like_all_cnt = 0
                video_cnt = 0
                photo_all_cnt = 0
                if 0 < len(href):
                    for i in href:
                        # 크롤링할 주소
                        user_url = "https://www.instagram.com" + i
                        driver.get(user_url)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.DINPA")))

                        source2 = driver.page_source
                        soup = BeautifulSoup(source2, 'html.parser')

                        post_date = soup.select('div.eo2As > div.k_Q0X.NnvRN > a > time')
                        for a in post_date:
                            post_date = a['title']
                        post_date = post_date.replace('년', '-').replace('월', '-').replace("일", '').replace('오전', 'AM'). \
                            replace('오후', 'PM').replace(' ', '')
                        #
                        try:
                            # 장소추가
                            place = soup.select('div.o-MQd > div.M30cS > a')[0].text
                            place_add += 1
                            print('장소 : ' + place)
                        except Exception as e:
                            place = ''
                            print('장소 없음 :', e)

                        try:
                            # 본문
                            content = soup.select('div.KlCQn.EtaWk > ul > li:nth-of-type(1) > div > div > div > span')[0].text
                            print('본문 : ' + content)
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
                        try:
                            photo_cnt = soup.select('div.Yi5aA')
                        except Exception as e:
                            photo_cnt = []
                            print('사진 또는 동영상 한 개', e)
                        photo_all_cnt += len(photo_cnt)

                        # @태그 pass
                        tag_list = ''
                        for j in tag:
                            if '#' in j.text:
                                tag_list += j.text
                            elif '@' in j.text:
                                pass
                            else:
                                pass
                        print('태그 : ' + tag_list)
                        # url_pattern = "(/p/)([0-9a-zA-Z|_|-]*)(/\?tagged=)([0-9a-zA-Z가-힣ㄱ-ㅎ]*)"
                        # main_re = re.compile(url_pattern)
                        # main_tag = main_re.findall(i)

                        # 사진인지 동영상인지 체크
                        if '좋아' in like_check:
                            like = like_cnt.replace(',', '')
                            print('좋아요 : ' + like)
                            view = '0'
                        elif '조회' in like_check:
                            like = '0'
                            video_cnt += 1
                            view = like_cnt.replace(',', '').replace('조회 ', '').replace('수', '')
                            print('조회수 : ' + view.replace('회', ''))
                        else:
                            like = '0'
                            view = '0'
                        like_all_cnt += int(like)
                        print()
                        try:
                            # Server Connection to MySQL
                            db = db_mysql_connection_SCI.DatabaseConnection()
                            db.post_insert(
                                '',
                                'insta',  # platform
                                user,  # page_id
                                content,
                                like,
                                None,
                                None,
                                post_date
                            )
                        except Exception as e_maria:
                            logger.error(msg=e_maria)
                else:
                    print('게시물 없음')

                # db
                result_dict['좋아요'] = like_all_cnt
                result_dict['장소추가'] = place_add
                result_dict['사진'] = photo_all_cnt
                result_dict['동영상'] = video_cnt
                try:
                    # Server Connection to MySQL
                    db = db_mysql_connection_SCI.DatabaseConnection()
                    db.insta_insert(
                        '',
                        'insta',  # platform
                        user,  # page_id
                        'expression_negative',
                        'expression_positive',
                        str(result_dict['이름']), # username
                        str(result_dict['팔로잉']),  # following_cnt
                        str(result_dict['팔로워']),  # follower_cnt
                        str(result_dict['총포스트']),  # post_cnt
                        str(result_dict['좋아요']),  # like_cnt
                        str(result_dict['장소추가']),  # place_add
                        str(result_dict['사진']),  # photo_cnt
                        str(result_dict['동영상']),  # video_cnt
                        'operation_year_period',
                        'friends_continuous_exchange',
                        'friends_rating_index',
                        'contents_regular'
                    )
                except Exception as e_maria:
                    logger.error(msg=e_maria)

                f = open('instagram_user.txt', mode='at', encoding='utf-8')
                f.write('_' + user + '_\n')
                f.close()
            except Exception as e:
                print('아이디 존재 x')
        else:
            print('이미 크롤링 한 데이터')


def main():
    start_time_all = time.time()

    user_list = ['dudgns3209', 'ㅎㅎ245ㄴ', 'jelly_jilli', '3.48kg', '4x2a', '0.94k', 'helenwoooo', 'shuni_kaeun', 'haneul__haneul', 'yoou.ch',
                 'soy.oon', 'oao.v']

    feed(user_list)

    end_time = time.time() - start_time_all
    print()
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)


