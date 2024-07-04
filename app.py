import streamlit as st
from streamlit_option_menu import option_menu
from send_email import sender_email
from google_sheets import GoogleSheets
from google_Calendary import GoogleCalendar  # Asumiendo que el nombre del archivo es google_calendar.py
import re
import uuid
import numpy as np
import datetime as dt


##VARIABLES
page_title = "Montenegro"
page_icon = ";"
layout = "centered"

horas = ["09:00", "10:30", "12:00", "13:30", "16:00", "17:30"]
capacitador = ["Edgar Santiago", "Julio Rubio", "Roxana Gónzales"]

# Temas por capacitador
temas_edgar = ["Tema 1 Edgar", "Tema 2 Edgar", "Tema 3 Edgar"]
temas_julio = ["Tema 1 Julio", "Tema 2 Julio", "Tema 3 Julio"]
temas_roxana = ["Tema 1 Roxana", "Tema 2 Roxana", "Tema 3 Roxana"]
temas_eduardo = ["Tema 1 Eduardo", "Tema 2 Eduardo", "Tema 3 Eduardo"]

##hojas de calculo
document = "Agenda-Montenegro"
sheet = "Capacitaciones"
credentials = st.secrets["google"]["credentials_sheet"]
idcalendar = "intzinjose1498472@gmail.com"
idcalendar2 = "9835ed681edd02ebf9c1800f77a885dca4520a422436db52d8dea43aff5f3664@group.calendar.google.com"
idcalendar3 = "468029ea954e32491d1ecefcb2f20d797de2cb0a350163f59a1e696489e49a55@group.calendar.google.com"
time_zone = "America/Mexico_City"

##Funciones
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def generate_uid():
    return str(uuid.uuid4())

def add_hour_and_half(time):
    parsed_time = dt.datetime.strptime(time, "%H:%M").time()
    new_time = (dt.datetime.combine(dt.date.today(), parsed_time) + dt.timedelta(hours=1, minutes=30)).time()
    return new_time.strftime("%H:%M")

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

st.image("assets/logo.png")
st.title("Agenda de Capacitaciones de Montenegro Editores Tecnología")
st.text("Av Topacio 2805, Verde Valle, 44550 Guadalajara, Jal.")

selected = option_menu(menu_title=None, options=["Reservar", "Pistas", "Detalles"],
                       icons=["calendar-date", "building", "clipboard-minus"],
                       orientation="horizontal")

if selected == "Detalles":
    st.subheader("Ubicación")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d59740.35012961662!2d-103.4000536!3d20.638153!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8428ae11f357b8ff%3A0x9346f3cfb13bd0c5!2sMontenegro%20Editores!5e0!3m2!1ses-419!2smx!4v1719530558329!5m2!1ses-419!2smx" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
    st.markdown("Pulsa, [aquí](https://www.google.com/maps/place/Montenegro+Editores/@20.638153,-103.4000536,13z/data=!4m10!1m2!2m1!1smontenegro+editores!3m6!1s0x8428ae11f357b8ff:0x9346f3cfb13bd0c5!8m2!3d20.6450088!4d-103.3943315!15sChNtb250ZW5lZ3JvIGVkaXRvcmVzkgEJcHVibGlzaGVy4AEA!16s%2Fg%2F11bwf6pqg1?entry=ttu) para ver la dirección")

    st.subheader("Horarios")
    st.write("Lunes - Viernes: 08:00 - 19:00")
    st.write("Sábado: 09:00 - 13:00")
    st.write("Domingo: Cerrado")

    st.subheader("Contacto")
    st.text("Teléfono: 333017715")

    st.subheader("Instagram")
    st.markdown("Síguenos [aquí](https://www.instagram.com/montenegro_editores/)")

if selected == "Pistas":
    st.write("##")
    st.image("assets/cuentacuentos.png", caption="Esta es una de nuestras pistas")
    st.image("assets/derecho-ambiental.png", caption="Esta es una de nuestras pistas")
    st.image("assets/equipo.png", caption="Esta es una de nuestras pistas")
    st.image("assets/esperando.png", caption="Esta es una de nuestras pistas")

if selected == "Reservar":
    st.subheader("Reservar")
    c1, c2 = st.columns(2)
    nombre = c1.text_input("Tu Nombre", placeholder="Nombre")
    email = c2.text_input("Tu email", placeholder="Correo electrónico")
    fecha = c1.date_input("Fecha")
    seleccionado = c2.selectbox("Capacitador", capacitador)

    if seleccionado == "Edgar Santiago":
        tema = c1.selectbox("Temas", temas_edgar)
        calendar_id = idcalendar
    elif seleccionado == "Julio Rubio":
        tema = c1.selectbox("Temas", temas_julio)
        calendar_id = idcalendar2
    elif seleccionado == "Roxana Gónzales":
        tema = c1.selectbox("Temas", temas_roxana)
        calendar_id = idcalendar3

    if fecha:
        calendar = GoogleCalendar(credentials, calendar_id)
        hours_blocked = calendar.get_events_start_time(str(fecha))
        result_hours = np.setdiff1d(horas, hours_blocked)

        hora = c2.selectbox("Hora", result_hours)

    notas = c1.text_area("Notas", placeholder="Describe algún tema específico sobre el cual quieres tratar.")
    enviar = st.button("Reservar")

    ## BACKEND Sheets
    if enviar:
        with st.spinner("Cargando..."):
            if nombre == "" or email == "":
                st.warning('El nombre y el correo electrónico son obligatorios.')
            elif not validate_email(email):
                st.warning("El correo electrónico no es válido.")
            else:
                #crear el evento en google calendar
                parsed_time = dt.datetime.strptime(hora, "%H:%M").time()
                hours1 = parsed_time.hour  
                print(hours1)
                minutes1 = parsed_time.minute
                print(minutes1)
                end_hours = add_hour_and_half(hora)
                parsed_time2 = dt.datetime.strptime(end_hours, "%H:%M").time()
                hours2 = parsed_time2.hour
                minutes2 = parsed_time2.minute
                start_time = dt.datetime(fecha.year,fecha.month,fecha.day, hours1-6, minutes1).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                end_time = dt.datetime(fecha.year,fecha.month,fecha.day, hours2-6, minutes2).astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
                calendar = GoogleCalendar(credentials,calendar_id)
                calendar.create_event(nombre,start_time,end_time,time_zone)
                #crear registros de sheet
                uid = generate_uid()
                data = [[nombre, email, str(fecha), hora, seleccionado, tema, notas, uid]]
                gs = GoogleSheets(credentials, document, sheet)
                range_data = gs.get_last_row_range()
                gs.write_data(range_data, data)
                sender_email(email, nombre, str(fecha), hora, seleccionado, tema, notas)
                st.success("Su cita ha sido reservada exitosamente.")
