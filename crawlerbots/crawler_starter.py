from crawlerbots.kakaostoryCrawlerBot import main as kksMain
from crawlerbots.facebookCrawlerBot import main as fbMain
from crawlerbots.instagramCrawlerBot import main as instaMain
from crawlerbots.db_mysql_select import DatabaseConnection

page = DatabaseConnection()

kakaoStroy_list = []
origin_ph_list = []
origin_name_list = []
start_list = []
end_list = []

for i in page:
    origin_ph_list.append(i[1])
    origin_name_list.append(i[15])
    kakaoStroy_list.append(i[6])
    start_list.append(i[26])
    end_list.append(i[27])

kksMain(kakaoStroy_list, origin_ph_list, origin_name_list, start_list, end_list)
