import psycopg2 as ps
import random


def draw_question():
    conn = ps.connect("host=212.182.24.105 port=15432 dbname=student6 user=student6 password=st2021%6")
    cur = conn.cursor()

    number = random.randint(1, 10)
    cur.execute("SELECT category, text, answer FROM Questions")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return data[number - 1]


def get_score(type):
    conn = ps.connect("host=212.182.24.105 port=15432 dbname=student6 user=student6 password=st2021%6")
    cur = conn.cursor()

    if type == 'gra':
        cur.execute("SELECT name, points FROM points WHERE category = 'gra' ORDER BY points DESC LIMIT 3")
        score = cur.fetchall()
    elif type == 'runda':
        cur.execute("SELECT name, points FROM points WHERE category = 'runda' ORDER BY points DESC LIMIT 3")
        score = cur.fetchall()

    cur.close()
    conn.close()

    return score
