import random

class GenNumEngine:

    def getCntInfo_kakao(self):

        feeling_cnt = random.randint(1, 500)
        reply_cnt = random.randint(1, 300)
        place_cnt = random.randint(1, 70)
        video_cnt = random.randint(1, 400)
        friends_continuous_exchange = random.randint(1, 100)
        friends_rating_index = random.randint(1, 100)

        returnListKakaoValue = [feeling_cnt, reply_cnt, place_cnt, video_cnt, friends_continuous_exchange,
                                friends_rating_index]

        return returnListKakaoValue

    def getCntInfo_face(self, friends_cnt, post_cnt):
        try:
            friends_residence = random.randint(0, friends_cnt//5)
        except Exception as e:
            friends_residence = 0
        try:
            friends_company = random.randint(0, friends_cnt//5)
        except Exception as e:
            friends_company = 0
        try:
            friends_univ = random.randint(0, friends_cnt//5)
        except Exception as e:
            friends_univ = 0
        try:
            friends_highschool = random.randint(0, friends_cnt//5)
        except Exception as e:
            friends_highschool = 0
        try:
            friends_native = random.randint(0, friends_cnt//2)
        except Exception as e:
            friends_native = 0
        album_category_cnt = random.randint(1, 10)
        try:
            video_tag_oneself_cnt = random.randint(0, post_cnt//5)
        except Exception as e:
            video_tag_oneself_cnt = 0
        operation_year_period = random.randint(1, 10)

        returnListFaceValue = [friends_residence, friends_company, friends_univ, friends_highschool, friends_native,
                               album_category_cnt, video_tag_oneself_cnt, operation_year_period]

        return returnListFaceValue

    def getCntInfo_instagram(self):
        following_cnt = random.randint(1,500)
        follower_cnt = random.randint(1, 500)
        like_cnt = random.randint(1, 400)
        comment_cnt = random.randint(1, 500)
        share_cnt = random.randint(1, 500)
        place_add = random.randint(1, 250)
        post_cnt = random.randint(1, 400)
        photo_cnt = random.randint(1, 400)
        friends_continuous_exchange = random.randint(1, 100)
        friends_rating_index = random.randint(1, 100)
        contents_regular = random.randint(1, 100)
        video_cnt = random.randint(1, 400)

        returnListInstaValue = [following_cnt, follower_cnt, like_cnt, comment_cnt, share_cnt, place_add, post_cnt,
                                photo_cnt, friends_continuous_exchange, friends_rating_index, contents_regular, video_cnt]

        return returnListInstaValue
