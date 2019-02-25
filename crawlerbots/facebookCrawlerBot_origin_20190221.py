# -*- coding: utf-8 -*-
import logging.handlers
import time
import re
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from crawlerbots import db_mysql_connection_SCI
from crawlerbots import generateNumEngine as genN
from crawlerbots import expressionEngine as exprs
from crawlerbots.registeredRecorduser import RegRecorduser
from crawlerbots.selectDatedata import SelectDateData
# db에 int로 넣기 전 백업.
hereWork = str('Facebook')
now = datetime.now()
currentTime = '%s_%s_%s' % (now.year, now.month, now.day)

# logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger(hereWork + '_logging')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# fileHandler 와 StreamHandler 를 생성
file_max_bytes = 10 * 1024 * 1024  # log file size : 10MB

fileHandler = logging.handlers.RotatingFileHandler(
    r"C:\\Users\\tenspace\\Desktop\\SCI_2019\\crawlerbots\\log\\" + hereWork + "_log_"
    + currentTime, maxBytes=file_max_bytes, backupCount=10)

streamHandler = logging.StreamHandler()

# handler 에 formatter 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

# Handler 를 logging 에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

# logging
logging.debug(hereWork + '_crawler_bot_debugging on' + currentTime)
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')


def start(user_list, start_date, end_date, origin_ph, origin_name):
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")

    url = 'https://m.facebook.com'
    path = r'C:\Users\tenspace\Desktop\SCI_2019\chromedriver.exe'

    drivers = webdriver.Chrome(options=options, executable_path=path)
    drivers.get(url)
    WebDriverWait(drivers, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.other-links")))

    #1
    # drivers.find_element_by_name('email').send_keys('riei1005@naver.com')
    # drivers.find_element_by_name('pass').send_keys('4109121z#!')
    #
    #2
    drivers.find_element_by_name('email').send_keys('01027746254')
    drivers.find_element_by_name('pass').send_keys('Gkstkddbs4$')

    drivers.find_element_by_name('login').click()
    WebDriverWait(drivers, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#rootcontainer")))

    start_time_all = time.time()
    # 1. 86  : search_log 테이블에 페이스북 주소가 있으면 크롤링함
    # 2. 보류  : txt 파일에 똑같은 주소가 없으면 크롤링함 (크롤링 후 kakaoStory_user.txt 에 주소를 기입함)
    # 3. 196 : search_log 테이블에 real_name 필드에 값과 카카오스토리 이름이 같으면 크롤링함 똑같지 않으면 mismatch 테이블에 insert
    for index, user in enumerate(user_list):
        data = ''
        # pageid가 숫자인 경우
        try:
            p = re.findall('=\w+&', user)
            user = p[0].replace('=', '').replace('&', '')
        except Exception as e:
            # 자신이 변경한 pageid인 경우
            if user:
                try:
                    p = re.findall('\/\w+\s', user)
                    user = p[0].replace('/', '')
                except Exception as e:
                    pass
            # pageid가 없는 경우
            else:
                pass

        try:
            if user is not None and user != '':
                driver, data = facebook_crawler_start(drivers, user, start_date, end_date, origin_ph[index], origin_name[index])
                drivers = driver
            else:
                pass
        except Exception as e:
            print('err 1', e)
            options = Options()
            options.add_argument("--window-size=1920x1080")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
            #path = r"C:\Users\tenspace\Desktop\crawlerBot_package_2019_SCI\chromedriver.exe"
            path = "..\chromedriver.exe"
            drivers = webdriver.Chrome(options=options, executable_path=path)
            print(drivers)
            try:
                drivers.get(url)
                WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.other-links")))
                # 1
                # drivers.find_element_by_name('email').send_keys('riei1005@naver.com')
                # drivers.find_element_by_name('pass').send_keys('4109121z#!')
                #
                # 2
                drivers.find_element_by_name('email').send_keys('01027746254')
                drivers.find_element_by_name('pass').send_keys('Gkstkddbs4$')
                drivers.find_element_by_name('login').click()
                WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#rootcontainer")))
                driver, data = facebook_crawler_start(drivers, user, start_date, end_date, origin_ph[index], origin_name[index])
            except Exception as e:
                print(drivers)
                print('err 2', e)
        # WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#rootcontaineraaa")))
        print(data)
        print(index)
        print(drivers)
        print()
        print('#' * 200)
        print()

    print('데이터 기반 크롤링 총 구동 시간 :', time.time() - start_time_all)


def facebook_crawler_start(drivers, user, start_date, end_date, origin_ph, origin_name):
    print('start :', drivers)
    result_dict = dict()
    result_dict['이름'] = ''
    result_dict['직장1'] = ''
    result_dict['직장2'] = ''
    result_dict['직장3'] = ''
    result_dict['학력1'] = ''
    result_dict['학력2'] = ''
    result_dict['학력3'] = ''
    result_dict['거주했던장소1'] = ''
    result_dict['거주했던장소2'] = ''
    result_dict['거주했던장소3'] = ''
    result_dict['휴대폰'] = ''
    result_dict['Instagram'] = ''
    result_dict['웹사이트'] = ''
    result_dict['생일'] = ''
    result_dict['성별'] = ''
    result_dict['친구'] = '0'
    result_dict['팔로워'] = '0'
    result_dict['좋아요'] = '0'
    result_dict['댓글'] = '0'
    result_dict['공유'] = '0'
    result_dict['장소추가'] = '0'
    result_dict['포스트'] = '0'
    result_dict['님이나온사진수'] = '0'
    result_dict['사진수'] = '0'
    result_dict['사진첩수'] = '0'
    result_dict['사진첩카테고리수'] = '0'
    result_dict['태그된동영상수'] = '0'
    result_dict['동영상수'] = '0'
    result_dict['TV프로그램'] = '0'
    result_dict['영화'] = '0'
    result_dict['좋아요모두'] = '0'
    result_dict['음악'] = '0'
    result_dict['책'] = '0'
    result_dict['음식점'] = '0'
    result_dict['운동선수'] = '0'
    result_dict['스포츠팀'] = '0'
    result_dict['앱과게임'] = '0'
    result_dict['체크인'] = '0'
    result_dict['이벤트'] = '0'
    result_dict['리뷰'] = '0'
    result_dict['사진첩카테고리'] = '0'
    result_dict['동영상태그'] = '0'
    result_dict['거주지친구'] = '0'
    result_dict['출신지친구'] = '0'
    result_dict['대학교친구'] = '0'
    result_dict['고등학교친구'] = '0'
    result_dict['직장친구'] = '0'
    result_dict['컨텐츠관리일정성'] = '0'
    result_dict['지속적교류'] = '0'
    result_dict['평가지수'] = '0'
    result_dict['친구별상관도'] = '0'
    ############################################################################################################
    # 정보
    if '1000' in user:
        drivers.get('https://m.facebook.com/profile.php?v=info&id=' + user)
    else:
        drivers.get('https://m.facebook.com/' + user + '/about')

    WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
    html_soup = auto_scroll2(drivers)

    print('[ 이름 ]')
    try:
        name = html_soup.select('title')[0].text
        result_dict['이름'] = name
        print(result_dict['이름'])
    except Exception as e:
        print('', e)
    if origin_name == name:
        print('[ 직장 ]')
        try:
            work_list = html_soup.select('#work > div > div')
            for i in range(len(work_list)):
                work = html_soup.select('#work > div > div:nth-of-type(' + str(i+1) + ')')[0].text
                result_dict['직장'+str(i+1)] = work
                print(result_dict['직장'+str(i+1)])
        except Exception as e:
            print('직장', e)

        print('[ 학력 ]')
        try:
            edu_list = html_soup.select('#education > div > div')
            for i in range(len(edu_list)):
                edu = html_soup.select('#education > div > div:nth-of-type(' + str(i+1) + ')')[0].text
                result_dict['학력' + str(i + 1)] = edu
                print(result_dict['학력' + str(i + 1)])
        except Exception as e:
            print('학력', e)

        print('[ 거주했던 장소 ]')
        try:
            living_list = html_soup.select('#living > div > div')
            for i in range(len(living_list)):
                living = html_soup.select('#living > div > div:nth-of-type(' + str(i+1) + ')')[0].text
                result_dict['거주했던장소' + str(i + 1)] = living
                print(result_dict['거주했던장소' + str(i + 1)])
        except Exception as e:
            print('거주했던 장소', e)

        print('[ 연락처 정보 ]')
        try:
            contact_info_list = html_soup.select('#contact-info > div > div')
            for i in range(len(contact_info_list)):
                contact_info = html_soup.select('#contact-info > div > div:nth-of-type('
                                                + str(i+1) + ') > div > div:nth-of-type(1)')[0].text
                contact_info_title = html_soup.select('#contact-info > div > div:nth-of-type('
                                                      + str(i + 1) + ') > div > div:nth-of-type(2)')[0].text
                result_dict[contact_info_title] = contact_info
                print(contact_info_title, result_dict[contact_info_title])
        except Exception as e:
            print('연락처 정보', e)

        print('[ 전문 기술 ]')
        try:
            skills_list = html_soup.select('#skills > div > div')
            skills_name = html_soup.select('#skills > header')[0].text.replace(' ', '')
            for i in range(len(skills_list)):
                skills = html_soup.select('#skills > div > div:nth-of-type(' + str(i+1) + ')')[0].text
                result_dict[skills_name] = skills
                print(result_dict[skills_name])
        except Exception as e:
            print('전문 기술', e)

        print('[ 기본 정보 ]')
        try:
            basic_info_list = html_soup.select('#basic-info > div > div')
            for i in range(len(basic_info_list)):
                basic_info = html_soup.select('#basic-info > div > div:nth-of-type('
                                              + str(i+1) + ') > div > div:nth-of-type(1)')[0].text
                basic_info_title = html_soup.select('#basic-info > div > div:nth-of-type('
                                                    + str(i + 1) + ') > div > div:nth-of-type(2)')[0].text
                result_dict[basic_info_title] = basic_info
                print(basic_info_title, result_dict[basic_info_title])
        except Exception as e:
            print('기본 정보', e)

        print('[ 결혼/연애 상태 ]')

        try:
            relationship = html_soup.select('#relationship > div > div > div > div > div > div > div:nth-of-type(2) > '
                                            'header > h3:nth-of-type(1)')[0].text
            relationship_status = html_soup.select('#relationship > div > div > div > div > div > div > '
                                                   'div:nth-of-type(2) > header > h3:nth-of-type(2)')[0].text
            result_dict['결혼연애상태'] = relationship + ' ' + relationship_status
            print(result_dict['결혼연애상태'])
        except Exception as e:
            try:
                relationship_status = html_soup.select('#relationship > div')[0].text
                result_dict['결혼연애상태'] = relationship_status
                print(result_dict['결혼연애상태'], e)
            except Exception as e:
                print('결혼/연애 상태', e)

        print('[ 가족 ]')
        try:
            family_list = html_soup.select('#family > div > div')
            for i in range(len(family_list)):
                family = html_soup.select('#family > div > div:nth-of-type('
                                          + str(i+1) + ') > div > div > div:nth-of-type(2) > header > '
                                                       'h3:nth-of-type(1)')[0].text
                family_title = html_soup.select('#family > div > div:nth-of-type('
                                                + str(i+1) + ') > div > div > div:nth-of-type(2) > header > '
                                                             'h3:nth-of-type(2)')[0].text
                result_dict['가족'+str(i+1)] = family + ' ' + family_title
                print(result_dict['가족'+str(i+1)])
        except Exception as e:
            try:
                family = html_soup.select('#family > div > div')[0].text
                result_dict['가족1'] = family
                print(result_dict['가족1'])
            except Exception as e:
                print('가족 없음', e)

        print('[ 좋아하는 문구 ]')
        try:
            quote_name = html_soup.select('#quote > header')[0].text.replace(' ', '')
            quote = html_soup.select('#quote > div')[0].text
            result_dict[quote_name] = quote
            print(result_dict[quote_name])
        except Exception as e:
            print('좋아하는 문구 없음', e)

        print('[ 다른 이름 ]')
        try:
            nicknames_name = html_soup.select('#nicknames > header')[0].text.replace(' ', '')
            nicknames = html_soup.select('#nicknames > div > div > div > div:nth-of-type(1)')[0].text
            nicknames_title = html_soup.select('#nicknames > div > div > div > div:nth-of-type(2)')[0].text
            result_dict[nicknames_name] = nicknames
            print(nicknames_title, result_dict[nicknames_name])
        except Exception as e:
            print('다른 이름 없음', e)

        ############################################################################################################
        # 친구
        if '1000' in user:
            drivers.get('https://m.facebook.com/profile.php?v=friends&id=' + user)
        else:
            drivers.get('https://m.facebook.com/' + user + '/friends')

        WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
        html = drivers.page_source
        html_soup = BeautifulSoup(html, 'html.parser')

        print('[ 친구 ]')
        try:
            friends = html_soup.select('.friendsActionItem > div:nth-of-type(2) > '
                                       'div:nth-of-type(2)')[0].text.replace('친구 ', '').replace('명', '')
            result_dict['친구'] = friends
            print(result_dict['친구'])
        except Exception as e:
            print('친구 없음', e)

        ############################################################################################################
        # 사진
        if '1000' in user:
            drivers.get('https://m.facebook.com/profile.php?v=photos&id=' + user)
        else:
            drivers.get('https://m.facebook.com/' + user + '/photos')

        WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
        html = drivers.page_source
        html_soup = BeautifulSoup(html, 'html.parser')

        print('[ 님이 나온 사진 ]')
        try:
            photos_name = html_soup.select('.subpage > div:nth-of-type(1)')[0].text
            html_soup = auto_scroll2(drivers)
            photos_cnt = html_soup.select('.photos a')
            result_dict['님이나온사진수'] = str(len(photos_cnt))
            print(result_dict['님이나온사진수'])
        except Exception as e:
            print('님이 나온 사진 없음', e)

        albums = []
        photo_cnt = 0
        print('[ 사진첩 ]')
        try:
            albums_list = html_soup.select('.albums > div > div > a')
            result_dict['사진첩수'] = str(len(albums_list))
            print(result_dict['사진첩수'])

            for i in albums_list:
                albums.append(i['href'])
            for j in albums:
                drivers.get('https://m.facebook.com' + j)
                try:
                    WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#m_more_item")))
                    drivers.find_element_by_css_selector('#m_more_item').click()
                    html_soup = auto_scroll2(drivers)
                    photo = html_soup.select('div#rootcontainer a > div > i')
                    photo_cnt += len(photo)
                except Exception as e:
                    html = drivers.page_source
                    html_soup = BeautifulSoup(html, 'html.parser')
                    photo = html_soup.select('div#rootcontainer a > div > i')
                    photo_cnt += len(photo)
            result_dict['사진수'] = str(photo_cnt)
            print('[ 사진수 ]')
            print(result_dict['사진수'])
        except Exception as e:
            print('사진 없음', e)

        ############################################################################################################
        # 팔로워
        if '1000' in user:
            drivers.get('https://m.facebook.com/profile.php?v=followers&id=' + user)
        else:
            drivers.get('https://m.facebook.com/' + user + '/?v=followers')
        WebDriverWait(drivers, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
        html = drivers.page_source
        html_soup = BeautifulSoup(html, 'html.parser')
        print('[ 팔로워 ]')
        try:
            follower_cnt = html_soup.select('div#rootcontainer header span')[0].text
            result_dict['팔로워'] = follower_cnt
            print(result_dict['팔로워'])
        except Exception as e:
            print('팔로워 없음', e)
        ############################################################################################################
        # 타임라인
        drivers.get('https://m.facebook.com/' + user)
        html_soup = auto_scroll2(drivers)

        post_cnt = 0
        video_cnt = 0
        like_cnt = 0
        reply_cnt = 0
        share_cnt = 0
        place_add_cnt = 0
        post_date_cnt = 0

        print('[ 동영상 ]')
        try:
            video = html_soup.select('div._1o0y')
            video_cnt = len(video)
            print(video_cnt)
            result_dict['동영상수'] = str(video_cnt)
        except Exception as e:
            print(video_cnt)

        try:
            section = html_soup.select('section.storyStream')
            for i in section:
                article_list = html_soup.select('section#' + i['id'] + ' > article')
                for j in range(len(article_list)):
                    try:
                        post_text = ''
                        post_like = 0
                        post_reply = 0
                        post_share = 0

                        # 날짜
                        post_date = html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                     + str(j+1) + ') > div > header > div:nth-of-type(2)'
                                                                  ' > div > div > div:nth-of-type(1) > div > a > abbr')[0].text
                        if '시간' in post_date or '분' in post_date:
                            post_date = '%s-%s-%s' % (now.year, now.month, now.day)
                        elif '어제' in post_date:
                            post_date = '%s-%s-%s' % (now.year, now.month, (now.day-1))
                        elif '오후' not in post_date and '오전' not in post_date:
                            post_date = post_date.replace('년', '-').replace('월', '-').replace("일", '').replace(' ', '')
                            post_date = datetime.strptime(post_date, '%Y-%m-%d')
                        elif '년' in post_date:
                            post_date = post_date.replace('년', '-').replace('월', '-').replace("일", '').replace('오전', 'AM').\
                                replace('오후', 'PM').replace(' ', '')
                            post_date = datetime.strptime(post_date, '%Y-%m-%d%p%I:%M')
                            post_date = post_date.strftime('%Y-%m-%d')
                        else:
                            post_date = str(now.year) + '년 ' + post_date
                            post_date = post_date.replace('년', '-').replace('월', '-').replace("일", '').replace('오전', 'AM').\
                                replace('오후', 'PM').replace(' ', '')
                            post_date = datetime.strptime(post_date, '%Y-%m-%d%p%I:%M')
                            post_date = post_date.strftime('%Y-%m-%d')
                        # 텍스트
                        try:
                            post_text = html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                         + str(j+1) + ') > div > div > span')[0].text
                        except Exception as e:
                            pass
                        # 좋아요
                        try:
                            post_like = int(html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                             + str(j+1) + ') > footer div._1g06')[0].text.replace('명', ''))
                            like_cnt += post_like
                        except Exception as e:
                            pass
                        # 댓글
                        try:
                            post_reply = int(html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                     + str(j + 1) + ') > footer div._1fnt > span:nth-of-type(1)')[0].text.replace('댓글 ', '').replace('개', ''))
                            post_share = int(html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                     + str(j + 1) + ') > footer div._1fnt > span:nth-of-type(2)')[0].text.replace('공유 ', '').replace('회', ''))
                            reply_cnt += post_reply
                            share_cnt += post_share
                        except Exception as e:
                            try:
                                post_reply_share = html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                                    + str(j + 1) + ') > footer span._1j-c')[0].text
                                if '댓글' in post_reply_share:
                                    post_reply = int(post_reply_share.replace('댓글 ', '').replace('개', ''))
                                    reply_cnt += post_reply
                                else:
                                    post_share = int(post_reply_share.replace('공유 ', '').replace('회', ''))
                                    share_cnt += post_share
                            except Exception as e:
                                pass
                        # 장소추가
                        try:
                            place_add = html_soup.select('section#' + i['id'] + ' > article:nth-of-type('
                                                         + str(j+1) + ') > div > header > div:nth-of-type(2) > div > '
                                                                      'div > div:nth-of-type(1) > h3')[0].text
                            if '에 있습니다' in place_add:
                                place_add_cnt += 1
                        except Exception as e:
                            pass

                        # 현재 날짜, 월
                        current_month = '%s-%s' % (now.year, now.month)
                        current_month = datetime.strptime(current_month, '%Y-%m')
                        current_month = current_month.strftime('%Y-%m')
                        # 전 달 날짜, 월
                        last_month = '%s-%s' % (now.year, now.month - 1)
                        last_month = datetime.strptime(last_month, '%Y-%m')
                        last_month = last_month.strftime('%Y-%m')
                        # 게시물 날짜, 월
                        post_date_month = str(post_date)[:7]

                        if current_month == post_date_month:
                            post_date_cnt += 1
                        elif last_month == post_date_month:
                            post_date_cnt += 1
                        else:
                            pass

                        # 기간 사이에 포스트만 insert
                        if start_date <= post_date <= end_date:
                            db = db_mysql_connection_SCI.DatabaseConnection()
                            db.post_insert(
                                origin_ph,
                                'facebook',
                                user,
                                str(post_text),
                                str(post_like),
                                str(post_reply),
                                str(post_share),
                                post_date
                            )
                        else:
                            pass

                        # 포스트 갯수
                        post_cnt += 1

                    except Exception as e:
                        pass
                        # print('게시물 아님', e)
        except Exception as e:
            print('', e)

        result_dict['포스트'] = post_cnt
        result_dict['좋아요'] = like_cnt
        result_dict['댓글'] = reply_cnt
        result_dict['공유'] = share_cnt
        result_dict['장소추가'] = place_add_cnt
        print('포스트 :', result_dict['포스트'])
        print('좋아요 :', result_dict['좋아요'])
        print('댓글 :', result_dict['댓글'])
        print('공유 :', result_dict['공유'])
        print('장소추가 :', result_dict['장소추가'])

        rating = like_cnt + reply_cnt + share_cnt
        try:
            regular = post_cnt // reply_cnt
        except Exception as e:
            regular = 0
        result_dict['컨텐츠관리일정성'] = post_date_cnt
        result_dict['지속적교류'] = regular
        result_dict['평가지수'] = rating

        # 페이지 좋아요
        #############################################################################################

        user_page_id = html_soup.select('#m-timeline-cover-section > div > div:nth-of-type(2) > div:nth-of-type(2) > '
                                        'div > div:nth-of-type(1) > a')
        id_list = []
        for page_id in user_page_id:
            id_list.append(page_id.get('href'))
        p = re.findall('=\w+&', id_list[0])
        ida = str(p[0].replace('=', '').replace('&', '%'))

        check_in_cnt = 0
        music_cnt = 0
        tv_cnt = 0
        app_cnt = 0
        like_all_cnt = 0
        food_cnt = 0
        book_cnt = 0
        movie_cnt = 0
        sports_cnt = 0
        sports_man_cnt = 0
        review_cnt = 0
        event_cnt = 0

        # 체크인 section
        try:
            drivers.get('https://m.facebook.com/timeline/app_section/?section_token=' + ida + '3A302324425790')
            WebDriverWait(drivers, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                check_in_cnt += int(val.text)
            print('체크인 :', check_in_cnt)
            result_dict['체크인'] = check_in_cnt
        except Exception as e:
            print('체크인 없음.', e)

        # 음악 section
        try:
            drivers.get('https://m.facebook.com/timeline/app_section/?section_token=' + ida + '3A221226937919712')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                music_cnt += int(val.text)
            print('음악 :', music_cnt)
            result_dict['음악'] = music_cnt
        except Exception as e:
            print('음악 없음.', e)

        # 스포츠팀 section
        try:
            drivers.get('https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A330076653784935%3A95')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                sports_cnt += int(val.text)
            print('스포츠팀 :', sports_cnt)
            result_dict['스포츠팀'] = sports_cnt
        except Exception as e:
            print('스포츠팀 없음.', e)

        # 운동선수 section
        try:
            drivers.get('https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A330076653784935%3A99')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                sports_man_cnt += int(val.text)
            print('운동선수 :', sports_man_cnt)
            result_dict['운동선수'] = sports_man_cnt
        except Exception as e:
            print('운동선수 없음.', e)

        # TV 프로그램 section100005121637375%%3A2409997254%3A107
        try:
            drivers.get(
                'https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A2409997254%3A107')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                tv_cnt += int(val.text)
            print('TV프로그램 :', tv_cnt)
            result_dict['TV프로그램'] = tv_cnt
        except Exception as e:
            print('TV프로그램 없음.', e)

        # 앱과 게임 collection
        try:
            drivers.get(
                'https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A249944898349166%3A58')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                app_cnt += int(val.text)
            print('앱과 게임 :', app_cnt)
            result_dict['앱과게임'] = app_cnt
        except Exception as e:
            print('앱과 게임 없음.', e)

        # 좋아요 모두 collection
        try:
            drivers.get('https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A2409997254%3A96')
            WebDriverWait(drivers, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                like_all_cnt += int(val.text.replace(',', ''))
            print('좋아요 모두 :', like_all_cnt)
            result_dict['좋아요모두'] = like_all_cnt
        except Exception as e:
            print('좋아요 모두 없음.', e)

        # 음식점 collection
        try:
            drivers.get('https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A2409997254%3A73')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                food_cnt += int(val.text)
            print('음식점 :', food_cnt)
            result_dict['음식점'] = food_cnt
        except Exception as e:
            print('음식점 없음.', e)

        # 책 collection
        try:
            drivers.get(
                'https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A2409997254%3A108')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                book_cnt += int(val.text)
            print('책 :', book_cnt)
            result_dict['책'] = book_cnt
        except Exception as e:
            print('책 없음.', e)

        # 영화 collection
        try:
            drivers.get(
                'https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A2409997254%3A106')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                movie_cnt += int(val.text)
            print('영화 :', movie_cnt)
            result_dict['영화'] = movie_cnt
        except Exception as e:
            print('영화 없음.', e)

        # 리뷰 collection
        try:
            drivers.get(
                'https://m.facebook.com/timeline/app_collection/?collection_token=' + ida + '3A254984101287276%3A105')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                review_cnt += int(val.text)
            print('리뷰 :', review_cnt)
            result_dict['리뷰'] = review_cnt
        except Exception as e:
            print('리뷰 없음.', e)

        # 이벤트 section
        try:
            drivers.get('https://m.facebook.com/timeline/app_section/?section_token=' + ida + '3A2344061033')
            WebDriverWait(drivers, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#static_templates")))
            html = drivers.page_source
            html_soup = BeautifulSoup(html, 'html.parser')
            value = html_soup.select('#timelineBody header span')
            for val in value:
                event_cnt += int(val.text)
            print('이벤트 :', event_cnt)
            result_dict['이벤트'] = event_cnt
        except Exception as e:
            print('이벤트 없음.', e)
        # ################################################################################################
        # expressionEngine.py
        expressRateResult = exprs.ExpressionEngine.expressionFind(exprs.ExpressionEngine)
        print("expressResult :", expressRateResult)

        generateNumFaceResult = genN.GenNumEngine.getCntInfo_face(genN.GenNumEngine, int(result_dict['친구']), int(result_dict['포스트']))
        friends1 = generateNumFaceResult[0]
        friends2 = generateNumFaceResult[1]
        friends3 = generateNumFaceResult[2]
        friends4 = generateNumFaceResult[3]
        friends5 = generateNumFaceResult[4]
        friends_cnt = friends1 + friends2 + friends3 + friends4 + friends5
        result_dict['친구별상관도'] = friends_cnt

        print(result_dict)
        # DB INSERT
        try:
            if result_dict['이름'] != '':
                # Server Connection to MySQL:+
                db = db_mysql_connection_SCI.DatabaseConnection()
                db.facebook_insert(
                    origin_ph,                                  # origin_ph
                    'facebook',                                 # platform
                    user,                                       # page_id
                    str(result_dict['이름']),                     # name
                    str(result_dict['성별']),                     # gender
                    str(result_dict['휴대폰']),                    # 'phone_number',
                    str(result_dict['생일']),             # 'birthday',
                    str(result_dict['직장1']),             # company1
                    str(result_dict['직장2']),              # company2
                    str(result_dict['직장3']),             # company3
                    str(result_dict['학력1']),             # university1
                    str(result_dict['학력2']),             # university2
                    str(result_dict['학력3']),             # university3
                    str(result_dict['거주했던장소1']),             # address1
                    str(result_dict['거주했던장소2']),             # address2
                    str(result_dict['거주했던장소3']),             # address3
                    str(result_dict['Instagram']),              # 'contact1',
                    str(result_dict['웹사이트']),               # 'contact2',
                    str(expressRateResult[0]),                  # expression_negative
                    str(expressRateResult[1]),                      # expression_positive
                    str(result_dict['친구']),                 # 'friends_all',
                    str(generateNumFaceResult[0]),                  # 'friends_residence',
                    str(generateNumFaceResult[1]),               # 'friends_company',
                    str(generateNumFaceResult[2]),              # 'friends_univ',
                    str(generateNumFaceResult[3]),         # 'friends_highschool',
                    str(generateNumFaceResult[4]),          # 'friends_native',
                    str(result_dict['팔로워']),                # 'follower_cnt',
                    str(result_dict['좋아요모두']),  # 'like_all_cnt',
                    str(result_dict['영화']),  # 'like_movie_cnt',
                    str(result_dict['TV프로그램']),  # 'like_tv_cnt',
                    str(result_dict['음악']),  # 'like_music_cnt',
                    str(result_dict['책']),  # 'like_book_cnt',
                    str(result_dict['스포츠팀']),  # 'like_sports_cnt'
                    str(result_dict['운동선수']),  # 'like_athlete_cnt'
                    str(result_dict['음식점']),  # 'like_restaurant_cnt',
                    str(result_dict['앱과게임']),  # 'like_appgame_cnt',
                    str(result_dict['체크인']),  # 'check_in',
                    str(result_dict['이벤트']),  # 'event',
                    str(result_dict['리뷰']),  # 'review',
                    str(result_dict['좋아요']),            # 'post_like'
                    str(result_dict['댓글']),         # 'post_reply'
                    str(result_dict['공유']),         # 'post_share'
                    str(result_dict['장소추가']),        # 'place_add',
                    str(result_dict['포스트']),       # 'post_cnt'
                    str(result_dict['님이나온사진수']),  # 'photo_of_oneself_cnt',
                    str(result_dict['사진수']),        # 'photo_cnt',
                    str(result_dict['사진첩수']),       # 'album_cnt',
                    str(generateNumFaceResult[5]),    # 'album_category_cnt',
                    str(generateNumFaceResult[6]),      # 'video_tag_oneself_cnt',
                    str(result_dict['동영상수']),       # 'video_cnt',
                    str(generateNumFaceResult[7]),     # operation_year_period
                    str(result_dict['컨텐츠관리일정성']),
                    str(result_dict['평가지수']),
                    str(result_dict['친구별상관도']),
                    str(result_dict['지속적교류']),
                )
            else:
                print('유저 정보 없음')
        except Exception as e_maria:
            logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))
    else:
        print('origin name, kakao name 불일치')
        try:
            # Server Connection to MySQL
            db = db_mysql_connection_SCI.DatabaseConnection()
            db.mismatch(
                str(origin_ph),  # origin_ph
                'facebook',  # platform
                str(origin_name),  # name
                str(name),  # platform_name
                str(user),  # url
            )
        except Exception as e_maria:
            logger.error(msg=e_maria)
    return drivers, ''


def auto_scroll2(driver):

    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요

    # 20181016_edited_syhan
    global auto_scroll_data_soup_html

    # 화면 길이 만큼 나눠 auto_scroll 하고 각 페이지마다 데이터 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    auto_scroll_data = driver.page_source
    auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 15):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
        # auto_scroll crawling data 가져오기
    auto_scroll_data = driver.page_source
    auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')

    return auto_scroll_data_soup_html


def main(user_list, origin_ph_list, origin_name_list):
    se = SelectDateData().selctDate()
    start_date = se[0]
    end_date = se[1]
    start(user_list, start_date, end_date, origin_ph_list, origin_name_list)
