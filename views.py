from main import app
import csv
from flask import Flask, render_template, url_for, request, redirect
from dotenv import load_dotenv
import google.generativeai as genai
import os
import markdown

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


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

@app.route('/pergunta', methods=['GET', 'POST'])
def pergunta():
    resposta = ""
    if request.method == 'POST':
        pergunta_usuario = request.form['pergunta']
        try:
            resposta = model.generate_content(pergunta_usuario).text
        except Exception as e:
            resposta = f"Ocorreu um erro: {e}"
        resposta=markdown.markdown(resposta)
    return render_template('pergunta.html', resposta=resposta)

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

@app.route('/editar-termo/<termo>', methods=['GET', 'POST'])
def editar_termo(termo):
    termos_atualizados = []

    if request.method == 'POST':
        novo_termo = request.form['novo_termo']
        nova_definicao = request.form['nova_definicao']

        with open('dicionario.csv', 'r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for linha in reader:
                if linha[0] == termo:
                    # Substitui por novo termo e nova definição
                    termos_atualizados.append([novo_termo, nova_definicao])
                else:
                    termos_atualizados.append(linha)

        with open('dicionario.csv', 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerows(termos_atualizados)

        return redirect(url_for('dicionario'))

    # Buscar definição atual
    definicao_atual = ''
    with open('dicionario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            if linha[0] == termo:
                definicao_atual = linha[1]
                break

    return render_template('editar_termo.html', termo=termo, definicao=definicao_atual)

@app.route('/deletar-termo/<termo>', methods=['POST'])
def deletar_termo(termo):
    termos_restantes = []

    with open('dicionario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            if linha[0] != termo:
                termos_restantes.append(linha)

    with open('dicionario.csv', 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerows(termos_restantes)

    return redirect(url_for('dicionario'))
