import psycopg2 as ps

conn = ps.connect("host=212.182.24.105 port=15432 dbname=student6 user=student6 password=st2021%6")
cur = conn.cursor()
cur.execute("CREATE TABLE Questions (id serial PRIMARY KEY, category varchar, text varchar, answer varchar);")
conn.commit()
cur.close()
conn.close()
