import pymysql
import requests
import sys
from datetime import datetime


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

    # Se for resposta manda o parent se não for manda o parent como zero

    # discussion = 1
    # parent = discussion
    # subject = "Re: mal ou mau"
    # created = datetime.timestamp(datetime.now())
    # modified = created
    # userid = 2
    # message = "<p>Obrigado pela resposta ^^</p>"
    # insert_post(connection, discussion, parent, userid, int(created), modified, subject, message)

    # firstpost é importante
    course = 3
    forum = 12
    name = "Ok"
    firstpost = 0
    userid = 3
    timemodified = datetime.timestamp(datetime.now())
    d = insert_discussion(connection, course, forum, name, userid, timemodified)

    discussion = d[0]
    parent = 0
    subject = d[3]
    created = datetime.timestamp(datetime.now())
    modified = created
    userid = d[5]
    message = "<p>TEstando</p>"
    p = insert_post(connection, discussion, parent, userid, int(created), modified, subject, message)
    alter_discussion(connection, d[0], p[0])

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


def insert_post(connection, discussion, parent, userid, created, modified, subject, message):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO mdl_forum_posts (`discussion`, `parent`, `userid`, `created`, `modified`, `subject`, `message`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql, (discussion, parent, userid, created, modified, subject, message))
                print("Task added successfully")
                return get_last_record(connection, "mdl_forum_posts")
            except pymysql.InternalError as error:
                code, mess = error.args
                print("Oops! Something wrong")
                print(code, mess)

    finally:
        connection.commit()


def insert_discussion(connection, course, forum, name, userid, timemodified):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO mdl_forum_discussions (`course`, `forum`, `name`, `userid`, `timemodified`) VALUES (%s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql, (course, forum, name, userid, timemodified))
                print("Task added successfully")
                return get_last_record(connection, "mdl_forum_discussions")
            except pymysql.InternalError as error:
                code, mess = error.args
                print("Oops! Something wrong")
                print(code, mess)

    finally:
        connection.commit()


def alter_discussion(connection, id, firstpost):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE mdl_forum_discussions SET `firstpost` = %s WHERE `id` = %s"
            try:
                cursor.execute(sql, (firstpost, id))
                print("Successfully Updated...")
            except:
                print("Oops! Something wrong")

    finally:
        connection.commit()


def get_last_record(connection, table):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM " + table + " ORDER BY `id` DESC LIMIT 1"
            try:
                cursor.execute(sql)
                last = cursor.fetchone()
                return last
            except:
                print("Oops! Something wrong")

    finally:
        connection.commit()


if __name__ == "__main__":
    main(sys.argv)
