import pymysql
import requests
import sys


def main(argv):
    host = 'localhost'

    connection = pymysql.connect(
        host=host,
        user='root',
        password='',
        db='moodle',
    )

    username = 'admin'
    password = 'aA123456789*'
    token = get_token(host, username, password, 'moodle_mobile_app')
    id = get_id(host, token)

    print('token:', token)
    print('id:', id)

    courses = get_courses(connection, id)
    print(courses)

    foruns = {}
    for course in courses:
        foruns[course] = get_foruns(connection, course)
    print(foruns)
    connection.close()


def get_token(host, username, password, service):
    request = requests.get(
        'http://' + host + '/moodle/login/token.php?username='+username+'&password='+password+'&service='+service)
    json_response = request.json()
    return json_response['token']


def get_id(host, token):
    function = 'core_webservice_get_site_info'
    request = requests.get(
        'http://'+host+'/moodle/webservice/rest/server.php?wstoken='+token+'&wsfunction='+function+'&moodlewsrestformat=json'
    )
    json_response = request.json()
    return json_response['userid']


def get_courses(connection, user_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT c.id FROM mdl_user u,  mdl_role_assignments ra,  mdl_context con, mdl_course c, mdl_role r WHERE u.id = ra.userid AND ra.contextid = con.id AND con.contextlevel = 50 AND con.instanceid = c.id AND ra.roleid = r.id AND r.shortname = 'student' AND u.id = " + str(user_id)
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                courses = []
                for row in result:
                    # print(row[0])
                    courses.append(row[0])
                return courses

            except:
                print("Oops! Something wrong")

    finally:
        connection.commit()


def get_foruns(connection, course_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `type`, `name`, `intro`, `introformat`, `maxattachments`  FROM mdl_forum WHERE course = " + str(course_id)
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                foruns = []
                for row in result:
                    foruns.append(row)
                return foruns

            except:
                print("Oops! Something wrong")

    finally:
        connection.commit()


if __name__ == "__main__":
    main(sys.argv)
