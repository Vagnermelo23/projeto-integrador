from flask import render_template, request, flash, redirect, url_for
from app import app
import mysql.connector
import os 

mydb = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST', 'localhost'),
    user=os.environ.get('MYSQL_USER', 'root'),
    port=os.environ.get('MYSQL_PORT', 3306),
    password=os.environ.get('MYSQL_PASSWORD', ''),
    database=os.environ.get('DB_DATABASE', 'db')
)

def get_available_dates():
    cursor = mydb.cursor()
    cursor.execute('SELECT datamc FROM cadastro')
    rows = cursor.fetchall()
    available_dates = [str(row[0]) for row in rows]
    return available_dates

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
        return redirect('/consulta')
    except mysql.connector.Error as err:
        flash(f"Erro ao cadastrar: {err}", "error")
        return redirect('/recemnascido')

@app.route('/autenticar4', methods=['POST'])
def autenticar4():
    datamc = request.form.get('datamc')
    nomedt = request.form.get('nomedt')
    cursor = mydb.cursor()

    cursor.execute('SELECT COUNT(*) FROM cadastro WHERE datamc = %s', (datamc,))
    result = cursor.fetchone()

    if result[0] > 0:
        flash("Já existe uma consulta marcada para esta data", "error")
        return redirect('/consulta')
    try:
        cursor.execute('INSERT INTO cadastro (datamc,nomedt) VALUES (%s,%s)', (datamc,nomedt))
        mydb.commit()
        cursor.close()
        flash("Consulta marcada", "successo")
        return redirect('/consulta')
    except mysql.connector.Error as err:
        flash(f"Erro ao marcar a consulta: {err}", "error")
        return redirect('/consulta')

@app.route('/consulta')
def consulta():
    available_dates = get_available_dates()
    return render_template('consulta.html', available_dates=available_dates)

