import random

class GenNumEngine:

    #긍정, 부정 표현을 제외한 나머지 항목들의 값들에 대해 무작위 생성 함수를 만들고자 한다.
    #friends_residence
    #friends_company
    #friends_univ
    #friends_highschool
    #friends_native
    #feeling_cnt
    #like_all_cnt
    #like_movie_cnt
    #like_tv_cnt
    #like_music_cnt
    #like_book_cnt
    #like_sports_cnt
    #like_athlete_cnt
    #like_restaurant_cnt
    #like_appgame_cnt
    #check_in
    #event
    #review
    #reply_cnt
    #place_cnt
    #album_category_cnt
    #video_tag_oneself_cnt
    #video_cnt
    #operation_year_period

    def getCntInfo_kakao(self):

        feeling_cnt= random.randint(1, 500)
        reply_cnt= random.randint(1, 300)
        place_cnt= random.randint(1, 70)
        video_cnt= random.randint(1, 400)

        returnListKakaoValue = [feeling_cnt, reply_cnt, place_cnt, video_cnt]

        return returnListKakaoValue

    def getCntInfo_face(self):

        friends_residence = random.randint(1, 2000)
        friends_company= random.randint(1, 2000)
        friends_univ= random.randint(1, 2000)
        friends_highschool= random.randint(1, 2000)
        friends_native= random.randint(1, 2000)
        # feeling_cnt= random.randint(1, 500)
        like_all_cnt= random.randint(1, 400)
        like_movie_cnt= random.randint(1, 100)
        like_tv_cnt= random.randint(1, 50)
        like_music_cnt= random.randint(1, 50)
        like_book_cnt= random.randint(1, 40)
        like_sports_cnt= random.randint(1, 60)
        like_athlete_cnt= random.randint(1, 50)
        like_restaurant_cnt= random.randint(1, 30)
        like_appgame_cnt= random.randint(1, 40)
        check_in= random.randint(1, 20)
        event= random.randint(1, 10)
        review= random.randint(1, 40)
        # reply_cnt= random.randint(1, 300)
        # place_cnt= random.randint(1, 70)
        album_category_cnt= random.randint(1, 40)
        video_tag_oneself_cnt= random.randint(1, 80)
        # video_cnt= random.randint(1, 400)
        operation_year_period= random.randint(1, 10)

        returnListFaceValue = [friends_residence, friends_company, friends_univ, friends_highschool, friends_native, like_all_cnt,
                      like_movie_cnt, like_tv_cnt, like_music_cnt, like_book_cnt, like_sports_cnt, like_athlete_cnt, like_restaurant_cnt, like_appgame_cnt,
                      check_in, event, review, album_category_cnt, video_tag_oneself_cnt, operation_year_period]

        return returnListFaceValue
