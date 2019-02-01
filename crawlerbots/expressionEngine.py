# -*-coding:utf-8-*-
import random
import json
import time


class ExpressionEngine:

    def expressionFind(self):

        print("Direction\n -30:매우 부정, -15:부정, 7:중립 or Unknown, 15:긍정, 30:매우 긍정\n 사전에 단어가 없는 경우 또는 중립적인 표현인 경우 Unknown\n")
        wordName = open('data/positivenegativewords.txt', encoding='utf-8-sig', mode='r')

        wordList = []
        for line in wordName.readlines():
            wordList.append(line.replace("\n", ""))

        # 만들어진 wordlist에서 100개의 단어를 random choice 하고 100개의 단어로 만들어진 리스트에서
        # 긍정어, 부정어 비율을 찾아 비율 값을 return
        # len(wordList) #9348
        cntr = 1
        snd_wordList = []
        while cntr <= 100:
            snd_wordList.append(random.choice(wordList))
            cntr += 1
        # second word list size: len(snd_wordList) #100
        # matching with json data and score on each word
        expressionRateResult = self.data_list(self, snd_wordList)

        if expressionRateResult != "None":
            return expressionRateResult
        else:
            return None

    def data_list(self, newWordList):

        with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
            data = json.load(f)
        result = ['None', 'None']

        for i in range(0, len(data)):
            if data[i]['word'] in newWordList:
                result.append(data[i]['word'])
                result.append(data[i]['polarity'])

                key_word = result[0]
                polar_word = result[1]

        #print(result)

        if polar_word == 'None':
            polar_word = '7'

        print("result:", result)
        if key_word != "None":
            print('key_word : ' + key_word)
            print('polar_word : ' + polar_word)
            print("\n")

        else:
            # if polarity is None, give 7
            polar_word = '7'
            print('root_word : ' + key_word)
            print('polar_word : ' + polar_word)

        # calculate expressionRateResult
        # 100개의 단어 중 polarity 7의 개수/ 15의 개수 / 30의 개수

        print('7-count:', result.count('7'))

        if result.count('7') >= 70:
            negative_exp_rate = random.randint(41, 58)
            positive_exp_rate = 100 - negative_exp_rate
            return negative_exp_rate, positive_exp_rate
        elif result.count('7') < 70 and result.count('15') >= 20:
            if result.count('-15') >= 20:
                negative_exp_rate = random.randint(60, 83)
                positive_exp_rate = 100 - negative_exp_rate
                return negative_exp_rate, positive_exp_rate
            else:
                positive_exp_rate = random.randint(60, 83)
                negative_exp_rate = 100 - positive_exp_rate
                return negative_exp_rate, positive_exp_rate
        elif result.count('7') < 70 and result.count('15') < 20 and result.count('30') >= 8:
            if result.count('-30') >= 8:
                negative_exp_rate = random.randint(85, 100)
                positive_exp_rate = 100 - negative_exp_rate
                return negative_exp_rate, positive_exp_rate
            else:
                positive_exp_rate = random.randint(85, 100)
                negative_exp_rate = 100 - positive_exp_rate
                return negative_exp_rate, positive_exp_rate
        else:
            positive_exp_rate = 50
            negative_exp_rate = 100 - positive_exp_rate
            return negative_exp_rate, positive_exp_rate







# For TEST
# if __name__ == "__main__":
#     ksl = ExpressionEngine()
#     ksl.expressionFind()
