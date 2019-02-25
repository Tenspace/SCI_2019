import csv
import logging
import pymysql

class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='uml.kr',
                port=3366,
                user='aster_dba',
                password='!aster716811',
                db='aster',
                charset='utf8mb4')

            # self.connection = pymysql.connect(
            #     host='127.0.0.1',
            #     port=3306,
            #     user='root',
            #     password='1234',
            #     db='aster',
            #     charset='utf8mb4')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            print('DB connection completed')

        except Exception as e:
            print('Cannot connect to Database: ', e)

    def insert(self, cell, name, startDate):

        print(cell, name, startDate)
        insert_sql = 'INSERT INTO compareDate_test(user_cell, user_name, user_loan_startdate)' \
                     'VALUES("' + cell + '","' + name + '","' + startDate + '");'
        print(insert_sql)

        self.cursor.execute(insert_sql)

        self.connection.commit()
        self.connection.close()


class CompareDate:
    def main(self):

        logging.basicConfig(filename=r'log\compareDateDate4.log', level=logging.DEBUG)

        path = r'C:\dev_tenspace\docs\hanacapital_users_201902.csv'

        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    #print(f'Column names are {", ".join(row)}')
                    logging.debug('Column names are '.format({", ".join(row)}))
                    line_count += 1
                else:
                    logging.debug('{}\t{}\t{}'.format(row[3], row[2], row[1]))

                    if row[3] is '':
                        row[3] = 'NULL'

                    if row[2] is '':
                        row[2] = 'NULL'

                    if row[1] is '':
                        row[1] = 'NULL'

                    DatabaseConnection().insert(row[3], row[2], row[1])
                    line_count += 1

        #OCCRD_YMD

if __name__ == '__main__':
    c = CompareDate()
    c.main()
