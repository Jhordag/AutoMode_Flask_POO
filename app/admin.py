from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'BiaUFGPOO'



class Admin:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha




# Admins
admin1 = Admin('luan', 'Luan Marques', '1234')
admin2 = Admin('Nico', 'Nico Steppat', '7a1')
admin3 = Admin('flavio', 'flavio Almeida', 'javascript')

usuarios = {admin1.nome: admin1,
            admin2.nome: admin2,
            admin3.nome: admin3}

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
