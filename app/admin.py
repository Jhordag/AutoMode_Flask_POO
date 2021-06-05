from flask_mysqldb import MySQL
import os
import mysql.connector
from app  import app
from flask import  render_template, request, redirect, session, flash, url_for

app.secret_key = 'BiaUFGPOO'
mysql =  mysql.connector.connect (host = ("lg3bot.cxp5nvrsoub5.us-east-2.rds.amazonaws.com"), 
            user =  ("admin"), 
              password = ("Lg3botisaproduct"), 
              db =  ("POO"),)


class Admin:
    def __init__(self, id, email, senha):
        self.id = id
        self.email = email
        self.senha = senha

class Cliente:
    def __init__(self, empresa, cnpj, plano):
        self.empresa = empresa
        self.cnpj = cnpj
        self.plano = plano       
class Funcionario():
    def __init__(self,nome,cpf,salario,cargo):
        self.nome = nome
        self.cpf = cpf
        self.salario = salario
        self.cargo = cargo

class Plano:
    def __init__(self, nome, preco, descricao):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao






# Admins
admin1 = Admin('luan', 'Luan Marques', '1234')
admin2 = Admin('Nico', 'Nico Steppat', '7a1')
admin3 = Admin('flavio', 'flavio Almeida', 'javascript')
usuarios = {admin1.email: admin1,
            admin2.email: admin2,
            admin3.email: admin3}

# Clientes
cliente1 = Cliente('Loja 67','46964253000186','Premium')
cliente2 = Cliente('JUSTGOI','46964253000186','Básico')
cliente3 = Cliente('GOIRF','46964253000186','Intermediario')
listaclientes = [cliente1,cliente2,cliente3]


# Funcionarios
funcionario1 = Funcionario('Ana','1234567890',3500.00,'Dev')
funcionario2 = Funcionario('Pedro','4234447890',3500.00,'Dev')
funcionario3 = Funcionario('Maria','4235677890',3000.00,'UX')
trabalhadores = [funcionario1, funcionario2, funcionario3]

# Planos
plano1 = Plano('Básico',89.00, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ornare, turpis vitae faucibus tincidunt, erat sem commodo sem, eget dapibus leo nisi non est.')
plano2 = Plano('Intermediario',119.00, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ornare, turpis vitae faucibus tincidunt, erat sem commodo sem, eget dapibus leo nisi non est.')
plano3 = Plano('Premium',159.00, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ornare, turpis vitae faucibus tincidunt, erat sem commodo sem, eget dapibus leo nisi non est.')
listaplanos = [plano1,plano2,plano3]




# Home
@app.route('/admin')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
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
    
    cursor = mysql.cursor()
    sql1 = f"SELECT * FROM  accessClient WHERE Email='{request.form['usuario']}' AND senha='{request.form['senha']}' "
    cursor.execute(sql1)
    profile = cursor.fetchall()
    print(profile)
    
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.email
            flash(usuario.email + ' logou com sucesso!')
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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_funcionarios')))
    return render_template('admin_funcionario.html', titulo='Funcionarios', trabalhadores = trabalhadores)


######################### Gabriel Urzeda #################################
'''
Deve Usar a tabela admin para salvar as informações
A função def salvar_cliente() do arquivo cliente.py pode servir de exemplo
'''
########################################################################
@app.route('/criarfunc', methods=['POST',])
def criarfunc():
    nome = request. form['nome']
    cpf = request. form['cpf']
    salario = request. form['salario']
    cargo = request. form['cargo']
    func = Funcionario( nome,cpf,salario,cargo)
    trabalhadores.append(func)
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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_planos')))
    return render_template('admin_planos.html', titulo='Funcionarios', listaplanos = listaplanos)

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
@app.route('/criarplano', methods=['POST',])
def criarplano():
    nome = request. form['nome']
    preco = request. form['preco']
    descricao = request. form['descricao']
    plano = Plano( nome,preco,descricao)
    listaplanos.append(plano)
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
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_cliente')))
    return render_template('admin_cliente.html', titulo='Clientes', listaclientes = listaclientes)

