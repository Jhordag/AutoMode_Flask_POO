from flask import Flask, render_template, request, redirect, session, flash, url_for
from app import app
import mysql.connector

app.secret_key = 'BiaUFGPOO'


class Plano:
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao


class Cliente:
    def __init__(self, empresa, cnpj, phone, email, senha):
        self.empresa = empresa
        self.cnpj = cnpj
        self.phone = phone
        self.email = email
        self.senha = senha


class Cartao:
    def __init__(self, parcela, numcart, dtv, cvv, nome, cpf):
        self.parcela = parcela
        self.numcart = numcart
        self.dtv = dtv
        self.cvv = cvv
        self.nome = nome
        self.cpf = cpf


# Clientes
cliente1 = Cliente('JOJH', '12345678901234', '99999000011', 'jojh@jojh.com', '1234')
cliente2 = Cliente('POJ', '12345278921234', '99999000022', 'poj@poj.com', '1357')
cliente3 = Cliente('KOL', '12345178411234', '99999000033', 'poj@poj.com', '2468')
clientes = {cliente1.email: cliente1,
            cliente2.email: cliente2,
            cliente3.email: cliente3}

# Planos
plano1 = Plano('Básico', 89.00,
               'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ornare, turpis vitae faucibus '
               'tincidunt, erat sem commodo sem, eget dapibus leo nisi non est.')
plano2 = Plano('Intermediario', 119.00,
               'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ornare, turpis vitae faucibus '
               'tincidunt, erat sem commodo sem, eget dapibus leo nisi non est.')
plano3 = Plano('Premium', 159.00,
               'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ornare, turpis vitae faucibus '
               'tincidunt, erat sem commodo sem, eget dapibus leo nisi non est.')
listaplanos = [plano1, plano2, plano3]


@app.route("/")
@app.route("/index")
def inicio():
    return render_template('index.html')


# Home Cliente
@app.route('/cliente')
def home_cliente():
    return render_template('cliente_home.html', titulo='Planos', listaplanos=listaplanos)


@app.route('/home_login')
def home_login():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('home_login')))
    return render_template('cliente_home_login.html', titulo='Home', listaplanos=listaplanos)


# Autenticação
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('cliente_login.html', proxima=proxima)


@app.route('/cliente_autenticar', methods=['POST', ])
def autenticar_cliente():
    if request.form['usuario'] in clientes:
        usuario = clientes[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.email
            flash(usuario.email + ' logou com sucesso!')
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


# Comprar Plano
@app.route('/comprarcredit')
def comprar():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('home_login')))
    return render_template('cliente_comprar.html', titulo='Comprar')


@app.route('/autenticar_cartao', methods=['POST', ])
def autenticar_cartao():
    if request.form['numcart'] is not None:
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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('perfil')))
    return render_template('cliente_perfil_usuario.html', titulo='Usuarios')


@app.route('/mensagens')
def mensagens():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('perfil')))
    return render_template('cliente_perfil_mensagem.html', titulo='Mensagens')


# Cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cliente_cadastro.html', titulo='Cadastro Cliente')


@app.route('/salvarcadastro', methods=['POST', ])
def salvar_cliente():
    db = mysql.connector.connect(user='admin', password='Lg3botisaproduct',
                                 host='lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com',
                                 database='POO')

    cursor = db.cursor()
    sql1 = "INSERT INTO CLIENTES (Nome_Empresa, CNPJ, Phone, Email, Senha) VALUES(%s, %s, %s,%s,%s)"
    datas = (
        request.form['nome_emp'], request.form['cnpj'], request.form['phone'], request.form['email'],
        request.form['senha'])
    cursor.execute(sql1, datas)
    db.commit()
    cursor.close()
    return redirect(url_for('home'))
