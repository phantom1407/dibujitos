import streamlit as st
from streamlit_drawable_canvas import st_canvas

# ---------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Tablero para dibujo",
    page_icon="🌸",
    layout="centered",
)

# ---------------------------------------------------------------
# Estilos (todo el tema rosado va aquí, sin config.toml)
# ---------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito:wght@400;600;700&display=swap');

    :root {
        --rubor: #FDE8EF;      /* fondo general */
        --petalo: #F7C6D9;     /* barra lateral */
        --rosa: #D6336C;       /* acentos */
        --ciruela: #4A1D32;    /* texto */
        --cinta: rgba(244, 143, 177, 0.55); /* cinta adhesiva del marco */
    }

    /* Fondo y texto general (se fuerza aunque el navegador esté en modo oscuro) */
    .stApp {
        background-color: var(--rubor) !important;
        font-family: 'Nunito', sans-serif;
    }
    .stApp, .stApp p, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3 {
        color: var(--ciruela);
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    [data-testid="stHeader"] svg,
    [data-testid="stSidebar"] button svg {
        fill: var(--ciruela) !important;
        color: var(--ciruela) !important;
    }

    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: var(--petalo) !important;
        border-right: 3px dashed #EFA3C0;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: 'Fredoka', sans-serif;
        color: var(--ciruela) !important;
    }
    [data-testid="stSidebar"] label p {
        font-weight: 700;
        color: var(--ciruela) !important;
    }
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #8C4A68 !important;
    }

    /* Sliders: el rojo por defecto de Streamlit se vuelve rosado */
    [data-testid="stSlider"] [data-baseweb="slider"] {
        filter: hue-rotate(-22deg) saturate(0.9);
    }
    [data-testid="stSliderTickBarMin"],
    [data-testid="stSliderTickBarMax"] {
        color: #8C4A68 !important;
    }

    /* Lista desplegable */
    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #EFA3C0 !important;
        border-radius: 12px !important;
    }
    [data-baseweb="select"] * {
        color: var(--ciruela) !important;
    }
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] li {
        background-color: #FFFFFF !important;
        color: var(--ciruela) !important;
    }
    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] li[aria-selected="true"] {
        background-color: var(--rubor) !important;
    }

    /* Selectores de color */
    [data-testid="stColorPicker"] [data-testid="stColorPickerBlock"],
    [data-testid="stColorPicker"] > div > div {
        border-radius: 12px;
        box-shadow: 0 0 0 3px #FFFFFF;
    }

    /* Título */
    .titulo {
        font-family: 'Fredoka', sans-serif;
        font-size: clamp(2.2rem, 6vw, 3.4rem);
        font-weight: 600;
        color: var(--ciruela) !important;
        text-align: center;
        margin: 0.2rem 0 0;
        line-height: 1.1;
    }
    .subtitulo {
        text-align: center;
        color: #8C4A68 !important;
        margin: 0.4rem 0 1.6rem;
        font-size: 1.05rem;
    }

    /* Marco del lienzo: hoja de cuaderno con cinta adhesiva */
    .st-key-marco {
        position: relative;
        background: #FFFFFF;
        border-radius: 6px;
        padding: 1.4rem 1rem 0.6rem;
        box-shadow: 0 10px 0 -4px #F3B4CB, 0 14px 28px rgba(74, 29, 50, 0.12);
        align-items: center;
    }
    .st-key-marco::before,
    .st-key-marco::after {
        content: "";
        position: absolute;
        top: -14px;
        width: 110px;
        height: 28px;
        background: var(--cinta);
        z-index: 2;
    }
    .st-key-marco::before {
        left: 18px;
        transform: rotate(-6deg);
    }
    .st-key-marco::after {
        right: 18px;
        transform: rotate(5deg);
    }

    /* Pie de página */
    .pie {
        text-align: center;
        color: #A0607E !important;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------
# Funciones de apoyo
# ---------------------------------------------------------------
def hex_a_rgba(hex_color: str, alpha: float) -> str:
    """Convierte un color #RRGGBB a texto rgba() con transparencia."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


# ---------------------------------------------------------------
# Herramientas disponibles (nombre bonito -> valor del componente)
# ---------------------------------------------------------------
HERRAMIENTAS = {
    "✏️ Lápiz libre": "freedraw",
    "📏 Línea": "line",
    "⬜ Rectángulo": "rect",
    "⚪ Círculo": "circle",
    "🔺 Polígono": "polygon",
    "🔘 Punto": "point",
    "🖐️ Mover y ajustar": "transform",
}

# ---------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------
with st.sidebar:
    st.header("🌸 Propiedades del tablero")

    st.subheader("Dimensiones")
    canvas_width = st.slider("Ancho del tablero", 300, 700, 500, 50)
    canvas_height = st.slider("Alto del tablero", 200, 600, 400, 50)

    st.subheader("Herramienta")
    herramienta = st.selectbox("Herramienta de dibujo", list(HERRAMIENTAS.keys()))
    drawing_mode = HERRAMIENTAS[herramienta]

    stroke_width = st.slider("Ancho de línea", 1, 30, 8)

    point_radius = 3
    if drawing_mode == "point":
        point_radius = st.slider("Tamaño del punto", 1, 25, 6)

    st.subheader("Colores")
    stroke_color = st.color_picker("Color de trazo", "#D6336C")
    bg_color = st.color_picker("Color de fondo", "#FFFFFF")
    fill_hex = st.color_picker("Relleno de figuras", "#F48FB1")
    fill_alpha = st.slider("Transparencia del relleno", 0.0, 1.0, 0.35, 0.05)

    if drawing_mode == "polygon":
        st.caption("Haz clic para poner cada vértice y clic derecho para cerrar el polígono.")
    elif drawing_mode == "transform":
        st.caption("Selecciona una figura para moverla, girarla o cambiarle el tamaño.")

# ---------------------------------------------------------------
# Contenido principal
# ---------------------------------------------------------------
st.markdown('<p class="titulo">Tablero para dibujo</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Elige una herramienta en el panel de la izquierda y empieza a dibujar.</p>',
    unsafe_allow_html=True,
)

with st.container(key="marco"):
    canvas_result = st_canvas(
        fill_color=hex_a_rgba(fill_hex, fill_alpha),
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        point_display_radius=point_radius,
        key=f"canvas_{canvas_width}_{canvas_height}",  # se reinicia al cambiar el tamaño
    )

# Contador de trazos
cantidad = 0
if canvas_result.json_data is not None:
    cantidad = len(canvas_result.json_data.get("objects", []))

if cantidad == 0:
    st.caption("El tablero está vacío. Haz tu primer trazo.")
else:
    texto = "trazo" if cantidad == 1 else "trazos"
    st.caption(f"Llevas {cantidad} {texto} en el tablero. Usa el ícono de descarga debajo del lienzo para guardarlo.")

st.markdown('<p class="pie">Hecho con 💗 y Streamlit</p>', unsafe_allow_html=True)
