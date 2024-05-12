from flask import render_template, request, flash, redirect, url_for
from app import app
import mysql.connector
import os 

mydb = mysql.connector.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'root'),
    port=os.environ.get('DB_PORT', 3306),
    password=os.environ.get('DB_PASSWORD', ''),
    database=os.environ.get('DB_DATABASE', 'db')
)

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/idoso')
def idoso():
    return render_template('idoso.html')

@app.route('/gestante')
def gestante():
    return render_template('gestante.html')

@app.route('/recemnascido')
def recemnascido():
    return render_template('recemnascido.html')

@app.route('/autenticar3', methods=['POST'])
def autenticar3():
    nome = request.form.get('nome')
    datanc = request.form.get('datanc')
    sexo = request.form.get('sexo')
    peso = request.form.get('peso')

    cursor = mydb.cursor()
    try:
        cursor.execute('INSERT INTO cadastro (nome, datanc, mf, peso) VALUES (%s, %s, %s, %s)',
                       (nome, datanc, sexo, peso))
        mydb.commit()
        cursor.close()
        flash("Cadastro confirmado", "success")
        return redirect('/recemnascido')
    except mysql.connector.Error as err:
        flash(f"Erro ao cadastrar: {err}", "error")
        return redirect('/recemnascido')
