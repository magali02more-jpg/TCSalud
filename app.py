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
# SUPABASE
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
        font-size: 42px;
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
# ESTADO
# =========================================================

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "modo_recuperacion" not in st.session_state:
    st.session_state.modo_recuperacion = False

if "paciente_seleccionado" not in st.session_state:
    st.session_state.paciente_seleccionado = None

# =========================================================
# RECUPERACIÓN DE CONTRASEÑA
# =========================================================

params = st.query_params

if (
    "code" in params
    or "access_token" in params
    or "type" in params
):

    tipo = params.get("type")

    if tipo == "recovery" or "code" in params:
        st.session_state.modo_recuperacion = True

# =========================================================
# OBTENER PROFESIONAL
# =========================================================

def obtener_profesional():

    try:

        if not st.session_state.usuario:
            return None

        uid = st.session_state.usuario["id"]

        respuesta = (
            supabase
            .table("profesionales")
            .select("*")
            .eq(
                "auth_user_id",
                uid
            )
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
        'Gestión profesional de salud'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.subheader(
            "🔐 Iniciar sesión"
        )

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Contraseña",
            type="password",
            key="login_password"
        )

        if st.button(
            "Ingresar",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Completá email y contraseña."
                )

            else:

                try:

                    respuesta = (
                        supabase
                        .auth
                        .sign_in_with_password(
                            {
                                "email": email,
                                "password": password
                            }
                        )
                    )

                    if respuesta.user:

                        # Guardamos los datos del usuario
                        st.session_state.usuario = {
                            "id": respuesta.user.id,
                            "email": respuesta.user.email
                        }

                        # Guardamos los tokens para mantener
                        # la sesión después de st.rerun()
                        if respuesta.session:

                            st.session_state.access_token = (
                                respuesta.session.access_token
                            )

                            st.session_state.refresh_token = (
                                respuesta.session.refresh_token
                            )

                            # Establecemos la sesión
                            supabase.auth.set_session(
                                respuesta.session.access_token,
                                respuesta.session.refresh_token
                            )

                        st.success(
                            "Ingreso correcto."
                        )

                        st.rerun()

                except Exception as error:

                    st.error(
                        "Email o contraseña incorrectos."
                    )

# =========================================================
# CAMBIAR CONTRASEÑA
# =========================================================

def pantalla_nueva_contrasena():

    st.markdown(
        '<div class="logo">🏥 TCSalud</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Restablecer contraseña'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.subheader(
            "🔐 Crear nueva contraseña"
        )

        nueva = st.text_input(
            "Nueva contraseña",
            type="password"
        )

        repetir = st.text_input(
            "Repetir contraseña",
            type="password"
        )

        if st.button(
            "Guardar nueva contraseña",
            use_container_width=True
        ):

            if not nueva or not repetir:

                st.warning(
                    "Completá ambos campos."
                )

            elif nueva != repetir:

                st.error(
                    "Las contraseñas no coinciden."
                )

            elif len(nueva) < 6:

                st.error(
                    "La contraseña debe tener "
                    "al menos 6 caracteres."
                )

            else:

                try:

                    supabase.auth.update_user(
                        {
                            "password": nueva
                        }
                    )

                    st.success(
                        "✅ Contraseña actualizada correctamente."
                    )

                    st.session_state.modo_recuperacion = False

                    st.query_params.clear()

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"No se pudo cambiar la contraseña: {error}"
                    )

# =========================================================
# PACIENTES
# =========================================================

def obtener_pacientes(profesional_id):

    try:

        respuesta = (
            supabase
            .table("pacientes")
            .select("*")
            .eq(
                "profesional_id",
                profesional_id
            )
            .order("apellido")
            .execute()
        )

        return respuesta.data or []

    except Exception as error:

        st.error(
            f"No se pudieron cargar los pacientes: {error}"
        )

        return []

# =========================================================
# CREAR PACIENTE
# =========================================================

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
            "fecha_nacimiento": str(
                fecha_nacimiento
            ),
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
# PANTALLA PACIENTES
# =========================================================

def pantalla_pacientes(profesional):

    st.title("👥 Pacientes")

    pacientes = obtener_pacientes(
        profesional["id"]
    )

    pestaña_lista, pestaña_nuevo = st.tabs(
        [
            "📋 Pacientes",
            "➕ Nuevo paciente"
        ]
    )

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
                    (
                        paciente.get("nombre")
                        or ""
                    )
                    + " "
                    + (
                        paciente.get("apellido")
                        or ""
                    )
                    + " "
                    + str(
                        paciente.get("dni")
                        or ""
                    )
                ).lower()
            ]

        if not pacientes_filtrados:

            st.info(
                "No hay pacientes registrados."
            )

        else:

            for paciente in pacientes_filtrados:

                with st.container(
                    border=True
                ):

                    col1, col2, col3 = st.columns(
                        [3, 2, 1]
                    )

                    with col1:

                        st.subheader(
                            f"{paciente.get('nombre', '')} "
                            f"{paciente.get('apellido', '')}"
                        )

                        st.write(
                            "DNI: "
                            + str(
                                paciente.get(
                                    "dni"
                                )
                                or "-"
                            )
                        )

                    with col2:

                        st.write(
                            "🏥 Obra social: "
                            + str(
                                paciente.get(
                                    "obra_social"
                                )
                                or "-"
                            )
                        )

                        st.write(
                            "📞 "
                            + str(
                                paciente.get(
                                    "telefono"
                                )
                                or "-"
                            )
                        )

                    with col3:

                        if st.button(
                            "Ver ficha",
                            key=(
                                "ver_"
                                + str(
                                    paciente["id"]
                                )
                            )
                        ):

                            st.session_state.paciente_seleccionado = paciente

                            st.rerun()

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
            value=date(
                1990,
                1,
                1
            ),
            min_value=date(
                1900,
                1,
                1
            ),
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
# FICHA
# =========================================================

def pantalla_ficha(paciente):

    st.title(
        "👤 "
        + str(
            paciente.get("nombre")
            or ""
        )
        + " "
        + str(
            paciente.get("apellido")
            or ""
        )
    )

    if st.button(
        "← Volver a pacientes"
    ):

        st.session_state.paciente_seleccionado = None

        st.rerun()

    st.divider()

    st.subheader(
        "📋 Datos personales"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Nombre:** "
            + str(
                paciente.get("nombre")
                or "-"
            )
        )

        st.write(
            "**Apellido:** "
            + str(
                paciente.get("apellido")
                or "-"
            )
        )

        st.write(
            "**DNI:** "
            + str(
                paciente.get("dni")
                or "-"
            )
        )

        fecha = paciente.get(
            "fecha_nacimiento"
        )

        if fecha:

            try:

                fecha_formateada = (
                    date.fromisoformat(
                        str(fecha)
                    )
                    .strftime(
                        "%d/%m/%Y"
                    )
                )

            except Exception:

                fecha_formateada = str(
                    fecha
                )

        else:

            fecha_formateada = "-"

        st.write(
            "**Fecha de nacimiento:** "
            + fecha_formateada
        )

        st.write(
            "**Teléfono:** "
            + str(
                paciente.get(
                    "telefono"
                )
                or "-"
            )
        )

    with col2:

        st.write(
            "**Email:** "
            + str(
                paciente.get(
                    "email"
                )
                or "-"
            )
        )

        st.write(
            "**Obra social:** "
            + str(
                paciente.get(
                    "obra_social"
                )
                or "-"
            )
        )

        st.write(
            "**Motivo de consulta:** "
            + str(
                paciente.get(
                    "motivo_consulta"
                )
                or "-"
            )
        )

        st.write(
            "**Estado:** "
            + str(
                paciente.get(
                    "estado"
                )
                or "activo"
            )
        )

    st.divider()

    st.subheader(
        "📝 Evoluciones"
    )

    st.info(
        "Todavía no hay evoluciones registradas."
    )

    if st.button(
        "➕ Nueva evolución",
        use_container_width=True
    ):

        st.info(
            "El módulo de evoluciones "
            "lo vamos a desarrollar a continuación."
        )

# =========================================================
# DASHBOARD
# =========================================================

def dashboard(profesional):

    st.sidebar.title(
        "🏥 TCSalud"
    )

    st.sidebar.write(
        "👤 "
        + str(
            profesional.get(
                "nombre"
            )
            or ""
        )
        + " "
        + str(
            profesional.get(
                "apellido"
            )
            or ""
        )
    )

    st.sidebar.caption(
        profesional.get(
            "profesion"
        )
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

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.clear()

        st.rerun()

    if opcion == "🏠 Inicio":

        pacientes = obtener_pacientes(
            profesional["id"]
        )

        st.title(
            "Buen día 👋"
        )

        st.write(
            "Bienvenido al panel profesional de TCSalud."
        )

        st.divider()

        col1, col2, col3, col4 = st.columns(
            4
        )

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
                    "**"
                    + str(
                        paciente.get(
                            "nombre"
                        )
                        or ""
                    )
                    + " "
                    + str(
                        paciente.get(
                            "apellido"
                        )
                        or ""
                    )
                    + "**"
                )

        else:

            st.info(
                "Todavía no tenés pacientes registrados."
            )

    elif opcion == "👥 Pacientes":

        paciente = (
            st.session_state
            .paciente_seleccionado
        )

        if paciente:

            pantalla_ficha(
                paciente
            )

        else:

            pantalla_pacientes(
                profesional
            )

    elif opcion == "📝 Evoluciones":

        st.title(
            "📝 Evoluciones"
        )

        st.info(
            "El módulo de evoluciones "
            "se encuentra en desarrollo."
        )

    elif opcion == "📅 Agenda":

        st.title(
            "📅 Agenda"
        )

        st.info(
            "El módulo de agenda "
            "se encuentra en desarrollo."
        )

    elif opcion == "📊 Estadísticas":

        st.title(
            "📊 Estadísticas"
        )

        pacientes = obtener_pacientes(
            profesional["id"]
        )

        st.metric(
            "Total de pacientes",
            len(pacientes)
        )

    elif opcion == "⚙️ Configuración":

        st.title(
            "⚙️ Configuración"
        )

        st.subheader(
            "👤 Datos profesionales"
        )

        st.write(
            "**Nombre:** "
            + str(
                profesional.get(
                    "nombre"
                )
                or "-"
            )
            + " "
            + str(
                profesional.get(
                    "apellido"
                )
                or "-"
            )
        )

        st.write(
            "**Email:** "
            + str(
                profesional.get(
                    "email"
                )
                or "-"
            )
        )

        st.write(
            "**Profesión:** "
            + str(
                profesional.get(
                    "profesion"
                )
                or "-"
            )
        )

        st.write(
            "**Matrícula:** "
            + str(
                profesional.get(
                    "matricula"
                )
                or "-"
            )
        )

# =========================================================
# INICIO DE LA APLICACIÓN
# =========================================================

if st.session_state.modo_recuperacion:

    pantalla_nueva_contrasena()

elif st.session_state.usuario is None:

    pantalla_login()

else:

    profesional = obtener_profesional()

    if profesional is None:

        st.error(
            "No encontramos un perfil profesional "
            "asociado a esta cuenta."
        )

        if st.button(
            "Cerrar sesión"
        ):

            try:
                supabase.auth.sign_out()
            except Exception:
                pass

            st.session_state.clear()

            st.rerun()

    else:

        dashboard(
            profesional
        ) 