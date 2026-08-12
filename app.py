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

        # PRUEBA TEMPORAL
        st.write(
            "🔎 UID recibido por TCSalud:",
            uid
        )

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

        # PRUEBA TEMPORAL
        st.write(
            "🔎 Resultado de Supabase:",
            respuesta.data
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

        st.sub