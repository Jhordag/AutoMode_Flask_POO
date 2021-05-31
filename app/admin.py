from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'BiaUFGPOO'



class Admin:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha

class Funcionario():
    def __init__(self,nome,cpf,salario,cargo):
        self.nome = nome
        self.cpf = cpf
        self.salario = salario
        self.cargo = cargo

# Admins
admin1 = Admin('luan', 'Luan Marques', '1234')
admin2 = Admin('Nico', 'Nico Steppat', '7a1')
admin3 = Admin('flavio', 'flavio Almeida', 'javascript')
usuarios = {admin1.nome: admin1,
            admin2.nome: admin2,
            admin3.nome: admin3}

# Funcionarios
funcionario1 = Funcionario('Ana','1234567890',3500.00,'Dev')
funcionario2 = Funcionario('Pedro','4234447890',3500.00,'Dev')
funcionario3 = Funcionario('Maria','4235677890',3000.00,'UX')
trabalhadores = [funcionario1, funcionario2, funcionario3]


# Home
@app.route('/admin')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('index')))
    return render_template('admin_home.html', titulo='Home Admin')

# Rotas Autencaticação
@app.route('/admin_login')
def login():
    proxima = request.args.get('proxima')
    return render_template('admin_login.html', proxima=proxima)

@app.route('/admin_autenticar', methods=['POST', ])
def autenticar_admin():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.nome
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route('/admin_logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

# Rotas Funcionarios
@app.route('/admin_funcionarios')
def funcionarios():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('admin_funcionarios')))
    return render_template('admin_funcionario.html', titulo='Funcionarios', trabalhadores = trabalhadores)

@app.route('/criarfunc', methods=['POST',])
def criarfunc():
    nome = request. form['nome']
    cpf = request. form['cpf']
    salario = request. form['salario']
    cargo = request. form['cargo']
    func = Funcionario( nome,cpf,salario,cargo)
    trabalhadores.append(func)
    return redirect(url_for('funcionarios'))



app.run(debug=True)
