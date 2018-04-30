import pymysql
import sys


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='moodle',
)


def main(argv):
    ''' tabela categorias geral '''
    mdl_course_categories()
    ''' tabela curso geral '''
    mdl_course()
    ''' tabela das seções de cada curso '''
    mdl_course_sections


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


# Course categories
def mdl_course_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `name`, `idnumber`, `description`, `descriptionformat`, `parent`, `visible` FROM mdl_course_categories"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tIdNumber: " + str(row[2]) + "\tDescriptionFormat: " + str(row[4]) +
                          "\tParent: " + str(row[5]) + "\tVisible: " + str(row[6]) + "\nName: " + str(row[1]) +
                          "\nDescription: \n" + str(row[3]))
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


# To define the sections for each courses
def mdl_course_sections():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `course`, `section`, `name`, `summary`, `summaryformat`, `sequence`, `visible`, availability FROM mdl_course_sections"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tCourse: " + str(row[1]) + "\tSection: " + str(row[2]) +
                          "\tSummaryFormat: " + str(row[5]) + "\tAvailability: " + str(row[8]) +
                          "\tVisible: " + str(row[7]) + "\nName: " + row[3] + "\nSequence: " + str(row[6]) +
                          "\nSummary: \n" + row[4])
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    main(sys.argv)
