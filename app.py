from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',   # Altere para o seu host, se necessário
        user='root',        # Seu usuário do MySQL
        password='', # Sua senha do MySQL
        database='quiz_game'
    )
    return conn

# Página inicial para o cadastro do jogador
@app.route('/')
def index():
    return render_template('inicio.html')

# Página para começar o quiz
@app.route('/start', methods=['POST'])
def start():
    username = request.form['username']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (username) VALUES (%s)", (username,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('quiz', player=username, question_num=1, points=0))

# Página do quiz com perguntas
@app.route('/quiz/<player>/<int:question_num>/<int:points>', methods=['GET', 'POST'])
def quiz(player, question_num, points):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtendo a pergunta atual
    cursor.execute("SELECT * FROM questions WHERE id = %s", (question_num,))
    question = cursor.fetchone()

    if not question:
        return redirect(url_for('result.html', player=player, points=points))

    # Verificando a resposta e atualizando a pontuação
    if request.method == 'POST':
        responder = int(request.form['responder'])
        correta_responder = question[6]  # A resposta correta está na coluna 6 (índice 6)

        if responder == correta_responder:
            points += 1

        # Próxima pergunta
        return redirect(url_for('quiz', player=player, question_num=question_num + 1, points=points))

    cursor.close()
    conn.close()

    # Renderizando a página com a pergunta e as opções
    return render_template('quiz.html', question=question, player=player, question_num=question_num, points=points)

# Página de resultado final
@app.route('/result/<player>/<int:points>')
def result(player, points):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Atualizando a pontuação do jogador no banco de dados
    cursor.execute("UPDATE players SET points = %s WHERE username = %s", (points, player))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('result.html', player=player, points=points)

if __name__== '__main__':
    app.run(debug=True)

   
