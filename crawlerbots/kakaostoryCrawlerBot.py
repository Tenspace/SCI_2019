# -*- coding: utf-8 -*-
import logging.handlers
import time
from datetime import datetime
from crawlerBot_pack_SCI_2019.crawlerbots import db_mysql_connection_SCI
from crawlerBot_pack_SCI_2019.crawlerbots import expressionEngine as exprs
from crawlerBot_pack_SCI_2019.crawlerbots import generateNumEngine as genN

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

hereWork = str('kakaoStory')
now = datetime.now()
currentTime = '%s_%s_%s' % (now.year, now.month, now.day)

# logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger(hereWork+'_logging')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# fileHandler 와 StreamHandler 를 생성
file_max_bytes = 10*1024*1024   # log file size : 10MB

fileHandler = logging.handlers.RotatingFileHandler(
    #'C:/Users/tenspace/Desktop/crawlerBot_package_SCI/NotUsingJSONDATAType/log/' + hereWork + '_log_'
    r"C:\\dev_tenspace\\2019_python_project_syhan\\201901_python36\\crawlerBot_pack_SCI_2019\\crawlerbots\\log\\" + hereWork + "_log_"
    + currentTime, maxBytes=file_max_bytes, backupCount=10)

streamHandler = logging.StreamHandler()

# handler 에 formatter 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

# Handler 를 logging 에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

logging.debug(hereWork + '_crawlerbot_debugging on' + currentTime)
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')


def kakao_story_crawler_start(user_list, start_date, end_date):
    start_time_all = time.time()
    login_url = 'https://accounts.kakao.com/login/kakaostory'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    response = requests.get(login_url, headers=headers)
    print(response)

    print('Auto login start.')

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920x1080")

    # prefs = {}
    # prefs['profile.default_content_setting_values.notifications'] = 2
    # chrome_options.add_experimental_option('prefs', prefs)

    #driver = webdriver.Chrome(chrome_options=chrome_options)
    path = r"C:\dev_tenspace\2019_python_project_syhan\201901_python36\crawlerBot_pack_SCI_2019\chromedriver.exe"

    driver = webdriver.Chrome(options=chrome_options, executable_path=path)
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.info_user")))

    admin_email = 'kimtheho@hanmail.net'
    admin_password = '77882e2e'

    # 로그인
    driver.find_element_by_id('loginEmail').send_keys(admin_email)
    driver.find_element_by_id('loginPw').send_keys(admin_password)
    driver.find_element_by_class_name('btn_login').click()

    # click 후 화면 전환까지 시간이 필요하여
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.add_top")))

    user_info = {}

    for user in user_list:
        driver.get('https://story.kakao.com/' + user + '/profile')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.profile_collection ")))
        print('start :', driver.current_url)
        user_info['카카오스토리페이지ID'] = user
        user_info['이름'] = ''
        user_info['스토리'] = 0
        user_info['생일'] = ''
        user_info['학교'] = ''
        user_info['한줄소개'] = ''
        user_info['한줄음악'] = ''
        user_info['거주지'] = ''
        user_info['직장'] = ''
        user_info['성별'] = ''
        user_info['게시글'] = 0
        user_info['좋아요'] = 0
        user_info['댓글'] = 0
        user_info['공유'] = 0
        user_info['up'] = 0
        user_info['사진'] = 0
        user_info['동영상'] = 0
        user_info['장소'] = 0
        user_info['관심글'] = 0
        user_info['up한글'] = 0
        user_info['소식받는수'] = 0
        user_info['kk_TSCORE'] = 0
        user_info['kk_CSCORE'] = 0
        user_info['kk_MSCORE'] = 0
        try:
            # 페이지가 로딩된 다음 beautifulSoup을 이용하여 HTML 문서 값 가져옴.
            html_soup = BeautifulSoup(driver.page_source, 'html.parser')
            print('[ 기본 정보 ]')
            dl_list = html_soup.select('#myStoryContentWrap > div:nth-of-type(2) > div > '
                                       'div.profile_collection > div > div[data-part-name=profileView] > dl')
            # 기본 정보(이름, 생일, 성별, 뮤직, 직장정보, 거주지정보)
            # 아래의 영역 값들은 공개할 수도, 안할 수도 있는 것들임. 각각의 항목을 반드시 try except 로 묶어
            # Exception 에 의한 process 중단을 피해야 함.
            for i in range(len(dl_list)):
                try:
                    user_info_span_title = html_soup.select(
                        '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div > '
                        'dl:nth-of-type(' + str(i + 1) + ') > dt > span')[0].text.replace(" ", "")

                    user_info_dl_value = html_soup.select(
                        '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > '
                        'div[data-part-name=profileView] > dl:nth-of-type(' + str(i + 1) + ') > dd > div '
                    )[0].text.replace('\xa0', '').replace(' ', '')

                    user_info[user_info_span_title] = user_info_dl_value
                    print(user_info_span_title, ' : ', user_info[user_info_span_title])

                except Exception as e:
                    print('사용자가 정보를 더이상 공개하지 않았습니다. ->', e)
            info = html_soup.select('#myStoryContentWrap > div[data-module=myStoryWidget] > '
                                    'div.story_widgets > div[data-part-name=myInfo] > div > h3')[0].text
            # 정보(스토리 개수, 출신 학교)
            if info is not None:
                info_list = html_soup.select(
                    '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > '
                    'div[data-part-name=myInfo] > div > dl.list_info > dt')
                print('[ 정보 ]')
                for i in range(len(info_list)):

                    user_compct_info_title = html_soup.select(
                        '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > '
                        'div[data-part-name=myInfo] > div > dl.list_info > dt:nth-of-type('
                        + str(i + 1) + ') > span:nth-of-type(1)')[0].text.replace('\xa0', '').replace(' ', '')

                    user_compct_info_value = html_soup.select(
                        '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > '
                        'div[data-part-name=myInfo] > div > dl.list_info > dd:nth-of-type('
                        + str(i + 1) + ')')[0].text.replace('\xa0', '').replace(' ', '')

                    user_info[user_compct_info_title] = user_compct_info_value
                    print(user_compct_info_title, ':', user_info[user_compct_info_title])

        except Exception as e:
            logger.exception(msg=e)
            print('크롤링 대상이 없습니다.--> ', e)
        # 정보 제공량 별 점수 산출
        print()
        driver.get('https://story.kakao.com/' + user)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed")))

        post_soup = auto_scroll(driver)

        all_like_cnt = 0
        all_reply_cnt = 0
        all_share_cnt = 0
        all_place_cnt = 0
        all_up_cnt = 0

        post_wrapper = post_soup.select('div.feed > div > div')

        for i in range(len(post_wrapper)):
            post_list = post_soup.select('div.feed > div > div:nth-of-type(' + str(i+1) + ') > div > div > div')
            for j in range(len(post_list)):
                try:
                    post_like_cnt = 0
                    post_comment_cnt = 0
                    post_share_cnt = 0
                    # 날짜
                    post_date = post_soup.select('div.feed > div > div:nth-of-type('
                                                 + str(i + 1) + ') > div > div > div:nth-of-type('
                                                 + str(j + 1) + ') .add_top > p > a')
                    for a in post_date:
                        post_date = a['title']
                    post_date = post_date.replace('년', '-').replace('월', '-').replace("일", '').replace('오전', 'AM').\
                        replace('오후', 'PM').replace(' ', '')
                    post_date = datetime.strptime(post_date, '%Y-%m-%d%p%I:%M')
                    post_date = post_date.strftime('%Y-%m-%d')
                    # print('게시글 날짜 :', post_date)

                    # 본문
                    post_text = post_soup.select('div.feed > div > div:nth-of-type('
                                                 + str(i+1) + ') > div > div > div:nth-of-type('
                                                 + str(j+1) + ') .txt_wrap')[0].text
                    # print('본문 :', post_text)

                    # 장소
                    try:
                        post_place = post_soup.select('div.feed > div > div:nth-of-type('
                                                      + str(i+1) + ') > div > div > div:nth-of-type('
                                                      + str(j+1) + ') .place'
                                                      )[0].text.replace('에서', '').replace(' ', '')
                        if '님과함께' in post_place:
                            pass
                            # print('장소 : 없음')
                        else:
                            all_place_cnt += 1
                            # print('장소 :', post_place)
                    except IndexError:
                        pass
                        # print('장소 : 없음', e)

                    # 좋아요 수
                    try:
                        post_like_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                         + str(i + 1) + ') > div > div > div:nth-of-type('
                                                         + str(j + 1) + ') ._likeCount')[0].text.replace(',', '')
                        # print('좋아요 :', post_like_cnt)
                        all_like_cnt += int(post_like_cnt)
                    except IndexError:
                        # print('좋아요 없음', e)
                        pass

                    # 댓글 수
                    try:
                        post_comment_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                            + str(i + 1) + ') > div > div > div:nth-of-type('
                                                            + str(j + 1) + ') ._commentCount')[0].text.replace(',', '')
                        # print('댓글 :', post_comment_cnt)
                        all_reply_cnt += int(post_comment_cnt)
                    except IndexError:
                        pass
                        # print('댓글 없음', e)

                    # 공유 수
                    try:
                        post_share_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                          + str(i + 1) + ') > div > div > div:nth-of-type('
                                                          + str(j + 1) + ') ._storyShareCount')[0].text.replace(',', '')
                        # print('공유 :', post_share_cnt)
                        all_share_cnt += int(post_share_cnt)
                    except IndexError:
                        # print('공유 없음', e)
                        pass
                    #  up 수
                    try:
                        post_up_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                       + str(i + 1) + ') > div > div > div:nth-of-type('
                                                       + str(j + 1) + ') ._sympathyCount')[0].text.replace(',', '')
                        # print('up :', post_up_cnt)
                        all_up_cnt += int(post_up_cnt)
                    except IndexError:
                        # print('up 없음', e)
                        pass
                    # print()
                    if start_date <= post_date <= end_date:
                        db = db_mysql_connection_SCI.DatabaseConnection()
                        db.post_insert(
                            'kakaoStory',
                            user,
                            str(post_text),
                            str(post_like_cnt),
                            str(post_comment_cnt),
                            str(post_share_cnt),
                            post_date
                        )
                    else:
                        pass
                except Exception as e:
                    print('게시글 에러', e)
        print('총 좋아요 :', all_like_cnt)
        print('총 댓글 :', all_reply_cnt)
        print('총 공유 :', all_share_cnt)
        print('총 장소 :', all_place_cnt)
        print('총 up :', all_up_cnt)
        print()
        driver.get('https://story.kakao.com/' + user + '/photos')
        photo_soup = auto_scroll(driver)
        try:
            photo_cnt = int(len(photo_soup.select('._listContainer > div')))
            print('사진 수 :', photo_cnt)
            user_info['사진'] = photo_cnt
        except Exception as e:
            print('사진 없음', e)

        driver.get('https://story.kakao.com/' + user + '/videos')
        video_soup = auto_scroll(driver)
        try:
            video_cnt = int(len(video_soup.select('._listContainer > div')))
            print('동영상 수 :', video_cnt)
            user_info['동영상'] = video_cnt
        except Exception as e:
            print('동영상 없음', e)

        driver.get('https://story.kakao.com/' + user + '/locations')
        locations_soup = auto_scroll(driver)
        try:
            locations_cnt = int(len(locations_soup.select('._listContainer > div')))
            print('장소 수 :', locations_cnt)
            user_info['장소'] = locations_cnt
        except Exception as e:
            print('장소 없음', e)

        driver.get('https://story.kakao.com/' + user + '/favorites')
        favorites_soup = auto_scroll(driver)
        try:
            favorites_cnt = int(len(favorites_soup.select('._listContainer > div')))
            print('관심글 수 :', favorites_cnt)
            user_info['관심글'] = favorites_cnt
        except Exception as e:
            print('관심글 없음', e)

        driver.get('https://story.kakao.com/' + user + '/up')
        up_soup = auto_scroll(driver)
        try:
            up_cnt = int(len(up_soup.select('._listContainer > div')))
            print('up 한 글 수 :', up_cnt)
            user_info['up한글'] = up_cnt
        except Exception as e:
            print('up 한 글 없음', e)

        driver.get('https://story.kakao.com/' + user + '/following')
        up_soup = auto_scroll(driver)
        try:
            following_cnt = int(len(up_soup.select('._listContainer > li')))
            print('소식받는 수 :', following_cnt)
            user_info['소식받는수'] = following_cnt
        except Exception as e:
            print('소식 없음', e)

        '''
        returnListKakaoValue = [
        0   feeling_cnt,
        1   reply_cnt, 
        2   place_cnt, 
        3   video_cnt]
        '''

        generateNumKakaoResult = genN.GenNumEngine.getCntInfo_kakao(genN.GenNumEngine)

        kakao_story_t_value = 0
        kakao_story_c_value = 0
        kakao_story_m_value = 0
        print('[ 점수 ]')

        if '성별' in user_info:
            if user_info['성별'] == '남성':
                print('성별 남성 : 20점이 부여되었습니다.')
                kakao_story_t_value += 20

            elif user_info['성별'] == '여성':
                kakao_story_t_value += 10
                print('성별 여성 : 10점이 부여되었습니다.')
        else:
            print('성별이 공개되지 않았습니다.')

        if '한줄음악' in user_info:
            print('카카오 뮤직 공개 : 20점이 부여되었습니다.')
            kakao_story_c_value += 20
        else:
            print('카카오 뮤직 비공개 : 0점이 부여되었습니다.')

        if '거주지' in user_info:
            print('거주지 정보 공개')
            if '서울' in user_info['거주지']:
                print('거주지 정보- 서울 : 50점이 부여되었습니다.')
                kakao_story_t_value += 50
            elif '경기' in user_info['거주지']:
                print('거주지 정보- 경기 : 30점이 부여되었습니다.')
                kakao_story_t_value += 30
            else:
                print('거주지 정보- 비수도권 : 15점이 부여되었습니다.')
                kakao_story_t_value += 15
        else:
            print('거주지 정보 비공개')

        if '스토리' in user_info:
            print('게시 스토리 개수 공개')

            try:
                kstory_count_str = user_info['스토리'].split('개')[0]
                kstory_count_int = int(kstory_count_str.replace(",", ""))

                if kstory_count_int >= 200:
                    print('게시 스토리 개수 200개 이상')
                    kakao_story_m_value += 50
                elif kstory_count_int < 200:
                    print('게시 스토리 개수 200개 미만')
                    kakao_story_m_value += 30

            except Exception as ex:
                print('스토리 개수 표시가 \"~개\" 로 표시되어 있지 않습니다. 단순 숫자로 표시')
                if int(user_info['스토리']) >= 200:
                    print('게시 스토리 개수 200개 이상')
                    kakao_story_m_value += 50
                elif int(user_info['스토리']) < 200:
                    print('게시 스토리 개수 200개 미만')
                    kakao_story_m_value += 30
                    print(ex)
        else:
            print('게시 스토리 개수 비공개')

        if '학교' in user_info:
            univ_list = ['서울대학교', '중앙대학교', '덕성여자대학교', '건국대학교', '서울교육대학교', '홍익대학교',
                         '이화여자대학교', '서울시립대학교', '동국대학교', '서울여자대학교', '연세대학교', '명지대학교',
                         '숙명여학교', '고려대학교', '상명대학교', '동덕여자대학교', '서강대학교', '삼육대학교', '국민대학교',
                         '서울과학기술대학교', '한국체육대학교', '성신여자대학교', '한국외국어대학교', '숭실대학교', '총신대학교',
                         '세종대학교', '한국종합예술학교', '한성대학교', '서경대학교', '성공회대학교']

            user_edu_history = user_info['학교']
            if '학교' in user_edu_history:
                if user_edu_history in univ_list:
                    print('학력 정보- in 서울')
                    kakao_story_t_value += 50

                else:
                    print('학력 정보- not in 서울')
                    kakao_story_t_value += 30
        else:
            print('학력 정보 비공개')
            user_info['학교'] = ''

            user_info['kk_TSCORE'] = kakao_story_t_value
            user_info['kk_CSCORE'] = kakao_story_c_value
            user_info['kk_MSCORE'] = kakao_story_m_value
        print('[', user_info['이름'], '님의 카카오스토리 크롤링 결과', ']')
        print(user_info)

        # expressionEngine.py
        expressResultRate = exprs.ExpressionEngine.expressionFind(exprs.ExpressionEngine)
        print("expressResult :", expressResultRate)


        # DB insert
        try:
            # Server Connection to MySQL
            db = db_mysql_connection_SCI.DatabaseConnection()
            db.kakao_insert(
                'kakao',                                                         # platform
                user,                                                           # page_id
                str(user_info['이름']),                                           # username
                str(user_info['성별']),                                           # gender
                str(user_info['거주지']),                                         # address
                str(user_info['생일']),                                           # birthday
                str(user_info['직장']),                                           # company1
                str(user_info['학교']),                                           # university1
                'expression_negative',                                              # expression_negative
                'expression_positive',                                              # expression_positive
                str(user_info['소식받는수']),                                      # take_news
                str(user_info['관심글']),                                         # post_interest
                str(user_info['up한글']),                                         # post_up
                str(generateNumKakaoResult[0]),                                               # feeling_cnt
                str(generateNumKakaoResult[1]),                                              # reply_cnt
                str(all_share_cnt),                                              # share_cnt
                str(generateNumKakaoResult[2]),                                           # place_cnt
                str(all_place_cnt),                                              # place_add
                str(user_info['스토리'].replace(",", "").replace("개", "")),      # post_cnt
                str(user_info['사진']),                                           # photo_cnt
                str(generateNumKakaoResult[3]),                                         # video_cnt
                'NULL',                                                         # operation_year_period
                str(generateNumKakaoResult[4]),                                 # friends_continuous_exchange
                str(generateNumKakaoResult[5]),                                 # friends_rating_index
                'NULL',                                                         # friends_correlation_score
                'NULL'                                                          # contents_regular

            )
        except Exception as e_maria:
            logger.error(msg=e_maria)

    end_time = time.time() - start_time_all

    print()
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)


def auto_scroll(driver):

    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요

    # 20181016_edited_syhan
    global auto_scroll_data_soup_html

    # 화면 길이 만큼 나눠 auto_scroll 하고 각 페이지마다 데이터 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    auto_scroll_data = driver.page_source
    auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 4):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 2).until(lambda driver: driver.execute_script("return document.body.scrollHeight;") >
                                                          last_height)
        except Exception as e:
            print(e, 'autoScroll 0')
            auto_scroll_data = driver.page_source
            auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')
            return auto_scroll_data_soup_html

        # # Calculate new scroll height and compare with last scroll height
        # new_height = driver.execute_script("return document.body.scrollHeight")
        # last_height = new_height

    # auto_scroll crawling data 가져오기
    auto_scroll_data = driver.page_source
    auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')

    return auto_scroll_data_soup_html


def auto_scroll(driver):

    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요

    # 20181016_edited_syhan
    global auto_scroll_data_soup_html

    # 화면 길이 만큼 나눠 auto_scroll 하고 각 페이지마다 데이터 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    auto_scroll_data = driver.page_source
    auto_scroll_data_soup_html = BeautifulSoup(auto_scroll_data, 'html.parser')

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 4):
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
    user_list = ['maplekim', 'qubixx', '_0DMwY', 'ppang_madam', 'chezmoi_2013', 'editorh', 'sy_217', '_9Y2Ok3',
                 'pepper_salt', 'wlsgmldml', 'dippydro', 'glila', 'cookieontheroad', 'suheeryu', 'sobook', 'akdmf72',
                 'liliant', 'silverway', 'chezmoi_2013', 'lks1719', 'ateliersujin', 'jjaoyami', 'songah_jeju']
    start_date = '2017-01-01'
    end_date = '2018-01-01'
    kakao_story_crawler_start(user_list, start_date, end_date)
main()
