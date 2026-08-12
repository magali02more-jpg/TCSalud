import streamlit as st

# ==============================
# CONFIGURACIÓN
# ==============================

st.set_page_config(
    page_title="TCSalud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# ESTILOS
# ==============================

st.markdown("""
<style>

    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
    }

    .logo {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        color: #167c80;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .card-title {
        color: #6b7280;
        font-size: 14px;
    }

    .card-number {
        color: #111827;
        font-size: 30px;
        font-weight: 700;
    }

</style>
""", unsafe_allow_html=True)


# ==============================
# LOGIN
# ==============================

if "logueado" not in st.session_state:
    st.session_state.logueado = False


def pantalla_login():

    st.markdown(
        '<div class="logo">🏥 TCSalud</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Gestión profesional para salud</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Iniciar sesión")

        usuario = st.text_input(
            "Usuario o email",
            placeholder="Ingresá tu usuario"
        )

        contraseña = st.text_input(
            "Contraseña",
            type="password",
            placeholder="Ingresá tu contraseña"
        )

        ingresar = st.button(
            "Ingresar",
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if ingresar:

            # Usuario de prueba
            if usuario == "demo" and contraseña == "1234":

                st.session_state.logueado = True
                st.rerun()

            else:

                st.error(
                    "Usuario o contraseña incorrectos."
                )

        st.caption(
            "Demo: usuario **demo** · contraseña **1234**"
        )


# ==============================
# DASHBOARD
# ==============================

def dashboard():

    st.sidebar.title("🏥 TCSalud")

    st.sidebar.caption(
        "Gestión profesional"
    )

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

        st.session_state.logueado = False
        st.rerun()


    # ==========================
    # INICIO
    # ==========================

    if opcion == "🏠 Inicio":

        st.title("Buen día 👋")

        st.write(
            "Bienvenido al panel profesional de TCSalud."
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Pacientes",
                "48"
            )

        with col2:
            st.metric(
                "📅 Sesiones hoy",
                "6"
            )

        with col3:
            st.metric(
                "📝 Evoluciones",
                "3"
            )

        with col4:
            st.metric(
                "📆 Próximos turnos",
                "4"
            )

        st.divider()

        st.subheader("📅 Próximos turnos")

        st.info(
            "14:00 — María González — Sesión"
        )

        st.info(
            "15:00 — Juan Pérez — Seguimiento"
        )

        st.info(
            "16:30 — Ana Rodríguez — Sesión"
        )


    # ==========================
    # PACIENTES
    # ==========================

    elif opcion == "👥 Pacientes":

        st.title("👥 Pacientes")

        st.write(
            "Desde acá podrás administrar tus pacientes."
        )

        st.button(
            "➕ Nuevo paciente",
            use_container_width=True
        )

        st.text_input(
            "🔎 Buscar paciente",
            placeholder="Nombre, apellido o DNI"
        )

        st.info(
            "El módulo de pacientes se conectará "
            "a la base de datos en la próxima etapa."
        )


    # ==========================
    # EVOLUCIONES
    # ==========================

    elif opcion == "📝 Evoluciones":

        st.title("📝 Evoluciones")

        st.write(
            "Historial de evoluciones de los pacientes."
        )

        st.info(
            "Acá construiremos el registro de cada sesión."
        )


    # ==========================
    # AGENDA
    # ==========================

    elif opcion == "📅 Agenda":

        st.title("📅 Agenda")

        st.info(
            "Acá construiremos el calendario "
            "de turnos profesionales."
        )


    # ==========================
    # ESTADÍSTICAS
    # ==========================

    elif opcion == "📊 Estadísticas":

        st.title("📊 Estadísticas")

        st.info(
            "Las estadísticas aparecerán cuando "
            "tengamos datos reales en la base de datos."
        )


    # ==========================
    # CONFIGURACIÓN
    # ==========================

    elif opcion == "⚙️ Configuración":

        st.title("⚙️ Configuración")

        st.subheader(
            "Datos del profesional"
        )

        st.text_input(
            "Nombre"
        )

        st.text_input(
            "Profesión"
        )

        st.text_input(
            "Matrícula"
        )

        st.button(
            "Guardar cambios"
        )


# ==============================
# EJECUCIÓN
# ==============================

if st.session_state.logueado:

    dashboard()

else:

    pantalla_login()