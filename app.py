"""
Flight Delay Predictor — Streamlit App
Asian Avengers · CIS 412 · Spring 2026
"""
import streamlit as st
import pandas as pd
import pickle

# =============================================================================
# Page config
# =============================================================================
st.set_page_config(
    page_title="Predicting Flight Delays Before Takeoff",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# Hero image URLs (Unsplash, free for commercial use, direct CDN)
# =============================================================================
HERO_IMAGE = "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=2400&q=80"
ACCENT_IMAGE = "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1200&q=80"

# =============================================================================
# Theme — deep navy, cream accent, editorial type
# =============================================================================
st.markdown("""
<style>
    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base */
    .main, .stApp {
        background: #0E1116 !important;
        color: #E8E0D2;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1100px !important;
    }

    /* Typography */
    body, p, .stMarkdown {
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #E8E0D2 !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #E8E0D2 !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 4rem !important;
        font-weight: 700 !important;
        line-height: 1.05 !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 2.2rem !important;
        font-weight: 500 !important;
    }

    .eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #C9A77A;
        margin-bottom: 1rem;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #9A9486 !important;
        line-height: 1.6;
        max-width: 620px;
        margin-top: 1rem;
    }

    /* Hero image with gradient overlay */
    .hero-image-wrap {
        position: relative;
        margin: 2rem 0 3rem 0;
        border-radius: 24px;
        overflow: hidden;
        height: 380px;
    }
    .hero-image-wrap img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.55) saturate(0.9);
    }
    .hero-image-wrap::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(14,17,22,0.4) 0%, rgba(14,17,22,0.85) 100%);
    }
    .hero-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 2.5rem 3rem;
        z-index: 2;
        color: #E8E0D2;
    }
    .hero-overlay-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 600;
        line-height: 1.1;
        font-style: italic;
        color: #E8E0D2;
    }
    .hero-overlay-sub {
        font-size: 0.95rem;
        color: #C9A77A;
        margin-top: 0.5rem;
        letter-spacing: 0.05em;
    }

    /* Form labels */
    .stSelectbox > label, .stSlider > label, .stNumberInput > label {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        color: #9A9486 !important;
        margin-bottom: 0.4rem !important;
    }

    /* Selectbox closed state */
    div[data-baseweb="select"] > div:first-child {
        background: #161B22 !important;
        border: 1px solid rgba(232, 224, 210, 0.08) !important;
        border-radius: 10px !important;
        min-height: 44px !important;
    }
    div[data-baseweb="select"] > div:first-child:hover {
        border-color: rgba(201, 167, 122, 0.4) !important;
    }
    div[data-baseweb="select"] [role="combobox"],
    div[data-baseweb="select"] [aria-selected="true"] {
        color: #E8E0D2 !important;
        background: transparent !important;
    }

    /* Selectbox popover */
    div[data-baseweb="popover"] {
        background: #161B22 !important;
    }
    ul[role="listbox"] {
        background: #161B22 !important;
        border: 1px solid rgba(201, 167, 122, 0.25) !important;
        border-radius: 10px !important;
        padding: 0.25rem !important;
    }
    li[role="option"] {
        background: transparent !important;
        color: #E8E0D2 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 0.85rem !important;
        border-radius: 6px !important;
    }
    li[role="option"]:hover {
        background: rgba(201, 167, 122, 0.15) !important;
        color: #E8E0D2 !important;
    }
    li[role="option"][aria-selected="true"] {
        background: rgba(201, 167, 122, 0.2) !important;
        color: #C9A77A !important;
    }

    /* Number input */
    .stNumberInput input {
        background: #161B22 !important;
        border: 1px solid rgba(232, 224, 210, 0.08) !important;
        border-radius: 10px !important;
        color: #E8E0D2 !important;
    }

    /* Slider */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #C9A77A !important;
        box-shadow: 0 0 0 4px rgba(201, 167, 122, 0.15) !important;
    }
    .stSlider [data-baseweb="slider"] > div > div > div {
        background: #C9A77A !important;
    }
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #6E6A5E !important;
        font-size: 0.7rem !important;
    }

    /* Checkbox */
    .stCheckbox label {
        color: #E8E0D2 !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
    }
    .stCheckbox label > div:first-child {
        background: #161B22 !important;
        border-color: rgba(232, 224, 210, 0.2) !important;
    }

    /* Predict button — DARK with gold border */
    .stButton > button {
        background: #1E1B16 !important;
        color: #E8E0D2 !important;
        border: 2px solid #C9A77A !important;
        padding: 1.1rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.25em !important;
        text-transform: uppercase !important;
        border-radius: 14px !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 20px rgba(201, 167, 122, 0.15);
    }
    .stButton > button:hover {
        background: #C9A77A !important;
        border-color: #C9A77A !important;
        color: #0E1116 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(201, 167, 122, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* Divider */
    hr {
        border: none !important;
        border-top: 1px solid rgba(232, 224, 210, 0.08) !important;
        margin: 3rem 0 !important;
    }

    /* Boarding-pass-style result card */
    .ticket {
        background: linear-gradient(145deg, #1A1F2A 0%, #161B22 100%);
        border: 1px solid rgba(232, 224, 210, 0.08);
        border-radius: 24px;
        padding: 3rem;
        position: relative;
        overflow: hidden;
        margin-top: 1rem;
    }
    .ticket::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #C9A77A, #E8E0D2, #C9A77A);
    }

    .route-display {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 1.5rem 0;
    }
    .route-code {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        color: #E8E0D2;
        letter-spacing: 0.05em;
    }
    .route-line {
        flex: 1;
        margin: 0 1.5rem;
        position: relative;
        height: 1px;
        background: rgba(232, 224, 210, 0.2);
    }
    .route-line::before {
        content: '✈';
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        background: #1A1F2A;
        padding: 0 0.8rem;
        color: #C9A77A;
        font-size: 1.2rem;
    }

    .prob-display {
        font-family: 'Playfair Display', serif;
        font-size: 6rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.04em;
    }

    .status-pill {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-top: 1rem;
    }
    .status-ontime { background: rgba(124, 196, 142, 0.12); color: #7CC48E; border: 1px solid rgba(124, 196, 142, 0.3); }
    .status-delayed { background: rgba(232, 110, 110, 0.12); color: #E86E6E; border: 1px solid rgba(232, 110, 110, 0.3); }
    .status-warn { background: rgba(201, 167, 122, 0.12); color: #C9A77A; border: 1px solid rgba(201, 167, 122, 0.3); }

    /* Detail rows */
    .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px dashed rgba(232, 224, 210, 0.08);
    }
    .detail-row:last-child { border-bottom: none; }
    .detail-label {
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #6E6A5E;
    }
    .detail-value {
        font-size: 0.95rem;
        color: #E8E0D2;
        font-weight: 500;
    }

    /* Stat tiles */
    .stat-tile {
        background: #161B22;
        border: 1px solid rgba(232, 224, 210, 0.06);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        text-align: left;
    }
    .stat-value {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 600;
        color: #C9A77A;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #6E6A5E;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Load model and metadata
# =============================================================================
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_data_info():
    with open('data_info.pkl', 'rb') as f:
        return pickle.load(f)

models = load_model()
info = load_data_info()

# =============================================================================
# HERO
# =============================================================================
st.markdown("<div class='eyebrow'>ASIAN AVENGERS · CIS 412 · SPRING 2026</div>", unsafe_allow_html=True)
st.markdown("<h1>Predicting Flight Delays<br/><em style='font-style:italic;color:#C9A77A;'>Before Takeoff</em></h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>"
    "A machine learning model trained on 2,201 commercial flights between "
    "Washington, D.C. and New York in January 2004. Enter pre-departure details "
    "to estimate delay probability."
    "</p>",
    unsafe_allow_html=True
)

# Hero image with overlay
st.markdown(f"""
<div class='hero-image-wrap'>
    <img src='{HERO_IMAGE}' alt='Aerial flight view'/>
    <div class='hero-overlay'>
        <div class='hero-overlay-title'>"Predict the unpredictable."</div>
        <div class='hero-overlay-sub'>MACHINE LEARNING · AVIATION · OPERATIONS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# MODEL TOGGLE + STATS
# =============================================================================
top_col1, top_col2 = st.columns([3, 1])
with top_col2:
    model_choice = st.selectbox(
        "MODEL",
        options=['random_forest', 'logistic_regression'],
        format_func=lambda x: 'Random Forest' if x == 'random_forest' else 'Logistic Regression',
    )

metrics = info['model_metrics'][model_choice]
m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.markdown(f"<div class='stat-tile'><div class='stat-value'>{metrics['test_accuracy']*100:.1f}%</div><div class='stat-label'>Test Accuracy</div></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='stat-tile'><div class='stat-value'>{metrics['test_f1']*100:.1f}%</div><div class='stat-label'>F1 Score</div></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='stat-tile'><div class='stat-value'>{metrics['test_recall']*100:.1f}%</div><div class='stat-label'>Recall</div></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='stat-tile'><div class='stat-value'>{metrics['test_precision']*100:.1f}%</div><div class='stat-label'>Precision</div></div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =============================================================================
# FORM
# =============================================================================
st.markdown("<div class='eyebrow'>FLIGHT PARAMETERS</div>", unsafe_allow_html=True)
st.markdown("<h2>Flight Details</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    carrier_dict = info['categorical_unique_values']['CARRIER']
    carrier_label = st.selectbox("Carrier", options=list(carrier_dict.keys()), format_func=lambda code: carrier_dict[code], index=2)

    origin_dict = info['categorical_unique_values']['ORIGIN']
    origin_label = st.selectbox("Origin Airport", options=list(origin_dict.keys()), format_func=lambda code: origin_dict[code], index=1)

    dest_dict = info['categorical_unique_values']['DEST']
    dest_label = st.selectbox("Destination Airport", options=list(dest_dict.keys()), format_func=lambda code: dest_dict[code], index=1)

    distance_min, distance_max, distance_default = info['numeric_ranges']['DISTANCE']
    distance = st.slider("Flight Distance (Miles)", distance_min, distance_max, distance_default)

with col2:
    day_dict = info['categorical_unique_values']['DAY_WEEK']
    day_week = st.selectbox("Day of Week", options=list(day_dict.keys()), format_func=lambda d: day_dict[d], index=2)

    dom_min, dom_max, dom_default = info['numeric_ranges']['DAY_OF_MONTH']
    day_of_month = st.slider("Day of Month", dom_min, dom_max, dom_default)

    h_min, h_max, h_default = info['numeric_ranges']['CRS_DEP_HOUR']
    dep_hour = st.slider("Scheduled Departure Hour", h_min, h_max, h_default)

    m_min, m_max, m_default = info['numeric_ranges']['CRS_DEP_MINUTE']
    dep_minute = st.slider("Scheduled Departure Minute", m_min, m_max, m_default)

st.markdown("<br>", unsafe_allow_html=True)
weather_checked = st.checkbox("Adverse weather conditions forecasted")
weather = 1 if weather_checked else 0

st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# Prediction logic
# =============================================================================
def build_input_row(carrier, origin, dest, distance, weather, day_week,
                    day_of_month, dep_hour, dep_minute, expected_columns):
    row = {col: 0 for col in expected_columns}
    row['DISTANCE'] = distance
    row['Weather'] = weather
    row['DAY_WEEK'] = day_week
    row['DAY_OF_MONTH'] = day_of_month
    row['MONTH'] = 1
    row['CRS_DEP_HOUR'] = dep_hour
    row['CRS_DEP_MINUTE'] = dep_minute
    for col_prefix, value in [('CARRIER_', carrier), ('ORIGIN_', origin), ('DEST_', dest)]:
        col = f'{col_prefix}{value}'
        if col in row:
            row[col] = 1
    return pd.DataFrame([row])[expected_columns]


# =============================================================================
# Predict button + result card (split into chunks to avoid Streamlit HTML escape)
# =============================================================================
if st.button("RUN PREDICTION", use_container_width=True):
    input_df = build_input_row(
        carrier=carrier_label, origin=origin_label, dest=dest_label,
        distance=distance, weather=weather, day_week=day_week,
        day_of_month=day_of_month, dep_hour=dep_hour, dep_minute=dep_minute,
        expected_columns=info['expected_columns'],
    )

    selected_model = models[model_choice]
    probabilities = selected_model.predict_proba(input_df)[0]
    delay_prob = probabilities[1]
    ontime_prob = probabilities[0]

    if delay_prob >= 0.7:
        status_text, status_class, status_color = "HIGH DELAY RISK", "status-delayed", "#E86E6E"
    elif delay_prob >= 0.5:
        status_text, status_class, status_color = "MODERATE RISK", "status-warn", "#C9A77A"
    elif delay_prob >= 0.3:
        status_text, status_class, status_color = "LOW RISK", "status-warn", "#C9A77A"
    else:
        status_text, status_class, status_color = "ON-TIME EXPECTED", "status-ontime", "#7CC48E"

    formatted_time = f"{dep_hour:02d}:{dep_minute:02d}"
    carrier_name = carrier_dict[carrier_label]
    day_name = day_dict[day_week]
    weather_text = "Adverse" if weather else "Clear"
    model_name = "Random Forest" if model_choice == "random_forest" else "Logistic Regression"

    # CRITICAL: render the entire ticket as a SINGLE compact f-string with NO blank lines
    # (Streamlit treats blank lines inside markdown as code blocks, which caused the raw HTML bug)
    ticket_html = (
        "<div class='ticket'>"
        "<div class='eyebrow'>PREDICTION RESULT</div>"
        "<div class='route-display'>"
        f"<div class='route-code'>{origin_label}</div>"
        "<div class='route-line'></div>"
        f"<div class='route-code'>{dest_label}</div>"
        "</div>"
        "<div style='display:flex; justify-content:space-between; align-items:flex-end; margin: 2rem 0;'>"
        "<div>"
        f"<div class='prob-display' style='color:{status_color};'>{delay_prob*100:.1f}%</div>"
        "<div class='stat-label'>DELAY PROBABILITY</div>"
        f"<div class='status-pill {status_class}'>{status_text}</div>"
        "</div>"
        "<div style='text-align:right;'>"
        f"<div style='font-family:Playfair Display,serif; font-size:2rem; font-weight:600; color:#E8E0D2;'>{formatted_time}</div>"
        "<div class='stat-label'>SCHEDULED DEPARTURE</div>"
        "</div>"
        "</div>"
        "<div style='margin-top: 2rem;'>"
        f"<div class='detail-row'><div class='detail-label'>Carrier</div><div class='detail-value'>{carrier_name}</div></div>"
        f"<div class='detail-row'><div class='detail-label'>Day</div><div class='detail-value'>{day_name}, Day {day_of_month}</div></div>"
        f"<div class='detail-row'><div class='detail-label'>Distance</div><div class='detail-value'>{distance} miles</div></div>"
        f"<div class='detail-row'><div class='detail-label'>Weather</div><div class='detail-value'>{weather_text}</div></div>"
        f"<div class='detail-row'><div class='detail-label'>On-Time Probability</div><div class='detail-value'>{ontime_prob*100:.1f}%</div></div>"
        f"<div class='detail-row'><div class='detail-label'>Model</div><div class='detail-value'>{model_name}</div></div>"
        "</div>"
        "</div>"
    )
    st.markdown(ticket_html, unsafe_allow_html=True)
