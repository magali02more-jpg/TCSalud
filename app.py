import streamlit as st
from datetime import date

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="TCSalud",
    page_icon="🏥",
    layout="wide"
)

# ==========================================
# ESTILOS
# ==========================================

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
}

.subtitle {
    text-align: center;
    color: #6b7280;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# DATOS DE PRUEBA
# ==========================================

if "pacientes" not in st.session_state:

    st.session_state.pacientes = [
        {
            "id": 1,
            "nombre": "María",
            "apellido": "González",
            "dni": "35123456",
            "fecha_nacimiento": "12/05/1990",
            "telefono": "3515555555",
            "email": "maria@email.com",
            "motivo": "Seguimiento",
            "fecha_ingreso": "01/08/2026",
            "estado": "Activo"
        },
        {
            "id": 2,
            "nombre": "Juan",
            "apellido": "Pérez",
            "dni": "38456789",
            "fecha_nacimiento": "20/09/1988",
            "telefono": "3514444444",
            "email": "juan@email.com",
            "motivo": "Consulta inicial",
            "fecha_ingreso": "05/08/2026",
            "estado": "Activo"
        }
    ]


# ==========================================
# LOGIN
# ==========================================

if "logueado" not in st.session_state:
    st.session_state.logueado = False


def login():

    st.markdown(
        '<div class="logo">🏥 TCSalud</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Gestión profesional para tu consultorio</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("Iniciar sesión")

        usuario = st.text_input(
            "Usuario o email"
        )

        contraseña = st.text_input(
            "Contraseña",
            type="password"
        )

        if st.button(
            "Ingresar",
            use_container_width=True
        ):

            if usuario == "demo" and contraseña == "1234":

                st.session_state.logueado = True
                st.rerun()

            else:

                st.error(
                    "Usuario o contraseña incorrectos."
                )

        st.caption(
            "Demo: demo / 1234"
        )


# ==========================================
# DASHBOARD
# ==========================================

def dashboard():

    st.sidebar.title("🏥 TCSalud")

    st.sidebar.caption(
        "Gestión profesional para tu consultorio"
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


    # ======================================
    # INICIO
    # ======================================

    if opcion == "🏠 Inicio":

        st.title("Buen día 👋")

        st.write(
            "Bienvenido al panel profesional de TCSalud."
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "👥 Pacientes",
                len(st.session_state.pacientes)
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

        st.subheader("👥 Pacientes recientes")

        for paciente in st.session_state.pacientes:

            st.write(
                f"**{paciente['nombre']} "
                f"{paciente['apellido']}**"
            )


    # ======================================
    # PACIENTES
    # ======================================

    elif opcion == "👥 Pacientes":

        st.title("👥 Pacientes")

        st.write(
            "Administrá los pacientes de tu consultorio."
        )

        pestaña1, pestaña2 = st.tabs(
            [
                "📋 Lista de pacientes",
                "➕ Nuevo paciente"
            ]
        )


        # ----------------------------------
        # LISTA
        # ----------------------------------

        with pestaña1:

            buscar = st.text_input(
                "🔎 Buscar paciente",
                placeholder="Nombre, apellido o DNI"
            )

            pacientes = st.session_state.pacientes

            if buscar:

                pacientes = [
                    p for p in pacientes
                    if buscar.lower() in
                    (
                        p["nombre"] + " " +
                        p["apellido"] + " " +
                        p["dni"]
                    ).lower()
                ]

            if not pacientes:

                st.warning(
                    "No se encontraron pacientes."
                )

            for paciente in pacientes:

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
                            f"DNI: {paciente['dni']}"
                        )

                    with col2:

                        st.write(
                            f"Estado: "
                            f"**{paciente['estado']}**"
                        )

                        st.write(
                            f"Teléfono: "
                            f"{paciente['telefono']}"
                        )

                    with col3:

                        if st.button(
                            "Ver ficha",
                            key=f"ver_{paciente['id']}"
                        ):

                            st.session_state.paciente_seleccionado = paciente

                            st.rerun()


        # ----------------------------------
        # NUEVO PACIENTE
        # ----------------------------------

        with pestaña2:

            st.subheader(
                "Registrar nuevo paciente"
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
                value=date(1990, 1, 1)
            )

            telefono = st.text_input(
                "Teléfono"
            )

            email = st.text_input(
                "Email"
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

                    nuevo_id = len(
                        st.session_state.pacientes
                    ) + 1

                    nuevo_paciente = {

                        "id": nuevo_id,

                        "nombre": nombre,

                        "apellido": apellido,

                        "dni": dni,

                        "fecha_nacimiento":
                            fecha_nacimiento.strftime(
                                "%d/%m/%Y"
                            ),

                        "telefono": telefono,

                        "email": email,

                        "motivo": motivo,

                        "fecha_ingreso":
                            date.today().strftime(
                                "%d/%m/%Y"
                            ),

                        "estado": "Activo"
                    }

                    st.session_state.pacientes.append(
                        nuevo_paciente
                    )

                    st.success(
                        "Paciente registrado correctamente."
                    )


    # ======================================
    # FICHA DEL PACIENTE
    # ======================================

    if "paciente_seleccionado" in st.session_state:

        paciente = st.session_state.paciente_seleccionado

        st.divider()

        st.title(
            f"👤 {paciente['nombre']} "
            f"{paciente['apellido']}"
        )

        if st.button("← Volver a pacientes"):

            del st.session_state.paciente_seleccionado

            st.rerun()

        st.subheader("Datos del paciente")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**DNI:** {paciente['dni']}"
            )

            st.write(
                f"**Fecha de nacimiento:** "
                f"{paciente['fecha_nacimiento']}"
            )

            st.write(
                f"**Teléfono:** "
                f"{paciente['telefono']}"
            )

        with col2:

            st.write(
                f"**Email:** "
                f"{paciente['email']}"
            )

            st.write(
                f"**Motivo de consulta:** "
                f"{paciente['motivo']}"
            )

            st.write(
                f"**Estado:** "
                f"{paciente['estado']}"
            )

        st.divider()

        st.subheader("📝 Evoluciones")

        st.info(
            "En la próxima etapa vamos a agregar "
            "el registro de evoluciones de cada consulta."
        )


    # ======================================
    # EVOLUCIONES
    # ======================================

    elif opcion == "📝 Evoluciones":

        st.title("📝 Evoluciones")

        st.info(
            "Este módulo será desarrollado en la próxima etapa."
        )


    # ======================================
    # AGENDA
    # ======================================

    elif opcion == "📅 Agenda":

        st.title("📅 Agenda")

        st.info(
            "Próximamente podrás administrar "
            "turnos y calendario."
        )


    # ======================================
    # ESTADÍSTICAS
    # ======================================

    elif opcion == "📊 Estadísticas":

        st.title("📊 Estadísticas")

        st.info(
            "Las estadísticas se conectarán "
            "a los datos reales del sistema."
        )


    # ======================================
    # CONFIGURACIÓN
    # ======================================

    elif opcion == "⚙️ Configuración":

        st.title("⚙️ Configuración")

        st.subheader(
            "Perfil profesional"
        )

        st.text_input(
            "Nombre del profesional"
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


# ==========================================
# INICIO DEL SISTEMA
# ==========================================

if st.session_state.logueado:

    dashboard()

else:

    login()