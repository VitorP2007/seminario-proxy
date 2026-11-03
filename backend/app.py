from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def inicio():

    return jsonify({
        "mensagem": "Backend funcionando!",
        "aplicacao": "Projeto Proxy Reverso",
        "status": "Online",

        # Informacoes da comunicacao
        "ip_visto_pelo_backend": request.remote_addr,
        "ip_encaminhado": request.headers.get("X-Real-IP"),
        "x_forwarded_for": request.headers.get("X-Forwarded-For")
    })


@app.route("/sobre", methods=["GET"])
def sobre():

    return jsonify({
        "projeto": "Demonstracao de Proxy Reverso",
        "linguagem": "Python",
        "framework": "Flask"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )