'''import mysql.connector
db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
                             host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
                             database='POO')

cursor = db.cursor()
sql1 = "CREATE TABLE CLIENTES  (ID int NOT NULL AUTO_INCREMENT, Nome_Empresa text, CNPJ text, Phone text, Email text, Senha text, PRIMARY KEY (id))"
cursor.execute(sql1,)'''

import mysql.connector


db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
                             host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
                             database='POO')  
cursor = db.cursor()
sql1 = f"SELECT * FROM CLIENTES" 
cursor.execute(sql1)
profile = cursor.fetchall()
for i in profile:
    print(i)
