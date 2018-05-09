import pymysql
import sys


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='moodle',
)


def main(argv):
    ''' tabela forum geral '''
    # mdl_forum()

    ''' tabela forum discussões '''
    # mdl_forum_discussions()

    ''' inscrições nas discussões de fóruns '''
    # mdl_forum_discussion_subs()

    ''' Postagens dos fóruns '''
    # mdl_forum_posts()

    ''' Inscrições em cada Fórum '''
    # mdl_forum_subscriptions()

# Forums contain and structure discussion
def mdl_forum():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `course`, `type`, `name`, `intro`, `introformat`, `maxattachments`  FROM mdl_forum"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tCurso: " + str(row[1]) + "\tTipo: " + row[2] +
                          "\tTipo da descrição: " + str(row[5]) + "\tMáximo de Anexos: " + str(row[6]) + "\nNome: "
                          + row[3] + "\nDescrição: \n" + row[4])
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


# Forums are composed of discussions
def mdl_forum_discussions():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `course`, `forum`, `name`, `firstpost`, `userid` FROM mdl_forum_discussions"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tCurso: " + str(row[1]) + "\tFórum: " + str(row[2]) +
                          "\tFirst post: " + str(row[4]) + "\tUserid: " + str(row[5]) + "\nAutor: " + row[3])
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


# Users may choose to subscribe and unsubscribe from specific
def mdl_forum_discussion_subs():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `forum`, `userid`, `discussion` FROM mdl_forum_discussion_subs"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tFórum: " + str(row[1]) + "\tUserid: " + str(row[2]) +
                          "\tDiscussion: " + str(row[3]))
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


# All posts are stored in this table
def mdl_forum_posts():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `discussion`, `parent`, `userid`, `subject`, `message`, `messageformat`, `attachment` FROM mdl_forum_posts"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tDiscussion: " + str(row[1]) + "\tParent: " + str(row[2]) +
                          "\tUserId: " + str(row[3]) + "\nMessageFormat: " + str(row[6]) + "\nSubject: " + row[4] +
                          "\nMessage:\n" + row[5] + "\nAttachment:\n" + row[7])
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


# all forum subscritions
def mdl_forum_subscriptions():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `userid`, `forum` FROM mdl_forum_subscriptions"
            try:
                cursor.execute(sql)
                result = cursor.fetchall()
                for row in result:
                    print("Id: " + str(row[0]) + "\tUserId: " + str(row[1]) + "\tForum: " + str(row[2]))
                    print("-------------------------------------------------------------------------------------------")
            except:
                print("Oops! Something wrong")

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    main(sys.argv)
