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

if __name__ == "__main__":
    main(sys.argv)
