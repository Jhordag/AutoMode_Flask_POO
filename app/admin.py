from flask_mysqldb import MySQL
import os
import mysql.connector
from app import app
from flask import render_template, request, redirect, session, flash, url_for

db = mysql.connector.connect(host=("lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com"),
                             user=("admin"),
                             password=("Lg3botisaproduct"),
                             db=("POO"))

app.secret_key = 'BiaUFGPOO'


class Admin:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


class Cliente:
    def __init__(self, empresa, cnpj, plano):
        self.empresa = empresa
        self.cnpj = cnpj
        self.plano = plano


class Funcionario:
    def __init__(self, nome, cpf, salario, cargo):
        self.nome = nome
        self.cpf = cpf
        self.salario = salario
        self.cargo = cargo


class Plano:
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao


# Home
@app.route('/admin')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('admin_login', proxima=url_for('index')))
    return render_template('admin_home.html', titulo='Home Admin')


# Rotas Autencaticação
@app.route('/admin_login')
def admin_login():
    proxima = request.args.get('proxima')
    return render_template('admin_login.html', proxima=proxima)


######################### Gabriel Urzeda #################################
'''
Deve usar os dados que estão presentes na tabela Admin para validar a entrada 
na pagina.
Lembra-se que tem os funcionarios é os admins então deve ter um redimensionamento 
de paginas diferentes para eles.
o def autenticar_cliente() no arquino cliente.py pode ser usado com exemplo
'''


########################################################################
@app.route('/admin_autenticar', methods=['POST', ])
def autenticar_admin():
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  acessAdmin WHERE Email='{request.form['usuario']}' AND senha='{request.form['senha']}' "
    cursor.execute(sql1)
    profile = cursor.fetchall()
    print(profile)

    if len(profile) != 0:
        session['usuario_logado'] = profile[0][1]
        flash(profile[0][1] + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('admin_login'))


@app.route('/admin_logout')
def admin_logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


# Rotas Funcionarios
######################### Gabriel Urzeda #################################
'''
Deve Usar as informação da  tabela admin para serem rederizadas 
para isso deve se usar passar uma lista de todos os usuarios para trabalhadores
'''


########################################################################
@app.route('/admin_funcionarios')
def funcionarios():
    # Funcionarios
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  Funcionario"
    cursor.execute(sql1)
    trabalhadores = cursor.fetchall()
    listatrabalhadores = []
    for i in trabalhadores:
        listatrabalhadores.append(Funcionario(i[1], i[2], i[3], i[4]))

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_funcionarios')))
    return render_template('admin_funcionario.html', titulo='Funcionarios', trabalhadores=listatrabalhadores)


######################### Gabriel Urzeda #################################
'''
Deve Usar a tabela admin para salvar as informações
A função def salvar_cliente() do arquivo cliente.py pode servir de exemplo
'''


########################################################################
@app.route('/criarfunc', methods=['POST', ])
def criarfunc():
    cursor = db.cursor()
    sql1 = "INSERT INTO Funcionario (nome, cpf, salario, cargo) VALUES(%s, %s, %s, %s)"
    datas = (request.form['nome'],request.form['cpf'],request.form['salario'],request.form['cargo'])
    cursor.execute(sql1, datas)
    db.commit()
    return redirect(url_for('funcionarios'))


# Rotas dos Planos
######################### Gabriel Urzeda #################################
'''
Deve Usar as informação da  tabela planos para serem rederizadas 
para isso deve se usar passar uma lista de todos os planos para listaplanos
'''
########################################################################

######################### Gabriel Marques ##############################
'''
Deve ser possivel editar ou excluir plano
'''


########################################################################
@app.route('/admin_planos')
def planos():
    # Planos
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  Plano"
    cursor.execute(sql1)
    planos = cursor.fetchall()
    listaplanos = []
    for i in planos:
        listaplanos.append(Plano(i[1], i[2], i[3]))

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_planos')))
    return render_template('admin_planos.html', titulo='Funcionarios', listaplanos=listaplanos)


@app.route('/admin_novo_plano')
def admin_planos():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_novo_plano')))
    return render_template('admin_criar_plano.html', titulo='Novo Plano')


######################### Gabriel Urzeda #################################
'''
Deve Usar a tabela plano para salvar as informações
A função def salvar_cliente() do arquivo cliente.py pode servir de exemplo
'''


########################################################################
@app.route('/criarplano', methods=['POST', ])
def criarplano():
    cursor = db.cursor()
    sql1 = "INSERT INTO Plano (Nome, Preco, Descricao) VALUES(%s, %s, %s)"
    datas = (request.form['nome'],request.form['preco'],request.form['descricao'])
    cursor.execute(sql1, datas)
    db.commit()
    return redirect(url_for('planos'))


# Rotas Clientes
######################### Gabriel Urzeda #################################
'''
Deve Usar as informação da  tabela CLIENTES para serem rederizadas 
para isso deve se usar passar uma lista de todos os clientes cadastrados 
para listaclientes
'''


########################################################################
@app.route('/admin_cliente')
def cliente():
    # Clientes
    cursor = db.cursor()
    sql1 = f"SELECT * FROM  CLIENTES"
    cursor.execute(sql1)
    clientes = cursor.fetchall()
    listaclientes = []
    for i in clientes:
        listaclientes.append(Cliente(i[1], i[2], 'Premium'))

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_cliente')))
    return render_template('admin_cliente.html', titulo='Clientes', listaclientes=listaclientes)
