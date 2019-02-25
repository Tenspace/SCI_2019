# -*- coding: utf-8 -*-
import logging.handlers
import time
from datetime import datetime
from crawlerbots import expressionEngine as exprs
from crawlerbots import db_mysql_connection_SCI
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
    'C:/Users/tenspace/Desktop/crawlerBot_package_SCI/NotUsingJSONDATAType/log/' + hereWork + '_log_'
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


def kakao_story_crawler_start(user_list, start_date, end_date, origin_ph, origin_name):
    start_time_all = time.time()
    login_url = 'https://accounts.kakao.com/login/kakaostory'

    print('Auto login start.')

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920x1080")

    # prefs = {}
    # prefs['profile.default_content_setting_values.notifications'] = 2
    # chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)
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

    for idx, user in enumerate(user_list):
        if idx > 11301 and idx < 14301:
            r = open('kakaoStory_user.txt', mode='rt', encoding='utf-8')
            user_txt = r.read()
            r.close()
            # 1. 90라인  : search_log 테이블에 카카오스토리 주소가 있으면 크롤링함
            # 2. 92라인  : txt 파일에 똑같은 주소가 없으면 크롤링함 (크롤링 후 kakaoStory_user.txt 에 주소를 기입함)
            # 3. 124라인 : search_log 테이블에 real_name 필드이름과 카카오스토리 이름이 같으면 크롤링함 똑같지 않으면 mismatch 테이블에 insert
            if user is not None and user != '':
                user = user.replace('https://story.kakao.com/', '')
                if '_' + user + '_' not in user_txt:
                    try:
                        start_time_all = time.time(                                            )
                        driver.get('https://story.kakao.com/' + user + '/profile')
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.profile_collection ")))
                        print('start :', driver.current_url)
                        user_info['카카오스토리페이지ID'] = user
                        user_info['이름'] = ''
                        user_info['스토리'] = 0
                        user_info['생일'] = ''
                        user_info['학교'] = ''
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
                        kakao_name = driver.find_element_by_css_selector('._profileName').text
                        print(origin_name[idx], ':', kakao_name)
                        if origin_name[idx] == kakao_name:
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

                            post_like_cnt = 0
                            post_comment_cnt = 0
                            post_share_cnt = 0
                            post_up_cnt = 0

                            post_date_cnt = 0
                            regular = 0
                            rating = 0

                            post_wrapper = post_soup.select('div.feed > div > div')

                            for i in range(len(post_wrapper)):
                                post_list = post_soup.select('div.feed > div > div:nth-of-type(' + str(i+1) + ') > div > div > div')
                                for j in range(len(post_list)):
                                    try:
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
                                        except IndexError:
                                            pass

                                        # 좋아요 수
                                        try:
                                            post_like_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                                             + str(i + 1) + ') > div > div > div:nth-of-type('
                                                                             + str(j + 1) + ') ._likeCount')[0].text.replace(',', '')
                                            post_like_cnt = int(post_like_cnt)
                                            all_like_cnt += post_like_cnt
                                        except IndexError:
                                            pass

                                        # 댓글 수
                                        try:
                                            post_comment_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                                                + str(i + 1) + ') > div > div > div:nth-of-type('
                                                                                + str(j + 1) + ') ._commentCount')[0].text.replace(',', '')
                                            post_comment_cnt = int(post_comment_cnt)
                                            all_reply_cnt += post_comment_cnt
                                        except IndexError:
                                            pass

                                        # 공유 수
                                        try:
                                            post_share_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                                              + str(i + 1) + ') > div > div > div:nth-of-type('
                                                                              + str(j + 1) + ') ._storyShareCount')[0].text.replace(',', '')
                                            post_share_cnt = int(post_share_cnt)
                                            all_share_cnt += post_share_cnt
                                        except IndexError:
                                            pass
                                        #  up 수
                                        try:
                                            post_up_cnt = post_soup.select('div.feed > div > div:nth-of-type('
                                                                           + str(i + 1) + ') > div > div > div:nth-of-type('
                                                                           + str(j + 1) + ') ._sympathyCount')[0].text.replace(',', '')
                                            post_up_cnt = int(post_up_cnt)
                                            all_up_cnt += post_up_cnt
                                        except IndexError:
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
                                        if str(start_date[idx]) <= post_date <= str(end_date[idx]):
                                            db = db_mysql_connection_SCI.DatabaseConnection()
                                            db.post_insert(
                                                str(origin_ph[idx]),
                                                'kakaoStory',
                                                str(user),
                                                str(post_text),
                                                post_like_cnt,
                                                post_comment_cnt,
                                                post_share_cnt,
                                                post_up_cnt,
                                                str(post_date)
                                            )
                                        else:
                                            pass
                                    except Exception as e:
                                        print('게시글 에러', e)

                            rating = all_like_cnt + all_reply_cnt + all_share_cnt
                            try:
                                regular = user_info['스토리'] // all_reply_cnt
                            except Exception as e:
                                regular = 0

                            user_info['컨텐츠관리일정성'] = post_date_cnt
                            user_info['지속적교류'] = regular
                            user_info['평가지수'] = rating

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

                            print('[', user_info['이름'], '님의 카카오스토리 크롤링 결과', ']')
                            print(user_info)

                            expressRateResult = exprs.ExpressionEngine.expressionFind(exprs.ExpressionEngine)
                            print("expressResult :", expressRateResult)

                            post_cnt = int(user_info['스토리'].replace(",", "").replace("개", ""))

                            # DB insert
                            try:
                                # Server Connection to MySQL
                                db = db_mysql_connection_SCI.DatabaseConnection()
                                db.kakao_insert(
                                    str(origin_ph[idx]),                                                     # origin_ph
                                    'kakao',                                                         # platform
                                    user,                                                           # page_id
                                    str(user_info['이름']),                                           # username
                                    str(user_info['성별']),                                           # gender
                                    str(user_info['거주지']),                                         # address
                                    str(user_info['생일']),                                           # birthday
                                    str(user_info['직장']),                                           # company1
                                    str(user_info['학교']),                                           # university1
                                    expressRateResult[0],
                                    expressRateResult[1],
                                    user_info['소식받는수'],                                      # take_news
                                    user_info['관심글'],                                         # post_interest
                                    user_info['up한글'],                                         # post_up
                                    all_like_cnt,                                               # feeling_cnt
                                    all_reply_cnt,                                              # comment_cnt
                                    all_share_cnt,                                              # share_cnt
                                    user_info['장소'],                                           # place_cnt
                                    all_place_cnt,                                              # place_add
                                    post_cnt,                                                   # post_cnt
                                    user_info['사진'],                                           # photo_cnt
                                    user_info['동영상'],                                         # video_cnt
                                    user_info['컨텐츠관리일정성'],
                                    user_info['지속적교류'],
                                    user_info['평가지수']
                                )
                            except Exception as e_maria:
                                logger.error(msg=e_maria)
                            f = open('kakaoStory_user.txt', mode='at', encoding='utf-8')
                            f.write('_' + user + '_\n')
                            f.close()
                            end_time = time.time() - start_time_all
                            print('크롤링 시간 :', end_time)
                        else:
                            print('origin name, kakao name 불일치')
                            try:
                                # Server Connection to MySQL
                                db = db_mysql_connection_SCI.DatabaseConnection()
                                db.mismatch(
                                    str(origin_ph[idx]),                                 # origin_ph
                                    'kakao',                                             # platform
                                    str(origin_name[idx]),                          # origin_name
                                    str(kakao_name),                                           # platform_name
                                    str(user),                                           # url
                                )
                            except Exception as e_maria:
                                logger.error(msg=e_maria)
                    except Exception as e:
                        print('에러', e)
                else:
                    print(user + ' : 이미 크롤링 한 데이터')
            else:
                print('카카오스토리 계정 없음')
        else:
            print('설정한 인덱스가 아님')
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


def main(user_list, origin_ph_list, origin_name_list, start_date, end_date):
    kakao_story_crawler_start(user_list, start_date, end_date, origin_ph_list, origin_name_list)

