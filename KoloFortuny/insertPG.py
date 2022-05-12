import psycopg2 as ps


def pointsToTable(name, points, cat):
    conn = ps.connect("host=212.182.24.105 port=15432 dbname=student6 user=student6 password=st2021%6")
    cur = conn.cursor()
    cur.execute("INSERT INTO points (name, points, category) VALUES (%(str)s, %(int)s, %(str2)s)",
                {'str': name, 'int': points, 'str2': cat})
    conn.commit()
    cur.close()
    conn.close()
    return


'''for i in range(0, 10):
    category = input("Kategoria: ")
    text = input("Treść pytania: ")
    answer = input("Odpowiedź: ")
    cur.execute("INSERT INTO Questions (category, text, answer) VALUES (%s, %s, %s)",
                category, text, answer)
'''
