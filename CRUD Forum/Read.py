import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='moodle',
)

try:
    with connection.cursor() as cursor:
        sql = "SELECT `id`, `course`, `type`, `name`, `intro`, `introformat`, `maxattachments`  FROM mdl_forum"
        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            print("Id\t\t Curso \t\t Tipo \t\t Nome \t\t Descrição \t\t\t\t\t\t\t Tipo da descrição \t\t Máximo de Anexos")
            print("---------------------------------------------------------------------------------------------------")
            for row in result:
                print(str(row[0]) + "\t\t" + str(row[1]) + "\t\t" + row[2] + "\t\t" + row[3] + "\t\t" + row[4] + "\t\t" + str(row[5]) + "\t\t" + str(row[6]))
                # print(str(row[0]) + "\t\t" + str(row[1]))
        except:
            print("Oops! Something wrong")

    connection.commit()
finally:
    connection.close()