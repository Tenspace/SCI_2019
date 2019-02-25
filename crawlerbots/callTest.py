# import crawlerBot_pack_SCI_2019.crawlerbots.expressionEngine as exprs
# import crawlerBot_pack_SCI_2019.crawlerbots.generateNumEngine as gen
from crawlerbots import registeredRecorduser as userlist
# expressionEngine.py
# expressRateResult = exprs.ExpressionEngine.expressionFind(exprs.ExpressionEngine)
# print("expressResult :", expressRateResult)

# generateNumEngine.py
# generateNumKakaoResult = gen.GenNumEngine.getCntInfo_kakao(gen.GenNumEngine)
# print(generateNumKakaoResult)
#
# generateNumFaceResult = gen.GenNumEngine.getCntInfo_face(gen.GenNumEngine)
# print(generateNumFaceResult)
#
# generateNumInstaResult = gen.GenNumEngine.getCntInfo_instagram(gen.GenNumEngine)
# print(generateNumInstaResult)

from crawlerbots.registeredRecorduser import RegRecorduser

regUser = RegRecorduser()

user_list = regUser.call_userlist_insta()
print(user_list)


# from crawlerBot_pack_SCI_2019.crawlerbots.registeredRecorduser import RegRecorduser
# regUser = RegRecorduser()
#
# returnedVal = regUser.load_words()
# print(returnedVal)



#
# from crawlerBot_pack_SCI_2019.crawlerbots.selectDatedata import SelectDateData
#
# se = SelectDateData().selctDate()
# # start_date = '2017-01-01'
# start_date = se[0]
# end_date = se[1]
# print(start_date, end_date)


# from crawlerBot_pack_SCI_2019.crawlerbots.facebookCrawlerBot import main as fbMain
#
# fbMain()
