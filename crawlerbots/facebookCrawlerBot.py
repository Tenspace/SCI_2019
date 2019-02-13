# -*- coding: utf-8 -*-
import logging.handlers
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from SCI_2019.crawlerbots import db_mysql_connection_SCI
from SCI_2019.crawlerbots import generateNumEngine as genN
from SCI_2019.crawlerbots import expressionEngine as exprs
from SCI_2019.crawlerbots.registeredRecorduser import RegRecorduser
from SCI_2019.crawlerbots.selectDatedata import SelectDateData

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
    r"C:\\dev_tenspace\\2019_python_project_syhan\\201901_python36\\crawlerBot_pack_SCI_2019\\crawlerbots\\log\\" + hereWork + "_log_"
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


def start(user_list, start_date, end_date):
    options = Options()
    options.add_argument("--window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")

    url = 'https://m.facebook.com'
    path = r"C:\dev_tenspace\2019_python_project_syhan\201901_python36\crawlerBot_pack_SCI_2019\chromedriver.exe"

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

    for index, user in enumerate(user_list):
        data = ''
        try:
            driver, data = facebook_crawler_start(drivers, user, start_date, end_date)
            drivers = driver
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
                driver, data = facebook_crawler_start(drivers, user, start_date, end_date)
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


def facebook_crawler_start(drivers, user, start_date, end_date):
    print(drivers)
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
    result_dict['친구'] = ''
    result_dict['팔로워'] = ''
    result_dict['좋아요'] = ''
    result_dict['댓글'] = ''
    result_dict['공유'] = ''
    result_dict['장소추가'] = ''
    result_dict['포스트'] = ''
    result_dict['님이나온사진수'] = ''
    result_dict['사진수'] = ''
    result_dict['사진첩수'] = ''
    result_dict['사진첩카테고리수'] = ''
    result_dict['태그된동영상수'] = ''
    result_dict['동영상수'] = ''
    result_dict['TV프로그램'] = ''
    result_dict['영화'] = ''
    result_dict['좋아요모두'] = ''
    result_dict['음악'] = ''
    result_dict['책'] = ''
    result_dict['음식점'] = ''
    result_dict['운동선수'] = ''
    result_dict['스포츠팀'] = ''
    result_dict['앱과게임'] = ''
    result_dict['체크인'] = ''
    result_dict['이벤트'] = ''
    result_dict['리뷰'] = ''
    result_dict['사진첩카테고리'] = ''
    result_dict['동영상태그'] = ''
    result_dict['거주지친구'] = ''
    result_dict['출신지친구'] = ''
    result_dict['대학교친구'] = ''
    result_dict['고등학교친구'] = ''
    result_dict['직장친구'] = ''

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
                    # 기간 사이에 포스트만 insert
                    if start_date <= post_date <= end_date:
                        db = db_mysql_connection_SCI.DatabaseConnection()
                        db.post_insert(
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
    #print('########################')
    print('포스트 :', result_dict['포스트'])
    print('좋아요 :', result_dict['좋아요'])
    print('댓글 :', result_dict['댓글'])
    print('공유 :', result_dict['공유'])
    print('장소추가 :', result_dict['장소추가'])
    #print('########################')


    # expressionEngine.py
    expressRateResult = exprs.ExpressionEngine.expressionFind(exprs.ExpressionEngine)
    print("expressResult :", expressRateResult)

    generateNumFaceResult = genN.GenNumEngine.getCntInfo_face(genN.GenNumEngine)
    print(result_dict)
    # DB INSERT
    try:
        if result_dict['이름'] != '':
            # Server Connection to MySQL:+
            db = db_mysql_connection_SCI.DatabaseConnection()
            db.facebook_insert(
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
                str(generateNumFaceResult[5]),      # 'like_all_cnt',
                str(generateNumFaceResult[6]),         # 'like_movie_cnt',
                str(generateNumFaceResult[7]),      # 'like_tv_cnt',
                str(generateNumFaceResult[8]),         # 'like_music_cnt',
                str(generateNumFaceResult[9]),           # 'like_book_cnt',
                str(generateNumFaceResult[10]),    # 'like_sports_cnt'
                str(generateNumFaceResult[11]),    # 'like_athlete_cnt'
                str(generateNumFaceResult[12]),        # 'like_restaurant_cnt',
                str(generateNumFaceResult[13]),      # 'like_appgame_cnt',
                str(generateNumFaceResult[14]),        # 'check_in',
                str(generateNumFaceResult[15]),        # 'event',
                str(generateNumFaceResult[16]),         # 'review',
                str(result_dict['좋아요']),            # 'post_like'
                str(result_dict['댓글']),         # 'post_reply'
                str(result_dict['공유']),         # 'post_share'
                str(result_dict['장소추가']),        # 'place_add',
                str(result_dict['포스트']),       # 'post_cnt'
                str(result_dict['님이나온사진수']),  # 'photo_of_oneself_cnt',
                str(result_dict['사진수']),        # 'photo_cnt',
                str(result_dict['사진첩수']),       # 'album_cnt',
                str(generateNumFaceResult[17]),    # 'album_category_cnt',
                str(generateNumFaceResult[18]),      # 'video_tag_oneself_cnt',
                str(result_dict['동영상수']),       # 'video_cnt',
                str(generateNumFaceResult[19]),     #operation_year_period
                'friends_continuous_exchange',
                'friends_rating_index',
                'friends_correlation_score',
                'contents_regular'
            )
        else:
            print('유저 정보 없음')
    except Exception as e_maria:
        logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))
    return drivers, ''


# def auto_scroll(driver):
#
#     # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
#
#     # 20181016_edited_syhan
#     global auto_scroll_data_soup_html
#
#     # 화면 길이 만큼 나눠 auto_scroll 하고 각 페이지마다 데이터 가져오기
#     last_height = driver.execute_script("return document.body.scrollHeight")
#
#     auto_scroll_data = driver.page_source
#     auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')
#
#     # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
#     for cyc in range(0, 15):
#         # Scroll down to bottom
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         try:
#             WebDriverWait(driver, 3).until(lambda driver: driver.execute_script("return document.body.scrollHeight;") >
#                                                           last_height)
#         except Exception as e:
#             print(e, 'autoScroll 0')
#             auto_scroll_data = driver.page_source
#             auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')
#             return auto_scroll_data_soup_html
#
#         # # Calculate new scroll height and compare with last scroll height
#         # new_height = driver.execute_script("return document.body.scrollHeight")
#         # last_height = new_height
#
#     # auto_scroll crawling data 가져오기
#     auto_scroll_data = driver.page_source
#     auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')
#
#     return auto_scroll_data_soup_html


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

def main():
    regUser = RegRecorduser()
    user_list = regUser.call_userlist_fb()
    se = SelectDateData().selctDate()
    start_date = se[0]
    end_date = se[1]
    for user in user_list:
        start(user_list, start_date, end_date)
main()
