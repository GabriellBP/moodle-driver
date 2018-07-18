from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

from datetime import datetime
import json

# Configuração da conexão com o banco de dados do Moodle
database = {'host': 'localhost', 'user': 'root', 'password': '', 'db': 'moodle'}

# Instancia do Flask
app = Flask(__name__)
app.config['MYSQL_HOST'] = database['host']
app.config['MYSQL_USER'] = database['user']
app.config['MYSQL_PASSWORD'] = database['password']
app.config['MYSQL_DB'] = database['db']
CORS(app)
mysql = MySQL(app)


@app.route("/")
def index():
    return "Moodle API RESTFul"


# GET /user/:user_id
@app.route('/user/<int:user_id>')
def user(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT u.firstname, u.lastname FROM mdl_user u WHERE u.id = %s" % str(user_id))
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchone()
        json_data = dict(zip(row_headers, rv))
        return jsonify(json_data)
    except:
        return jsonify({'status': 400, 'mensagem': 'ID inválido'})


# GET /courses/:user_id
@app.route('/courses/<int:user_id>')
def courses(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT c.id, c.fullname, c.shortname FROM mdl_user u,  mdl_role_assignments ra,  mdl_context con, mdl_course c, mdl_role r WHERE u.id = ra.userid AND ra.contextid = con.id AND con.contextlevel = 50 AND con.instanceid = c.id AND ra.roleid = r.id AND r.shortname = 'student' AND u.id = " + str(
                user_id))
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            cur.execute("SELECT `id`, `name`, `intro`  FROM mdl_forum WHERE course = " + str(result[0]))
            rvv = cur.fetchall()
            forums = []
            for f in rvv:
                forum = {'id': f[0], 'name': f[1], 'intro': f[2]}
                forums.append(forum)
            content = {'id': result[0], 'fullname': result[1], 'shortname': result[2], 'forum': forums}
            json_data.append(content)
        return jsonify(json_data)
    except:
        return jsonify({'status': 400, 'mensagem': 'Usuário inválido'})


# GET /forum/:forum_id
@app.route('/forum/<int:forum_id>')
def forum(forum_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT `id`, `type`, `name`, `intro`, `introformat`, `maxattachments`  FROM mdl_forum WHERE id = " + str(
                forum_id))
        forum = cur.fetchone()
        cur.execute("SELECT `id`, `name`, `userid`, `timemodified` FROM mdl_forum_discussions WHERE forum = " + str(
            forum_id))
        rv = cur.fetchall()
        discussions = []
        for result in rv:
            username = json.loads(user(result[2]).get_data(as_text=True))
            discussion = {'id': result[0], 'name': result[1], 'userid': result[2], 'username': username, 'timemodified': result[3]}
            discussions.append(discussion)
        json_data = {'id': forum[0], 'type': forum[1], 'name': forum[2], 'intro': forum[3], 'introformat': forum[4],
                     'maxattachments': forum[5], 'discussions': discussions}
        return jsonify(json_data)
    except Exception as e:
        print(e)
        return jsonify({'status': 404, 'mensagem': 'Forum não encontrado'})


# GET /discussion/:discussion_id
@app.route('/discussion/<int:discussion_id>')
def discussion(discussion_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT `id`, `name`, `firstpost`, `userid` FROM mdl_forum_discussions WHERE id = " + str(discussion_id))
        discussion = cur.fetchone()  # informações abaixo + id_discussão + id_forum
        cur.execute(
            "SELECT P.id, p.parent, p.userid, p.modified, p.subject, p.message FROM mdl_forum_posts p WHERE discussion = " + str(
                discussion_id) + " ORDER BY p.id ASC")
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        posts = []
        for result in rv:
            post = {'id': result[0], 'parent': result[1], 'userid': result[2], 'modified': datetime.fromtimestamp(
                int(result[3])
            ).strftime('%d-%m-%Y %H:%M:%S'), 'subject': result[4], 'message': result[5]}
            posts.append(post)
        json_data = {'id': discussion[0], 'name': discussion[1], 'firstpost': discussion[2], 'userid': discussion[3],
                     'posts': posts}
        return jsonify(json_data)
    except Exception as e:
        print(e)
        return jsonify({'status': 404, 'mensagem': 'Discussão não encontrada'})


# POST /forum/:forum_id
@app.route('/forum/<int:forum_id>', methods=['POST'])
def new_discussion(forum_id):
    try:
        sql = "INSERT INTO mdl_forum_discussions (`course`, `forum`, `name`, `userid`, `timemodified`) VALUES (%s, %s, %s, %s, %s)"
        data = request.json
        timenow = datetime.timestamp(datetime.now())
        cur = mysql.connection.cursor()
        cur.execute(sql, (data['course'], forum_id, data['title'], data['userid'], int(timenow)))
        cur.fetchall()
        discussion = get_last_record("mdl_forum_discussions")
        new_post(discussion['id'], data['message'], data['title'], data['userid'])
        post = get_last_record("mdl_forum_posts")
        sql = "UPDATE mdl_forum_discussions SET `firstpost` = %s WHERE `id` = %s"
        cur.execute(sql, (post['id'], discussion['id']))
        mysql.connection.commit()
        return jsonify({'status': 200, 'mensagem': 'Discussão salva com sucesso!'})
    except Exception as e:
        print(e)
        return jsonify({'status': 400, 'mensagem': 'Dados Inválidos'})


# POST /discussion/:discussion_id
@app.route('/discussion/<int:discussion_id>', methods=['POST'])
def new_post(discussion_id, message="", subject="", userid=-1):
    try:
        sql = "INSERT INTO mdl_forum_posts (`discussion`, `parent`, `userid`, `created`, `modified`, `subject`, `message`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = request.json
        timenow = datetime.timestamp(datetime.now())
        cur = mysql.connection.cursor()
        if userid != -1:
            cur.execute(sql, (discussion_id, 0, userid, int(timenow), int(timenow), subject, message))
        else:
            cur.execute(sql, (
            discussion_id, data['firstpost'], data['userid'], int(timenow), int(timenow), data['subject'],
            data['message']))
            sql = "UPDATE mdl_forum_discussions SET `timemodified` = %s, `usermodified` = %s WHERE `id` = %s"
            cur.execute(sql, (int(timenow), data['userid'], discussion_id))
            mysql.connection.commit()
        return jsonify({'status': 200, 'mensagem': 'Post salvo com sucesso!'})
    except Exception as e:
        print(e)
        return jsonify({'status': 400, 'mensagem': 'Dados Inválidos'})


def get_last_record(table):
    try:
        with mysql.connection.cursor() as cursor:
            sql = "SELECT * FROM " + table + " ORDER BY `id` DESC LIMIT 1"
            cursor.execute(sql)
            row_headers = [x[0] for x in cursor.description]
            last = cursor.fetchone()
            last = dict(zip(row_headers, last))
            return last
    except:
        return jsonify({'status': 404, 'mensagem': 'Não encontrado!'})


if __name__ == '__main__':
    app.run(debug=True)
