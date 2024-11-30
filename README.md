# Quiz Game &#127918; - Jogo de Perguntas e Respostas

Este projeto é um **Jogo de Perguntas e Respostas** simples criado com **Flask** (para o backend), **MySQL** (para o banco de dados) e **HTML/CSS** (para o frontend). O objetivo do jogo é testar os conhecimentos do usuário com perguntas sobre programação em Python, com um sistema de pontuação que é armazenado no banco de dados.

## Funcionalidades

- Cadastro de jogadores.
- Perguntas e respostas de múltipla escolha.
- Sistema de pontuação.
- Armazenamento de dados dos jogadores no banco de dados.
- Exibição de resultados ao final do quiz.

## Tecnologias Utilizadas

- **Flask**: Framework para desenvolvimento web em Python.
- **MySQL**: Sistema de gerenciamento de banco de dados.
- **HTML/CSS**: Linguagens para estruturar e estilizar o frontend.
- **Python**: Linguagem principal para a lógica do backend.
- **figma**:Para o esboço do projeto do desing do projeto.
  [Design no Figma](https://www.figma.com/design/rfI8XbMvqRqWPVbb7CSULt/Untitled?node-id=0-1&t=4bYENdfheLTWOQI9-1)


## Estrutura do Projeto

O projeto é composto pelas seguintes partes:

1. **Banco de Dados**: Tabelas para armazenar perguntas, respostas e dados dos jogadores.
2. **Backend (Flask)**: Controla o fluxo do quiz e interage com o banco de dados.
3. **Frontend (HTML/CSS)**: Interface de usuário para interação com o quiz.

## Pré-requisitos

- **Python 3.7+**
- **MySQL** (ou MariaDB)
- **Bibliotecas Python**:
  - Flask
  - mysql-connector-python

### Instalação

1. **Clone o repositório**:
    ```bash
    git clone https://github.com/seu-usuario/quiz-game.git
    cd quiz-game
    ```

2. **Instale as dependências**:
    Crie um ambiente virtual e instale as dependências necessárias.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows use venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configure o banco de dados**:
    - Acesse o MySQL e crie o banco de dados `quiz_game`:
      ```sql
      CREATE DATABASE quiz_game;
      ```

    - Crie as tabelas necessárias executando os seguintes comandos SQL:
      ```sql
      USE quiz_game;

      CREATE TABLE questions (
          id INT AUTO_INCREMENT PRIMARY KEY,
          question TEXT NOT NULL,
          responder1 TEXT NOT NULL,
          responder2 TEXT NOT NULL,
          responder3 TEXT NOT NULL,
          responder4 TEXT NOT NULL,
          correta_responder INT NOT NULL
      );

      CREATE TABLE players (
          id INT AUTO_INCREMENT PRIMARY KEY,
          username VARCHAR(100) NOT NULL,
          points INT DEFAULT 0
      );

      INSERT INTO questions (question, responder1, responder2, responder3, responder4, correta_responder) VALUES
      ('O que o seguinte código faz? \nx = 3\nx += 2\nprint(x)', 'a) Imprime 3', 'b) Imprime 5', 'c) Imprime 2', 'd) Lança um erro', 2),
      ('O que o operador // faz em Python?', 'a) Realiza a divisão comum', 'b) Realiza a divisão e arredonda para o número inteiro mais próximo', 'c) Realiza a divisão inteira (descarta a parte decimal)', 'd) Multiplica os números', 3),
      ('Qual é a saída do seguinte código? \nx = 10\nif x > 5:\nprint("Maior que 5")\nelse:\nprint("Menor ou igual a 5")', 'a) Maior ou igual a 5', 'b) Menor ou igual a 5', 'c) Maior que 5', 'd) Não imprime nada', 3);
      ```

4. **Configuração do MySQL**:
    Altere as credenciais de conexão com o banco de dados MySQL no código do Flask. No arquivo `app.py`, modifique a função `get_db_connection()` com as informações do seu banco de dados:
    ```python
    def get_db_connection():
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sua_senha',
            database='quiz_game'
        )
        return conn
    ```

5. **Executando o servidor Flask**:
    Execute o servidor Flask para iniciar o quiz.
    ```bash
    python app.py
    ```

    O aplicativo estará disponível em `http://127.0.0.1:5000/`.

## Como Jogar

1. **Acesse o jogo**: Abra o navegador e acesse `http://127.0.0.1:5000/`.
2. **Cadastre-se**: Digite seu nome para começar o quiz.
3. **Responda às Perguntas**: O quiz apresenta perguntas com quatro alternativas. Escolha a alternativa correta.
4. **Veja o Resultado**: Ao final do quiz, o jogo exibe a sua pontuação e atualiza o banco de dados com o seu nome e pontuação.

## Exemplo de Funcionamento

1. **Página de Início**:

    Ao acessar a URL do jogo, você verá um formulário para inserir seu nome.

    ![Página de Início](https://via.placeholder.com/600x400.png?text=Página+de+Início)

2. **Quiz de Perguntas**:

    Durante o quiz, você verá as perguntas e poderá selecionar uma resposta.

    ![Página de Pergunta](https://via.placeholder.com/600x400.png?text=Quiz+de+Perguntas)

3. **Resultado Final**:

    Após responder todas as perguntas, o jogo exibirá o seu resultado final.

    ![Página de Resultados](https://via.placeholder.com/600x400.png?text=Resultado+Final)

## Estrutura do Código

### Banco de Dados

O banco de dados `quiz_game` tem duas tabelas principais:

- **questions**: Armazena as perguntas e alternativas do quiz.
    - `id`: Identificador da pergunta.
    - `question`: Texto da pergunta.
    - `responder1`, `responder2`, `responder3`, `responder4`: Alternativas de resposta.
    - `correta_responder`: Índice da alternativa correta (1 a 4).

- **players**: Armazena informações dos jogadores e suas pontuações.
    - `id`: Identificador do jogador.
    - `username`: Nome do jogador.
    - `points`: Pontuação do jogador.

### Backend (Flask)

A aplicação Flask gerencia a lógica do quiz, incluindo o registro de jogadores, apresentação de perguntas e cálculo da pontuação. A aplicação usa **MySQL** para armazenar os dados dos jogadores e perguntas.

Exemplo de configuração do Flask:

```python
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
