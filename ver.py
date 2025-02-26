import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import socketio

# Configuración del servidor de señalización
SIGNALING_SERVER_URL = "https://signaling-server-5voq.onrender.com"
sio = socketio.Client()

# Configuración de WebRTC
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Estado de la aplicación
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "peer_id" not in st.session_state:
    st.session_state.peer_id = None

# Conectar al servidor de señalización
def connect_to_signaling_server():
    try:
        sio.connect(SIGNALING_SERVER_URL)
        st.session_state.user_id = sio.sid
        st.success("Conectado al servidor de señalización.")
    except Exception as e:
        st.error(f"Error al conectar al servidor de señalización: {e}")

# Manejar ofertas y respuestas SDP
@sio.on("offer")
def handle_offer(data):
    st.session_state.peer_id = data["sender_id"]
    st.write(f"Oferta recibida de {data['sender_id']}")

@sio.on("answer")
def handle_answer(data):
    st.session_state.peer_id = data["receiver_id"]
    st.write(f"Respuesta recibida de {data['receiver_id']}")

def main():
    st.title("Transmisión en Directo con Streamlit y WebRTC")
    usuario = st.text_input("Ingrese su Usuario")
    if usuario != "":
        st.session_state.user_id = usuario

    if not st.session_state.user_id:
        connect_to_signaling_server()

    if st.session_state.user_id:
        st.write(f"Tu ID de usuario: {st.session_state.user_id}")

        # Ingresar el ID del otro usuario
        peer_id = st.text_input("Ingresa el ID del otro usuario:")
        if peer_id:
            st.session_state.peer_id = peer_id

        # Iniciar la transmisión
        if st.session_state.peer_id:
            webrtc_ctx = webrtc_streamer(
                key="broadcast",
                mode=WebRtcMode.SENDRECV,  # Transmite y recibe
                rtc_configuration=RTC_CONFIGURATION,
                media_stream_constraints={"video": True, "audio": True},
            )

            if webrtc_ctx.state.playing:
                st.write("¡Transmisión en vivo activada! Otra persona puede ver tu transmisión.")

if __name__ == "__main__":
    main()