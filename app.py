from flask import Flask, request, jsonify
from flask_cors import CORS

import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/pague")
def exiba_mensagem():
    return "<h2>Oii</h2>"


def init_db():
    # CONECTE O SQLITE3 NO ARQUIVO DATABASE.DB COM A VARIÁVEL CONN (CONNECTION)
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
             )
""")


init_db()


@app.route("/doar", methods=["POST"])
def doar():

    dados = request.get_json()
    print(f"AQUI ESTÃO OS DADOS RETORNADOS DO CLIENTE {dados}")

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    if not titulo or not categoria or not autor or not image_url:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:

        conn.execute(f"""
        INSERT INTO LIVROS (titulo,categoria,autor,image_url)
        VALUES ("{titulo}", "{categoria}", "{autor}", "{image_url}")
""")

    conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201


@app.route("/livros", methods=["GET"])
def listar_livros():

    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

    livros_formatados = []

    for item in livros:
        dicionario_livros = {
            "id": item[0],               # ID do livro
            "titulo": item[1],           # Título do livro
            "categoria": item[2],        # Categoria do livro
            "autor": item[3],            # Autor do livro
            "image_url": item[4]         # URL da imagem do livro
        }
        # Adicionamos o dicionário à lista final
        livros_formatados.append(dicionario_livros)

    # Retornamos a lista de livros como JSON com o status 200 (OK)
    return jsonify(livros_formatados), 200

# Se o app.py for o arquivo principal da API:
# Execute o app.run com o modo debug ativado
if __name__ == "__main__":
    app.run(debug=True)
