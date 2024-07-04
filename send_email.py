from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import streamlit as st

def sender_email(email, nombre, fecha, hora, seleccionado, tema, notas):
    # Credenciales
    user = st.secrets["emails"]["smtp_user"]
    password = st.secrets["emails"]["smtp_password"]

    sender_email = "Montenegro Editores"

    # Configuración del servidor SMTP de Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Construir el mensaje MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Reserva de capacitación"

    # Cuerpo del mensaje
    message = f"""
    Hola {nombre},
    Su reserva ha sido realizada con éxito.
    Fecha: {fecha}
    Hora: {hora}
    Capacitador: {seleccionado}
    Temas: {tema}
    Notas: {notas}

    Gracias por confiar en nosotros.
    Un saludo.
    """

    # Adjuntar el cuerpo del mensaje al mensaje MIME
    msg.attach(MIMEText(message, 'plain'))

    # Intentar enviar el correo electrónico
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(sender_email, email, msg.as_string())

        st.success("Email enviado correctamente")

    except smtplib.SMTPException as e:
        st.exception("Error al enviar el email")

# Ejemplo de uso
# send_email("correo_destino@example.com", "Nombre", "2024-07-01", "10:00", "Edgar Santiago", "Tema 1 Edgar", "Notas adicionales")
