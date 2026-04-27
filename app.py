from flask import Flask, request
import requests
from bot import processar_mensagem

app = Flask(__name__)

VERIFY_TOKEN = "meu_token_123"
ACCESS_TOKEN = "Seu token de acesso"
PHONE_NUMBER_ID = "seu ID de telefone"


@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge

    return "Token inválido", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return "ok", 200

        mensagem = value["messages"][0]
        numero = mensagem["from"]
        texto = mensagem["text"]["body"]

        print(f"Mensagem recebida: {texto}")

        resposta = processar_mensagem(texto, numero)
        responder(numero, resposta)

    except Exception as erro:
        print("ERRO NO WEBHOOK:", erro)

    return "ok", 200


def responder(numero, mensagem):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print("STATUS:", response.status_code)
    print("RESPOSTA:", response.text)


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
