import crawlerBot_pack_SCI_2019.crawlerbots.expressionEngine as exprs
import crawlerBot_pack_SCI_2019.crawlerbots.generateNumEngine as gen

# expressionEngine.py
# expressResult = exprs.ExpressionEngine.expressionFind(exprs.ExpressionEngine)
# print("expressResult :", expressResult)


# generateNumEngine.py
generateNumKakaoResult = gen.GenNumEngine.getCntInfo_kakao(gen.GenNumEngine)
print(generateNumKakaoResult)

generateNumFaceResult = gen.GenNumEngine.getCntInfo_face(gen.GenNumEngine)
print(generateNumFaceResult)