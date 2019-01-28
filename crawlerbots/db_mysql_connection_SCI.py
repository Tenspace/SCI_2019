import pymysql

class DatabaseConnection:
    def __init__(self):

        try:
            self.connection = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='1234',
                db='face',
                charset='utf8mb4')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            # print('DB connection completed')

        except Exception as e:
            print('Cannot connect to Database: ', e)

    # INSERT facebook
    def facebook_insert(self, platform, page_id, username, gender, phone_number, birthday, company1, company2, company3,
                        university1, university2, university3, address1, address2, address3, contact1, contact2,
                        expression_negative, expression_positive,
                        friends_all, friends_residence, friends_company, friends_univ, friends_highschool,
                        friends_native, follower_cnt, like_all_cnt, like_movie_cnt, like_tv_cnt, like_music_cnt,
                        like_book_cnt, like_sports_cnt, like_athlete_cnt, like_restaurant_cnt, like_appgame_cnt,
                        check_in, event, review, like_cnt, comment_cnt, share_cnt, place_add, post_cnt,
                        photo_of_oneself_cnt, photo_cnt, album_cnt, album_category_cnt, video_tag_oneself_cnt,
                        video_cnt, operation_year_period, friends_continuous_exchange, friends_rating_index,
                        friends_correlation_score, contents_regular):
        try:
            insert_command = """INSERT INTO crawler_score (
                             platform, page_id, username, gender, phone_number, birthday, address1, address2, address3,  
                             company1, company2, company3, university1, university2, university3, contact1, contact2,
                             expression_negative, expression_positive, friends_all, friends_residence,
                             friends_company, friends_univ, friends_highschool, friends_native, take_news,
                             post_interest, post_up, feeling_cnt, following_cnt, follower_cnt, like_all_cnt,
                             like_movie_cnt, like_tv_cnt, like_music_cnt, like_book_cnt, like_sports_cnt,
                             like_athlete_cnt, like_restaurant_cnt, like_appgame_cnt, check_in, event, review,
                             like_cnt ,comment_cnt, share_cnt, place_cnt, place_add, post_cnt,
                             photo_of_oneself_cnt, photo_cnt, album_cnt, album_category_cnt, video_tag_oneself_cnt,
                             video_cnt, operation_year_period, friends_continuous_exchange, friends_rating_index,
                             friends_correlation_score, contents_regular
                             ) VALUES (
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
            print('insert ok', insert_command)
            self.cursor.execute(insert_command, (platform, page_id, username, gender, phone_number, birthday, address1, address2,
                                                 address3, company1, company2, company3, university1, university2,
                                                 university3, contact1, contact2, expression_negative,
                                                 expression_positive, friends_all, friends_residence, friends_company,
                                                 friends_univ, friends_highschool, friends_native, None, None,
                                                 None, None, None, follower_cnt, like_all_cnt, like_movie_cnt,
                                                 like_tv_cnt, like_music_cnt, like_book_cnt, like_sports_cnt,
                                                 like_athlete_cnt, like_restaurant_cnt, like_appgame_cnt,
                                                 check_in, event, review, like_cnt, comment_cnt, share_cnt, None,
                                                 place_add, post_cnt, photo_of_oneself_cnt, photo_cnt, album_cnt,
                                                 album_category_cnt, video_tag_oneself_cnt, video_cnt,
                                                 operation_year_period, friends_continuous_exchange,
                                                 friends_rating_index, friends_correlation_score, contents_regular))
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print('db 에러', e)

    # INSERT kakao story
    def kakao_insert(self, platform, page_id, username, gender, address, birthday, company, university, expression_negative,
                     expression_positive, take_news, post_interest, post_up, feeling_cnt, comment_cnt, share_cnt,
                     place_cnt, place_add, post_cnt, photo_cnt, video_cnt, operation_year_period,
                     friends_continuous_exchange, friends_rating_index, friends_correlation_score, contents_regular):
        try:
            insert_command = """INSERT INTO crawler_score (
                             platform, page_id, username, gender, phone_number, birthday, address1, address2, address3,  
                             company1, company2, company3, university1, university2, university3, contact1, contact2,
                             expression_negative, expression_positive, friends_all, friends_residence,
                             friends_company, friends_univ, friends_highschool, friends_native, take_news,
                             post_interest, post_up, feeling_cnt, following_cnt, follower_cnt, like_all_cnt,
                             like_movie_cnt, like_tv_cnt, like_music_cnt, like_book_cnt, like_sports_cnt,
                             like_athlete_cnt, like_restaurant_cnt, like_appgame_cnt, check_in, event, review,
                             like_cnt ,comment_cnt, share_cnt, place_cnt, place_add, post_cnt,
                             photo_of_oneself_cnt, photo_cnt, album_cnt, album_category_cnt, video_tag_oneself_cnt,
                             video_cnt, operation_year_period, friends_continuous_exchange, friends_rating_index,
                             friends_correlation_score, contents_regular
                             ) VALUES (
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """

            print('insert ok', insert_command)
            self.cursor.execute(insert_command, (platform, page_id, username, gender, None, birthday, address, None,
                                                 None, company, None, None, university, None, None, None, None,
                                                 expression_negative, expression_positive, None, None, None, None, None,
                                                 None, take_news, post_interest, post_up, feeling_cnt, None, None, None,
                                                 None, None, None, None, None, None, None, None, None, None, None, None,
                                                 comment_cnt, share_cnt, place_cnt, place_add, post_cnt, None,
                                                 photo_cnt, None, None, None, video_cnt, operation_year_period,
                                                 friends_continuous_exchange, friends_rating_index,
                                                 friends_correlation_score, contents_regular))
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print('db 에러', e)

    def post_insert(self, platform, page_id, post_text, post_like, post_reply, post_share, post_date):
        try:
            insert_command = """INSERT INTO post (
                             platform, page_id, post_text, post_like, post_reply, post_share, post_date
                             ) VALUES(
                             %s, %s, %s, %s, %s, %s, %s)
                            """
            # print('insert ok', insert_command)
            self.cursor.execute(insert_command, (platform, page_id, post_text, post_like, post_reply, post_share, post_date))
            self.connection.commit()
            self.connection.close()

        except Exception as e:
            print('db 에러', e)





