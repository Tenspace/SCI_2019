import pymysql


def DatabaseConnection():
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='1234',
            db='aster',
            charset='utf8mb4')

        connection.autocommit = True
        cursor = connection.cursor()

    except Exception as e:
        print('Cannot connect to Database: ', e)

    try:
        insert_command = """SELECT * FROM search_log"""
        # print('insert ok', insert_command)
        cursor.execute(insert_command)
        connection.commit()
        connection.close()
        return cursor.fetchall()
    except Exception as e:
        print('db 에러', e)
    return cursor.fetchall()


