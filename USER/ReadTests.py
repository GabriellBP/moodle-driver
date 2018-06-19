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

    username = 'jorge'
    password = 'aA123456789*'
    token = get_token(host, username, password, 'moodle_easyForum_app')
    id = get_id(host, token)

    print('token:', token)
    print('id:', id)

    courses = get_courses(connection, id)
    print("cursos:")
    print(courses)

    foruns = {}
    for course in courses:
        foruns[course[0]] = get_foruns(connection, course[0])
    print("Foruns:")
    print(foruns)

    discussions = {}
    for id_course in foruns:
         for forum in foruns[id_course]:
            discussions[forum[0]] = get_discussions(connection, forum[0])
    print("Discussions")
    print(discussions)

    get_posts(connection, 1, 1)

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
            sql = "SELECT c.id, c.fullname FROM mdl_user u,  mdl_role_assignments ra,  mdl_context con, mdl_course c, mdl_role r WHERE u.id = ra.userid AND ra.contextid = con.id AND con.contextlevel = 50 AND con.instanceid = c.id AND ra.roleid = r.id AND r.shortname = 'student' AND u.id = " + str(user_id)
            try:
                cursor.execute(sql)
                courses = cursor.fetchall()
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


def get_discussions(connection, forum_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `course`, `forum`, `name`, `firstpost`, `userid` FROM mdl_forum_discussions WHERE forum = " + str(forum_id)
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                discussions = []
                for row in result:
                    discussions.append(row)
                return discussions

            except:
                print("Oops! Something wrong")

    finally:
        connection.commit()


def get_posts(connection, discussion_id, first_post):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT P.id, p.discussion, p.parent, p.userid, p.modified, p.subject, p.message FROM mdl_forum_posts p WHERE discussion = " + str(discussion_id) + " ORDER BY p.id ASC"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                posts = []
                for row in result:
                    posts.append(row)
                print(posts)

            except:
                print("Oops! Something wrong")

    finally:
        connection.commit()


if __name__ == "__main__":
    main(sys.argv)
