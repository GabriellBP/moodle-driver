import pymysql
import csv

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='moodle',
)


# gerando csv com a biblioteca csv
def generate_csv():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT f.course as courseId, f.forum as forumId, p.discussion as discussionId, p.id as postId, " \
                  "p.parent as  postParentId, p.userid as userId, p.modified as modifiedDate, p.subject, p.message " \
                  "FROM mdl_forum_posts p, mdl_forum_discussions f " \
                  "WHERE f.id = p.discussion"

            try:
                cursor.execute(sql)
                row_headers = [x[0] for x in cursor.description]
                result = cursor.fetchall()
                fp = open('temp.csv', 'w')
                myFile = csv.writer(fp)
                myFile.writerow(row_headers)
                myFile.writerows(result)
                fp.close()
                print("OK!")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


# gerando csv através de comandos sql (obs.: se já ouver o arquivo, ele da erro e não recria nem altera o mesmo)
def generate_csv_msql():
    try:
        with connection.cursor() as cursor:
            sql = "(SELECT 'courseId', 'forumId', 'discussionId', 'postId', 'postParentId', 'userId', 'modifiedDate', 'subject', 'message')" \
                  "UNION" \
                  " (SELECT f.course, f.forum, p.discussion, p.id, p.parent, p.userid, p.modified, p.subject, p.message" \
                  " FROM mdl_forum_posts p, mdl_forum_discussions f" \
                  " WHERE f.id = p.discussion" \
                  " INTO OUTFILE 'temp.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n')"
            try:
                cursor.execute(sql)
                print("OK!")
            except Exception as e:
                print("Oops! Something wrong")
                print(e)

        connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    generate_csv()
    # generate_csv_msql()
