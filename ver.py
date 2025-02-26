import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode

def main():
    st.title("Transmisión en Directo con Streamlit y WebRTC")

    st.write("""
    Esta es una aplicación básica que te permite transmitir tu cámara y audio en directo.
    Otra persona puede ver tu transmisión accediendo a esta misma URL.
    """)

    # Configuración de WebRTC para la transmisión
    webrtc_ctx = webrtc_streamer(
        key="broadcast",
        mode=WebRtcMode.SENDONLY,  # Solo transmite, no recibe
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
        media_stream_constraints={
            "video": True,
            "audio": True
        }
    )

    if webrtc_ctx.state.playing:
        st.write("¡Transmisión en vivo activada! Otra persona puede ver tu transmisión.")

if __name__ == "__main__":
    main()