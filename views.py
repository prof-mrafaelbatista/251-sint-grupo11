from main import app
import csv
from flask import Flask, render_template, url_for, request, redirect

@app.route('/')
def homepage():
    return render_template("homepage.html")

@app.route('/selecao')
def selecao():
    return render_template("selecao.html")

@app.route('/repeticao')
def repeticao():
    return render_template("repeticao.html")

@app.route('/vetores')
def vetores():
    return render_template("vetores.html")

@app.route('/funcoes')
def funcoes():
    return render_template("funcoes.html")

@app.route('/pergunta')
def pergunta():
    return render_template("pergunta.html")

@app.route('/dicionario')
def dicionario():

    dicionario_de_termos = []

    with open('dicionario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            dicionario_de_termos.append(linha)

    return render_template('dicionario.html', dicionario=dicionario_de_termos)

@app.route('/novo-termo')
def novo_termo():
    return render_template('novo_termo.html')

@app.route('/criar_termo', methods=['POST'])
def criar_termo():

    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('dicionario.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('dicionario'))









