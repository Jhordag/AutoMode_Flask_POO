import mysql.connector

# Função que adiciona novas mensagens ao DB de comparação
db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
                             host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
                             database='POO')


def generatorTable():
    cursor = db.cursor()
    sql1 = "CREATE TABLE  acessAdmin  (ID int NOT NULL AUTO_INCREMENT,Email text, Senha text, PRIMARY KEY (id))"
    cursor.execute(sql1)

def generatorTable2():
    cursor = db.cursor()
    sql1 = "CREATE TABLE  acessFuncionario  (ID int NOT NULL AUTO_INCREMENT,Email text, Senha text, PRIMARY KEY (id))"
    cursor.execute(sql1)

def generatorTable3():
    cursor = db.cursor()
    sql1 = "CREATE TABLE  acessClient  (ID int NOT NULL AUTO_INCREMENT,Email text, Senha text, PRIMARY KEY (id))"
    cursor.execute(sql1)


def addData():
    cursor = db.cursor()
    sql1 = f"INSERT INTO  acessClient (Email, Senha) Value('gabriel', '123')"
    cursor.execute(sql1)
    db.commit()

def addData2():
    cursor = db.cursor()
    sql1 = f"INSERT INTO  acessFuncionario (Email, Senha) Value('gabriel', '123')"
    cursor.execute(sql1)
    db.commit()

def addData1():
    cursor = db.cursor()
    sql1 = f"INSERT INTO  acessAdmin (Email, Senha) Value('gabriel', '123')"
    cursor.execute(sql1)
    db.commit()


def writeDB():
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  acessClient WHERE Email='gabriel' AND Senha='123' "
    cursor.execute(sql1)
    profile = cursor.fetchall()
    print(profile)

def writeDB2():
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  acessFuncionario WHERE Email='gabriel' AND Senha='123' "
    cursor.execute(sql1)
    profile = cursor.fetchall()
    print(profile)

def writeDB1():
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  acessAdmin WHERE Email='gabriel' AND Senha='123' "
    cursor.execute(sql1)
    profile = cursor.fetchall()
    print(profile)

#def updateData():
# 	cursor = db.cursor()
#    sql = "UPDATE NumbersSend SET confirmation='f"
#    cursor.execute(sql1)
#   db.commit()

writeDB()
writeDB2()
writeDB1()
