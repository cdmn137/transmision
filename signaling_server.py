from flask import Flask, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Almacenar ofertas y respuestas SDP
sdp_data = {}

@socketio.on("offer")
def handle_offer(data):
    # Almacenar la oferta del remitente
    sender_id = data["sender_id"]
    sdp_data[sender_id] = data["offer"]
    # Enviar la oferta al receptor
    send({"sender_id": sender_id, "offer": data["offer"]}, room=data["receiver_id"])

@socketio.on("answer")
def handle_answer(data):
    # Almacenar la respuesta del receptor
    receiver_id = data["receiver_id"]
    sdp_data[receiver_id] = data["answer"]
    # Enviar la respuesta al remitente
    send({"receiver_id": receiver_id, "answer": data["answer"]}, room=data["sender_id"])

@socketio.on("connect")
def handle_connect():
    print(f"Usuario conectado: {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    print(f"Usuario desconectado: {request.sid}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)