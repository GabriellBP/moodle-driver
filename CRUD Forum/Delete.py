import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='test',
)

try:
    with connection.cursor() as cursor:
        sql = "DELETE FROM todos WHERE id = %s"
        try:
            cursor.execute(sql, (1,))
            print("Successfully Deleted...")
        except:
            print("Oops! Something wrong")

    connection.commit()
finally:
    connection.close()
