import psycopg2
conn = psycopg2.connect(database="project_551",
                            host="localhost",
                            user="vansh16",
                            password="Vansh0513#",
                            port="5433")
        
c=conn.cursor()

c.execute("SELECT name from namenode where type='FILE';")
f_id=c.fetchall()
print(f_id)

f_path=[i[0] for i in f_id if 'whr.csv' in i[0].split('/')]
