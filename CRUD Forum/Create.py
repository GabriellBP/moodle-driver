import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='test',
)

title = input("Enter title of your task: ")
desc = input("Add some description to it: ")
date = input("Enter the date for this task (YYYY-MM-DD): ")

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO todos (`title`, `desc`, `date`) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (title, desc, date))
            print("Task added successfully")
        except:
            print("Oops! Something wrong")

    connection.commit()
finally:
    connection.close()


