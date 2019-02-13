import pymysql

db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='1234',
    db='crawling',
    charset='utf8mb4')
print(db)
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
version = cursor.fetchall()
print(version)

sql = '''CREATE TABLE `crawler_score` (
        `no_index` INT(11) NOT NULL AUTO_INCREMENT,
        `insertedTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `origin_ph` VARCHAR(255) NULL DEFAULT NULL,
        `platform` VARCHAR(255) NULL DEFAULT NULL,
        `page_id` VARCHAR(255) NULL DEFAULT NULL,
        `username` VARCHAR(255) NULL DEFAULT NULL,
        `gender` VARCHAR(255) NULL DEFAULT NULL,
        `phone_number` VARCHAR(255) NULL DEFAULT NULL,
        `birthday` VARCHAR(255) NULL DEFAULT NULL,
        `address1` VARCHAR(255) NULL DEFAULT NULL,
        `address2` VARCHAR(255) NULL DEFAULT NULL,
        `address3` VARCHAR(255) NULL DEFAULT NULL,
        `company1` VARCHAR(255) NULL DEFAULT NULL,
        `company2` VARCHAR(255) NULL DEFAULT NULL,
        `company3` VARCHAR(255) NULL DEFAULT NULL,
        `university1` VARCHAR(255) NULL DEFAULT NULL,
        `university2` VARCHAR(255) NULL DEFAULT NULL,
        `university3` VARCHAR(255) NULL DEFAULT NULL,
        `contact1` VARCHAR(255) NULL DEFAULT NULL,
        `contact2` VARCHAR(255) NULL DEFAULT NULL,
        `expression_negative` VARCHAR(255) NULL DEFAULT NULL,
        `expression_positive` VARCHAR(255) NULL DEFAULT NULL,
        `friends_all` VARCHAR(255) NULL DEFAULT NULL,
        `friends_residence` VARCHAR(255) NULL DEFAULT NULL,
        `friends_company` VARCHAR(255) NULL DEFAULT NULL,
        `friends_univ` VARCHAR(255) NULL DEFAULT NULL,
        `friends_highschool` VARCHAR(255) NULL DEFAULT NULL,
        `friends_native` VARCHAR(255) NULL DEFAULT NULL,
        `take_news` VARCHAR(255) NULL DEFAULT NULL,
        `post_interest` VARCHAR(255) NULL DEFAULT NULL,
        `post_up` VARCHAR(255) NULL DEFAULT NULL,
        `feeling_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `following_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `follower_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_all_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_movie_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_tv_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_music_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_book_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_sports_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_athlete_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_restaurant_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `like_appgame_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `check_in` VARCHAR(255) NULL DEFAULT NULL,
        `event` VARCHAR(255) NULL DEFAULT NULL,
        `review` VARCHAR(255) NULL DEFAULT NULL,
        `like_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `comment_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `share_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `place_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `place_add` VARCHAR(255) NULL DEFAULT NULL,
        `post_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `photo_of_oneself_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `photo_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `album_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `album_category_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `video_tag_oneself_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `video_cnt` VARCHAR(255) NULL DEFAULT NULL,
        `operation_year_period` VARCHAR(255) NULL DEFAULT NULL,
        `friends_continuous_exchange` VARCHAR(255) NULL DEFAULT NULL,
        `friends_rating_index` VARCHAR(255) NULL DEFAULT NULL,
        `friends_correlation_score` VARCHAR(255) NULL DEFAULT NULL,
        `contents_regular` VARCHAR(255) NULL DEFAULT NULL,
        PRIMARY KEY (`no_index`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;'''

sql2 = '''CREATE TABLE `post` (
        `no_index` INT(11) NOT NULL AUTO_INCREMENT,
        `insertedTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `origin_ph` VARCHAR(255) NULL DEFAULT NULL,
        `platform` VARCHAR(255) NULL DEFAULT NULL,
        `page_id` VARCHAR(255) NULL DEFAULT NULL,
        `post_text` VARCHAR(255) NULL DEFAULT NULL,
        `post_like` VARCHAR(255) NULL DEFAULT NULL,
        `post_reply` VARCHAR(255) NULL DEFAULT NULL,
        `post_share` VARCHAR(255) NULL DEFAULT NULL,
        `post_date` DATE NULL DEFAULT NULL,
        PRIMARY KEY (`no_index`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;'''

cursor.execute(sql)
cursor.execute(sql2)

















# a = '댓글 23개공유 2회'
# print(a.split(" ")[1].split('개')[0])
#
# a = 'profile.php?id=100005615048302'
# print(a.split("=")[1])

# a = '좋아요'
# print(a.split(" ")[1])
# sql = '''CREATE TABLE `post` (
#         `no_index` INT(11) NOT NULL AUTO_INCREMENT,
#         `insertedTime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#         `facebookUrl` VARCHAR(50) NULL DEFAULT '',
#         `post_date` DATE NULL DEFAULT NULL,
#         `post_text` VARCHAR(200) NULL DEFAULT '',
#         `post_like` VARCHAR(50) NULL DEFAULT '',
#         `post_reply` VARCHAR(200) NULL DEFAULT '',
#         PRIMARY KEY (`no_index`)
#     ) ENGINE=InnoDB DEFAULT CHARSET=utf8
#     ;'''
# cursor.execute(sql)
#
# import datetime
# import time
# from datetime import datetime
# updatedTime = '1월 2일 오후 11:17'
# 1. 7시간 (게시물 올린지 24시간 지나지 않았으면)
# 2. 어제 오전 11: 22 (게시물 올린지 24시간이 지났으면)
# 3. 1월 2일 오후 11:17 (현재 월에 올린 게시글)
# 4. 2018년 12월 31일 오후 9:30 (현재 년도가 아니면서 한달이내 게시글)
# 5. 2018년 11월 23일 (현재 년도가 아닌 년도에 올린 게시글)
#
# if '년' not in updatedTime:
#     current_time = str(datetime.now())[:10]
#     if '시간' in updatedTime:
#         print('게시물 올린 날짜 :', updatedTime, '전')
#         print('현재 날짜 :', current_time, datetime.now().hour)
#         post_hour = updatedTime.replace('시간', '')
#         current_hour = datetime.now().hour
#         hour = int(current_hour) - int(post_hour)
#         hour_str = str(hour)
#         if hour_str[0] == '-':
#             insert_time = current_time.replace(current_time[9], str(int(current_time[9]) - 1))
#             print('1.', insert_time)
#         else:
#             insert_time = current_time
#             print('1-2.', insert_time)
#     elif '어제' in updatedTime:
#         insert_time = current_time.replace(current_time[9], str(int(current_time[9]) - 1))
#         print('2.', insert_time)
#     else:
#
#         print('3.', updatedTime)
# else:
#     if '오전' in updatedTime:
#         print('4.', updatedTime)
#     elif '오후' in updatedTime:
#         print('4-2.', updatedTime)
#     else:
# #         print('5.', updatedTime)
# a=[1, 2]
# b=len(a)
# print(b)
# c=range(b)
# print(c)
# for i in c:
#     print('a')

# # INSERT kakao story
# def kakao_insert(self, platform, name, gender, address, birthday, company, university, expression_negative,
#                  expression_positive, take_news, post_interest, post_up, feeling_cnt, comment_cnt, share_cnt,
#                  place_cnt, place_add, post_cnt, photo_cnt, video_cnt, operation_year_period,
#                  friends_continuous_exchange, friends_rating_index, friends_correlation_score, contents_regular):
#     try:
#         # 50개
#         insert_command = """INSERT INTO crawler_score (
#                          platform, name, gender, phone_number, address, birthday, company, university,
#                          expression_negative, expression_positive, friends_all, friends_residence,
#                          friends_company, friends_univ, friends_highschool, friends_native, take_news,
#                          post_interest, post_up, feeling_cnt, following_cnt, follower_cnt, like_all_cnt,
#                          like_movie_cnt, like_tv_cnt, like_music_cnt, like_book_cnt, like_sports_cnt,
#                          like_ahtlete_cnt, like_restaurant_cnt, like_appgame_cnt, check_in, event, review,
#                          like_cnt ,comment_cnt, share_cnt, place_cnt, place_add, post_cnt,
#                          photo_of_oneself_cnt, photo_cnt, album_cnt, album_category_cnt, video_tag_oneself_cnt,
#                          video_cnt, operation_year_period, friends_continuous_exchange, friends_rating_index,
#                          friends_correlation_score, contents_regular
#                          ) VALUES (
#                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                         """
#         print('insert ok', insert_command)
#         self.cursor.execute(insert_command, (platform, name, gender, 'NULL', address, birthday, company, university,
#                                              expression_negative, expression_positive, 'NULL', 'NULL',
#                                              'NULL', 'NULL', 'NULL', 'NULL', take_news,
#                                              post_interest, post_up, feeling_cnt, 'NULL', 'NULL', 'NULL',
#                                              'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
#                                              'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL',
#                                              'NULL', comment_cnt, share_cnt, place_cnt, place_add, post_cnt,
#                                              'NULL', photo_cnt, 'NULL', 'NULL', 'NULL',
#                                              video_cnt, operation_year_period, friends_continuous_exchange,
#                                              friends_rating_index, friends_correlation_score, contents_regular))
#         self.connection.commit()
#         self.connection.close()
#
#     except Exception as e:
#         print('db 에러', e)