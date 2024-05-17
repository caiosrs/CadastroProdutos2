from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

dados_conexao = (
    "Driver={SQL Server};"
    "Server=ISPD-DP062\\SQLEXPRESS01;"
    "Database=DatabaseTeste;"
    "Trusted_Connection=yes;"
)

def conectar_bd():
    return pyodbc.connect(dados_conexao)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome_cad']
        email = request.form['email_cad']
        senha = request.form['senha_cad']

        conexao = conectar_bd()
        cursor = conexao.cursor()

        cursor.execute(
                """INSERT INTO Usuarios (Nome, Email, Senha)
                    VALUES (?, ?, ?)""", (nome, email, senha))
        conexao.commit()
        cursor.close()
        conexao.close()

        return redirect(url_for('sucesso_login'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email_login']
        senha = request.form['senha_login']

        conexao = conectar_bd()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM Usuarios WHERE Email = ? AND Senha = ?", (email, senha))
        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if usuario:
            return redirect(url_for('cadastrar_produtos'))
        else:
            return redirect(url_for('erro_login'))

    return redirect(url_for('index'))

@app.route('/cadastro_produtos')
def cadastrar_produtos():
    return render_template('cadastro_produtos.html')

@app.route('/erro_login')
def erro_login():
    return render_template('erro_login.html')

@app.route('/sucesso_login')
def sucesso_login():
    return render_template('sucesso_login.html')

@app.route('/contato')
def contato():
    return render_template('contatos.html')

@app.route('/excluir_produto/<int:id>', methods=['POST'])
def excluir_produto(id):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Produtos WHERE id = ?", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return redirect(url_for('produtos'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        cor = request.form['cor']
        preco = request.form['preco']
        cursor.execute("UPDATE Produtos SET Nome=?, Descricao=?, Cor=?, Preco=? WHERE id=?", (nome, descricao, cor, preco, id))
        conexao.commit()
        cursor.close()
        conexao.close()
        return redirect(url_for('produtos'))

    cursor.execute("SELECT * FROM Produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    cursor.close()
    conexao.close()
    return render_template('editar.html', produto=produto)

@app.route('/produtos')
def produtos():
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Produtos")
    produtos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('produtos.html', produtos=produtos)

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    cor = request.form['cor']
    preco = request.form['preco']

    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO Produtos (Nome, Descricao, Cor, Preco) VALUES (?, ?, ?, ?)", (nome, descricao, cor, preco))
    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect(url_for('cadastro_produtos'))

if __name__ == '__main__':
    app.run(debug=True)