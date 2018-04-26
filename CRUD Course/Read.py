import pymysql
import sys


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='moodle',
)


def main(argv):
    ''' tabela curso geral '''
    mdl_course()


# Central course table
def mdl_course():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `category`, `fullname`, `shortname`, `idnumber`, `summary`, `summaryformat`, `format`, `visible` FROM mdl_course"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tCategory: " + str(row[1]) + "\tIdNumber: " + str(row[4]) +
                          "\tSummaryformat: " + str(row[6]) + "\tFormat: " + row[7] + "\tVisible: " + str(row[8]) +
                          "\nShortName: " + str(row[3]) + "\nFullName: \n" + str(row[2]) + "\nSummary: \n" + str(row[5]))
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    main(sys.argv)
