import mysql.connector

conectar=mysql.connector.connect(
    host='localhost',
    user='root',
    password='alex12345678',
    database='ferpacific'
)

cursor=conectar.cursor()
cursor.execute("select * from rangos_deficiencia")
print(cursor.fetchall())
cursor.close()
conectar.close()