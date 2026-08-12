import streamlit as st
from datetime import date
from supabase import create_client, Client


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="TCSalud",
    page_icon="🏥",
    layout="wide"
)


# =========================================================
# CONEXIÓN CON SUPABASE
# =========================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
    }

    .logo {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: #167c80;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FUNCIONES
# =========================================================

def obtener_profesional():

    try:

        usuario = st.session_state.usuario

        respuesta = (
            supabase
            .table("profesionales")
            .select("*")
            .eq("auth_user_id", usuario["id"])
            .limit(1)
            .execute()
        )

        if respuesta.data:

            return respuesta.data[0]

        return None

    except Exception as error:

        st.error(
            f"No se pudo obtener el profesional: {error}"
        )

        return None


def obtener_pacientes(profesional_id):

    try:

        respuesta = (
            supabase
            .table("pacientes")
            .select("*")
            .eq("profesional_id", profesional_id)
            .order("apellido")
            .execute()
        )

        return respuesta.data or []

    except Exception as error:

        st.error(
            f"No se pudieron cargar los pacientes: {error}"
        )

        return []


def crear_paciente(
    profesional_id,
    nombre,
    apellido,
    dni,
    fecha_nacimiento,
    telefono,
    email,
    obra_social,
    motivo
):

    try:

        datos = {
            "profesional_id": profesional_id,
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "fecha_nacimiento": str(fecha_nacimiento),
            "telefono": telefono,
            "email": email,
            "obra_social": obra_social,
            "motivo_consulta": motivo,
            "estado": "activo"
        }

        respuesta = (
            supabase
            .table("pacientes")
            .insert(datos)
            .execute()
        )

        return respuesta.data

    except Exception as error:

        st.error(
            f"No se pudo guardar el paciente: {error}"
        )

        return None


# =========================================================
# LOGIN
# =========================================================

def pantalla_login():

    st.markdown(
        '<div class="logo">🏥 TCSalud</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Gestión profesional para tu consultorio'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Iniciar sesión")

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Contraseña",
            type="password"
        )

        if st.button(
            "Ingresar",
            use_container_width=True
        ):

            try:

                respuesta = supabase.auth.sign_in_with_password(
                    {
                        "email": email,
                        "password": password
                    }
                )

                if respuesta.user:

                    st.session_state.usuario = {
                        "id": respuesta.user.id,
                        "email": respuesta.user.email
                    }

                    st.rerun()

            except Exception:

                st.error(
                    "Email o contraseña incorrectos."
                )


# =========================================================
# LISTA DE PACIENTES
# =========================================================

def pantalla_pacientes(profesional):

    st.title("👥 Pacientes")

    st.write(
        "Administrá los pacientes de tu consultorio."
    )

    pacientes = obtener_pacientes(
        profesional["id"]
    )

    pestaña_lista, pestaña_nuevo = st.tabs(
        [
            "📋 Pacientes",
            "➕ Nuevo paciente"
        ]
    )


    # =====================================================
    # LISTA
    # =====================================================

    with pestaña_lista:

        buscar = st.text_input(
            "🔎 Buscar paciente",
            placeholder="Nombre, apellido o DNI"
        )

        pacientes_filtrados = pacientes

        if buscar:

            texto = buscar.lower()

            pacientes_filtrados = [
                paciente
                for paciente in pacientes
                if texto in (
                    paciente["nombre"]
                    + " "
                    + paciente["apellido"]
                    + " "
                    + (paciente["dni"] or "")
                ).lower()
            ]


        if not pacientes_filtrados:

            st.info(
                "Todavía no hay pacientes registrados."
            )

        else:

            for paciente in pacientes_filtrados:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [3, 2, 1]
                    )

                    with col1:

                        st.subheader(
                            f"{paciente['nombre']} "
                            f"{paciente['apellido']}"
                        )

                        st.write(
                            f"DNI: {paciente['dni'] or '-'}"
                        )

                    with col2:

                        st.write(
                            f"🏥 Obra social: "
                            f"{paciente.get('obra_social') or '-'}"
                        )

                        st.write(
                            f"📞 {paciente.get('telefono') or '-'}"
                        )

                    with col3:

                        if st.button(
                            "Ver ficha",
                            key=f"paciente_{paciente['id']}"
                        ):

                            st.session_state.paciente_seleccionado = paciente

                            st.rerun()


    # =====================================================
    # NUEVO PACIENTE
    # =====================================================

    with pestaña_nuevo:

        st.subheader(
            "➕ Registrar paciente"
        )

        nombre = st.text_input(
            "Nombre *"
        )

        apellido = st.text_input(
            "Apellido *"
        )

        dni = st.text_input(
            "DNI"
        )

        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento",
            value=date(1990, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )

        telefono = st.text_input(
            "Teléfono"
        )

        email = st.text_input(
            "Email"
        )

        obra_social = st.text_input(
            "Obra social"
        )

        motivo = st.text_area(
            "Motivo de consulta"
        )

        if st.button(
            "💾 Guardar paciente",
            use_container_width=True
        ):

            if not nombre or not apellido:

                st.error(
                    "Nombre y apellido son obligatorios."
                )

            else:

                resultado = crear_paciente(
                    profesional["id"],
                    nombre,
                    apellido,
                    dni,
                    fecha_nacimiento,
                    telefono,
                    email,
                    obra_social,
                    motivo
                )

                if resultado:

                    st.success(
                        "✅ Paciente guardado correctamente."
                    )

                    st.rerun()


# =========================================================
# FICHA DEL PACIENTE
# =========================================================

def pantalla_ficha(paciente):

    st.title(
        f"👤 {paciente['nombre']} "
        f"{paciente['apellido']}"
    )

    if st.button(
        "← Volver a pacientes"
    ):

        st.session_state.paciente_seleccionado = None

        st.rerun()

    st.divider()

    st.subheader("📋 Datos del paciente")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Nombre:** "
            f"{paciente['nombre']} "
            f"{paciente['apellido']}"
        )

        st.write(
            f"**DNI:** "
            f"{paciente['dni'] or '-'}"
        )

        fecha = paciente.get(
            "fecha_nacimiento"
        )

        if fecha:

            try:

                fecha_formateada = date.fromisoformat(
                    str(fecha)
                ).strftime("%d/%m/%Y")

            except Exception:

                fecha_formateada = str(fecha)

        else:

            fecha_formateada = "-"

        st.write(
            f"**Fecha de nacimiento:** "
            f"{fecha_formateada}"
        )

        st.write(
            f"**Teléfono:** "
            f"{paciente.get('telefono') or '-'}"
        )


    with col2:

        st.write(
            f"**Email:** "
            f"{paciente.get('email') or '-'}"
        )

        st.write(
            f"**Obra social:** "
            f"{paciente.get('obra_social') or '-'}"
        )

        st.write(
            f"**Motivo de consulta:** "
            f"{paciente.get('motivo_consulta') or '-'}"
        )

        st.write(
            f"**Estado:** "
            f"{paciente.get('estado') or 'activo'}"
        )

    st.divider()

    st.subheader("📝 Evoluciones")

    st.info(
        "Todavía no hay evoluciones registradas."
    )

    if st.button(
        "➕ Nueva evolución",
        use_container_width=True
    ):

        st.info(
            "El módulo de evoluciones lo "
            "vamos a activar en el siguiente paso."
        )


# =========================================================
# PANEL PRINCIPAL
# =========================================================

def dashboard(profesional):

    st.sidebar.title("🏥 TCSalud")

    st.sidebar.write(
        f"👤 {profesional['nombre']} "
        f"{profesional['apellido']}"
    )

    st.sidebar.caption(
        profesional.get("profesion")
        or "Profesional de la salud"
    )

    st.sidebar.divider()

    opcion = st.sidebar.radio(
        "Menú",
        [
            "🏠 Inicio",
            "👥 Pacientes",
            "📝 Evoluciones",
            "📅 Agenda",
            "📊 Estadísticas",
            "⚙️ Configuración"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Cerrar sesión",
        use_container_width=True
    ):

        supabase.auth.sign_out()

        st.session_state.clear()

        st.rerun()


    # =====================================================
    # INICIO
    # =====================================================

    if opcion == "🏠 Inicio":

        pacientes = obtener_pacientes(
            profesional["id"]
        )

        st.title("Buen día 👋")

        st.write(
            "Bienvenido al panel profesional de TCSalud."
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "👥 Pacientes",
                len(pacientes)
            )

        with col2:

            st.metric(
                "📅 Sesiones hoy",
                "0"
            )

        with col3:

            st.metric(
                "📝 Evoluciones",
                "0"
            )

        with col4:

            st.metric(
                "📆 Próximos turnos",
                "0"
            )

        st.divider()

        st.subheader(
            "👥 Pacientes recientes"
        )

        if pacientes:

            for paciente in pacientes[:5]:

                st.write(
                    f"**{paciente['nombre']} "
                    f"{paciente['apellido']}**"
                )

        else:

            st.info(
                "Todavía no tenés pacientes registrados."
            )


    # =====================================================
    # PACIENTES
    # =====================================================

    elif opcion == "👥 Pacientes":

        if st.session_state.get(
            "paciente_seleccionado"
        ):

            pantalla_ficha(
                st.session_state.paciente_seleccionado
            )

        else:

            pantalla_pacientes(
                profesional
            )


    # =====================================================
    # EVOLUCIONES
    # =====================================================

    elif opcion == "📝 Evoluciones":

        st.title("📝 Evoluciones")

        st.info(
            "Este módulo será desarrollado "
            "a continuación."
        )


    # =====================================================
    # AGENDA
    # =====================================================

    elif opcion == "📅 Agenda":

        st.title("📅 Agenda")

        st.info(
            "El módulo de turnos será desarrollado "
            "a continuación."
        )


    # =====================================================
    # ESTADÍSTICAS
    # =====================================================

    elif opcion == "📊 Estadísticas":

        st.title("📊 Estadísticas")

        pacientes = obtener_pacientes(
            profesional["id"]
        )

        st.metric(
            "Total de pacientes",
            len(pacientes)
        )


    # =====================================================
    # CONFIGURACIÓN
    # =====================================================

    elif opcion == "⚙️ Configuración":

        st.title("⚙️ Configuración")

        st.subheader(
            "👤 Datos profesionales"
        )

        st.write(
            f"**Nombre:** "
            f"{profesional['nombre']} "
            f"{profesional['apellido']}"
        )

        st.write(
            f"**Email:** "
            f"{profesional['email']}"
        )

        st.write(
            f"**Profesión:** "
            f"{profesional.get('profesion') or '-'}"
        )

        st.write(
            f"**Matrícula:** "
            f"{profesional.get('matricula') or '-'}"
        )


# =========================================================
# CONTROL DE SESIÓN
# =========================================================

if "usuario" not in st.session_state:

    st.session_state.usuario = None

if "paciente_seleccionado" not in st.session_state:

    st.session_state.paciente_seleccionado = None


# =========================================================
# EJECUCIÓN
# =========================================================

if st.session_state.usuario is None:

    pantalla_login()

else:

    profesional = obtener_profesional()

    if profesional is None:

        st.error(
            "No encontramos un perfil profesional "
            "asociado a esta cuenta."
        )

        if st.button("Cerrar sesión"):

            supabase.auth.sign_out()

            st.session_state.clear()

            st.rerun()

    else:

        dashboard(profesional)