# import mysql.connector
# db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
#                              host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
#                              database='POO')
#
# cursor = db.cursor()
# sql1 = "CREATE TABLE CLIENTESPlano  (ID int NOT NULL AUTO_INCREMENT, Nome_Plano text, Preço float, Descricao text, PRIMARY KEY (id))"
# cursor.execute(sql1,)

import mysql.connector


db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
                             host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
                             database='POO')
# cursor = db.cursor()
# sql1 = f"SELECT * FROM planos"
# cursor.execute(sql1)
# profile = cursor.fetchall()

cursor = db.cursor()
sql1 = f"SELECT * FROM  Funcionario"
cursor.execute(sql1)
listaplanos = cursor.fetchall()

for i in listaplanos:
    print(i)
