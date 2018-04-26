import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='test',
)

try:
    with connection.cursor() as cursor:
        sql = "UPDATE todos SET `title`=%s, `desc`=%s WHERE `id` = %s"
        try:
            cursor.execute(sql, ('new title', 'new description', 1))
            print("Successfully Updated...")
        except:
            print("Oops! Something wrong")

    connection.commit()
finally:
    connection.close()