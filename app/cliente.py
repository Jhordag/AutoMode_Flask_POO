from app  import app
from flask import  render_template, request, redirect, session, flash, url_for
import mysql.connector

db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
                             host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
                             database='POO')

app.secret_key = 'BiaUFGPOO'
class Plano:
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao

class Cartao:
    def __init__(self,parcela,numcart,dtv,cvv,nome,cpf):
        self.parcela = parcela
        self.numcart = numcart
        self.dtv = dtv
        self.cvv = cvv
        self.nome = nome
        self.cpf = cpf

class Usuarios:
    def __init__(self,nome,phone):
        self.nome = nome
        self.phone = phone

class Cadastro:
    def __init__(self,nome_empresa,cnpj,phone,email,senha):
        self.nome_empresa = nome_empresa
        self.cnpj = cnpj
        self.phone = phone
        self.email = email
        self.senha = senha

@app.route("/")
def inicio():
    return render_template('index.html')

@app.route('/home')
def home():
    # Planos
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  Plano"
    cursor.execute(sql1)
    planos = cursor.fetchall()
    listaplanos = []
    for i in planos:
        listaplanos.append(Plano(i[1], i[2], i[3]))

    return render_template('cliente_home.html', titulo='Planos', listaplanos=listaplanos)
@app.route('/home_login')
def home_login():
    # Planos
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  Plano"
    cursor.execute(sql1)
    planos = cursor.fetchall()
    listaplanos = []
    for i in planos:
        listaplanos.append(Plano(i[1], i[2], i[3]))

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('home_login')))
    return render_template('cliente_home_login.html', titulo='Home', listaplanos=listaplanos)

#Autenticação
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('cliente_login.html',proxima=proxima)

@app.route('/cliente_autenticar', methods=['POST', ])
def autenticar_cliente():
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  CLIENTES WHERE Email='{request.form['usuario']}' AND Senha='{request.form['senha']}' "
    cursor.execute(sql1)
    profile = cursor.fetchall()
    print(profile)

    if len(profile) != 0:
        print('Entrou')
        session['usuario_logado'] = profile[0][1]
        flash(profile[0][1] + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('home'))

#Cadastro 
@app.route('/cadastro')
def cadastro():
    return render_template('cliente_cadastro.html', titulo='Cadastro Cliente')

@app.route('/salvarcadastro',methods=['POST', ])
def salvar_cliente():
    cursor = db.cursor()
    sql1 = "INSERT INTO CLIENTES (Nome_Empresa, CNPJ, Phone, Email, Senha) VALUES(%s, %s, %s,%s,%s)"
    datas = (request.form['nome_emp'],request.form['cnpj'],request.form['phone'],request.form['email'],request.form['senha'])
    cursor.execute(sql1, datas)
    db.commit()
    return redirect(url_for('home'))


#Comprar Plano
@app.route('/comprarcredit')
def comprar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('home_login')))
    return render_template('cliente_comprar.html', titulo='Comprar')

@app.route('/autenticar_cartao', methods=['POST', ])
def autenticar_cartao():
    if request.form['numcart'] != None :
        flash('Compara feita  com sucesso!')
        return redirect(url_for('home_login'))
    else:
        flash('Não foi possivel fazer a comprar!')
        return redirect(url_for('login'))

# Perfil Cliente
@app.route('/perfil')
def perfil():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('perfil')))
    return render_template('cliente_perfil.html', titulo='Perfil')

@app.route('/usuarios')
def usuarios():
    # Usuarios
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  CLIENTES"
    cursor.execute(sql1)
    users = cursor.fetchall()
    users_cliente = []
    for i in users:
        users_cliente.append(Usuarios(i[1], i[2]))

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('perfil')))
    return render_template('cliente_perfil_usuario.html', titulo='Usuarios',users_cliente = users_cliente)
@app.route('/cadastrousuario', methods=['POST',])
def criarusuarios():
    nome = request. form['nome']
    phone= request. form['phone']
    cursor = db.cursor()
    sql1 = "INSERT INTO Usuarios (Nome, Phone) VALUES('%s', '%s')"
    datas = (request.form['Nome'],request.form['Phone'])
    cursor.execute(sql1, datas)
    db.commit()
    return redirect(url_for('usuarios'))

@app.route('/mensagens')
def mensagens():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('perfil')))
    return render_template('cliente_perfil_mensagem.html', titulo='Mensagens')

@app.route('/validarmensagem', methods=['POST',])
def validarmensagem():
    flash('Mensagem enviada com sucesso!')
    return redirect(url_for('mensagens'))
