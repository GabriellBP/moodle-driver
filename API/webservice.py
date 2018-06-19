from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

# Configuração da conexão com o banco de dados do Moodle
database = {'host': 'localhost', 'user': 'root', 'password': '', 'db': 'moodle'}

# Instancia do Flask
app = Flask(__name__)
app.config['MYSQL_HOST'] = database['host']
app.config['MYSQL_USER'] = database['user']
app.config['MYSQL_PASSWORD'] = database['password']
app.config['MYSQL_DB'] = database['db']
mysql = MySQL(app)


@app.route("/")
def index():
    return "Moodle API RESTFul"


# GET /courses/:user_id
@app.route('/courses/<int:user_id>')
def courses(user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT c.id, c.fullname, c.shortname FROM mdl_user u,  mdl_role_assignments ra,  mdl_context con, mdl_course c, mdl_role r WHERE u.id = ra.userid AND ra.contextid = con.id AND con.contextlevel = 50 AND con.instanceid = c.id AND ra.roleid = r.id AND r.shortname = 'student' AND u.id = " + str(user_id))
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
        cur.execute("SELECT `id`, `type`, `name`, `intro`, `introformat`, `maxattachments`  FROM mdl_forum WHERE id = " + str(forum_id))
        forum = cur.fetchone()
        cur.execute("SELECT `id`, `name`, `userid` FROM mdl_forum_discussions WHERE forum = " + str(forum_id))
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        discussions = []
        for result in rv:
            discussions.append(dict(zip(row_headers, result)))
        json_data = {'id': forum[0], 'type': forum[1], 'name': forum[2], 'intro': forum[3], 'introformat': forum[4],
                     'maxattachments': forum[5], 'discussions': discussions}
        return jsonify(json_data)
    except:
        return jsonify({'status': 404, 'mensagem': 'Forum não encontrado'})



# GET /discussion/:discussion_id
@app.route('/discussion/<int:discussion_id>')
def discussion(discussion_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT `id`, `name`, `firstpost`, `userid` FROM mdl_forum_discussions WHERE id = " + str(discussion_id))
        discussion = cur.fetchone()
        cur.execute("SELECT P.id, p.parent, p.userid, p.modified, p.subject, p.message FROM mdl_forum_posts p WHERE discussion = " + str(discussion_id) + " ORDER BY p.id ASC")
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        posts = []
        for result in rv:
            posts.append(dict(zip(row_headers, result)))
        json_data = {'id': discussion[0], 'name': discussion[1], 'firstpost': discussion[2], 'userid': discussion[3],
                     'posts': posts}
        return jsonify(json_data)
    except:
        return jsonify({'status': 404, 'mensagem': 'Discussão não encontrada'})


# POST /forum/:forum_id
@app.route('/forum/<int:forum_id>', methods=['POST'])
def new_discussion(forum_id):
    try:
        sql = "INSERT INTO mdl_forum_discussions (`course`, `forum`, `name`, `userid`, `timemodified`) VALUES (%s, %s, %s, %s, %s)"
        data = request.json
        timenow = datetime.timestamp(datetime.now())
        cur = mysql.connection.cursor()
        cur.execute(sql, (data['course'], data['forum'], data['name'], data['userid'], timenow))
        return jsonify({'status': 200, 'mensagem': 'Discussão salva com sucesso!'})
    except:
        return jsonify({'status': 400, 'mensagem': 'Dados Inválidos'})


if __name__ == '__main__':
    app.run(debug=True)