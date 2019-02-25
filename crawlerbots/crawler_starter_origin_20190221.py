from crawlerbots.facebookCrawlerBot import main as fbMain
# from crawlerbots.kakaostoryCrawlerBot import main as kksMain
# from crawlerbots.instagramCrawlerBot import main as instaMain
from crawlerbots.db_mysql_select import DatabaseConnection
from self import self

page = DatabaseConnection()
facebook_list = []
kakaoStroy_list = []
origin_ph_list = []
origin_name_list = []
for i in page:
    origin_ph_list.append(i[1])
    origin_name_list.append(i[15])
    # facebook_list.append(i[9])
    kakaoStroy_list.append(i[6])

fbMain(facebook_list, origin_ph_list, origin_name_list)