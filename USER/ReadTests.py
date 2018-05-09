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
    token = get_token(host, username, password, 'moodle_mobile_app')
    id = get_id(host, token)

    print('token:', token)
    print('id:', id)

    get_courses(connection, id)


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
            sql = "SELECT * FROM mdl_user u,  mdl_role_assignments ra,  mdl_context con, mdl_course c, mdl_role r WHERE u.id = ra.userid AND ra.contextid = con.id AND con.contextlevel = 50 AND con.instanceid = c.id AND ra.roleid = r.id AND r.shortname = 'student'"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print(str(row))
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    main(sys.argv)
