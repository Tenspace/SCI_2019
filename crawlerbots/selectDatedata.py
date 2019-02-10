import random

class SelectDateData:

    def selctDate(self):
        yr1 = random.randint(2008, 2018)
        yr2 = random.randint(2008, 2018)
        if yr1 <= yr2:
            yr11 = yr1
            yr22 = yr2
        else:
            yr11 = yr2
            yr22 = yr1

        mnth = random.randint(1, 12)

        if mnth == 2:
            day1 = random.randint(1, 28)
            #day2 = random.randint(1, 30)
            if day1 is not 1:
                day2 = day1 - 1
            else:
                day1 = 2
                day2 = day1 - 1
            # day2 = random.randint(1, 28)
            #
            # if day1 == day2:
            #     day11 = day1
            #     day22 = day1 - 1
            # elif day1 > day2:
            #     day11 = day1
            #     day22 = day1 - 1
            # else:
            #     day11 = day2
            #     day22 = day2 - 1

        elif mnth in [1, 3, 5, 7, 8, 10, 12]:
            day1 = random.randint(1, 31)
            #day2 = random.randint(1, 30)
            if day1 is not 1:
                day2 = day1 - 1
            else:
                day1 = 2
                day2 = day1 - 1
            # day2 = random.randint(1, 31)
            #
            # if day1 == day2:
            #     day11 = day1
            #     day22 = day1 - 1
            # elif day1 > day2:
            #     day11 = day1
            #     day22 = day1 - 1
            # else:
            #     day11 = day2
            #     day22 = day2 - 1
        elif mnth in [4, 6, 9, 11]:
            day1 = random.randint(1, 30)
            #day2 = random.randint(1, 30)
            if day1 is not 1:
                day2 = day1 - 1
            else:
                day1 = 2
                day2 = day1 - 1
            #
            # if day1 == day2:
            #     day11 = day1
            #     day22 = day1 - 1
            # elif day1 > day2:
            #     day11 = day1
            #     day22 = day1 - 1
            # else: #day1 < day2
            #     day11 = day2
            #     day22 = day2 - 1

        return str(yr11)+'-'+str("{0:0=2d}".format(mnth))+'-'+str("{0:0=2d}".format(day1)), str(yr22)+'-'+str("{0:0=2d}".format(mnth))+'-'+str("{0:0=2d}".format(day2))