"""
Flight Delay Predictor — Streamlit App
Asian Avengers · CIS 412 · Spring 2026
"""
import streamlit as st
import pandas as pd
import pickle
import json
from datetime import date, time
import streamlit.components.v1 as components

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
# Image URLs
# =============================================================================
HERO_IMAGE = "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=2400&q=80"
TICKET_IMAGE = "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1600&q=80"

# =============================================================================
# Theme
# =============================================================================
st.markdown("""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

    .main, .stApp { background: #0E1116 !important; color: #E8E0D2; }
    .block-container { padding-top: 2rem !important; padding-bottom: 4rem !important; max-width: 1100px !important; }

    body, p, .stMarkdown {
        font-family: 'Inter', -apple-system, sans-serif !important;
        color: #E8E0D2 !important;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #E8E0D2 !important;
        letter-spacing: -0.02em;
    }
    h1 { font-size: 4rem !important; font-weight: 700 !important; line-height: 1.05 !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 2.2rem !important; font-weight: 500 !important; }

    .eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem; font-weight: 600;
        letter-spacing: 0.25em; text-transform: uppercase;
        color: #C9A77A; margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.05rem; color: #9A9486 !important;
        line-height: 1.6; max-width: 620px; margin-top: 1rem;
    }

    .hero-image-wrap {
        position: relative; margin: 2rem 0 3rem 0;
        border-radius: 24px; overflow: hidden; height: 380px;
    }
    .hero-image-wrap img {
        width: 100%; height: 100%; object-fit: cover;
        filter: brightness(0.55) saturate(0.9);
    }
    .hero-image-wrap::after {
        content: ''; position: absolute; inset: 0;
        background: linear-gradient(135deg, rgba(14,17,22,0.4) 0%, rgba(14,17,22,0.85) 100%);
    }
    .hero-overlay {
        position: absolute; bottom: 0; left: 0; right: 0;
        padding: 2.5rem 3rem; z-index: 2; color: #E8E0D2;
    }
    .hero-overlay-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem; font-weight: 600; line-height: 1.1;
        font-style: italic; color: #E8E0D2;
    }
    .hero-overlay-sub {
        font-size: 0.95rem; color: #C9A77A; margin-top: 0.5rem;
        letter-spacing: 0.05em;
    }

    .stSelectbox > label, .stSlider > label, .stNumberInput > label,
    .stDateInput > label, .stTimeInput > label {
        font-size: 0.7rem !important; font-weight: 600 !important;
        letter-spacing: 0.18em !important; text-transform: uppercase !important;
        color: #9A9486 !important; margin-bottom: 0.4rem !important;
    }

    div[data-baseweb="select"] > div:first-child {
        background: #161B22 !important;
        border: 1px solid rgba(232, 224, 210, 0.08) !important;
        border-radius: 10px !important; min-height: 44px !important;
    }
    div[data-baseweb="select"] > div:first-child:hover {
        border-color: rgba(201, 167, 122, 0.4) !important;
    }
    div[data-baseweb="select"] [role="combobox"],
    div[data-baseweb="select"] [aria-selected="true"] {
        color: #E8E0D2 !important; background: transparent !important;
    }
    div[data-baseweb="popover"] { background: #161B22 !important; }
    ul[role="listbox"] {
        background: #161B22 !important;
        border: 1px solid rgba(201, 167, 122, 0.25) !important;
        border-radius: 10px !important; padding: 0.25rem !important;
    }
    li[role="option"] {
        background: transparent !important; color: #E8E0D2 !important;
        font-family: 'Inter', sans-serif !important; font-size: 0.95rem !important;
        padding: 0.6rem 0.85rem !important; border-radius: 6px !important;
    }
    li[role="option"]:hover {
        background: rgba(201, 167, 122, 0.15) !important; color: #E8E0D2 !important;
    }
    li[role="option"][aria-selected="true"] {
        background: rgba(201, 167, 122, 0.2) !important; color: #C9A77A !important;
    }

    /* Date input + Time input — same dark/cream style */
    .stDateInput > div > div,
    .stTimeInput > div > div {
        background: #161B22 !important;
        border: 1px solid rgba(232, 224, 210, 0.08) !important;
        border-radius: 10px !important;
    }
    .stDateInput > div > div:hover,
    .stTimeInput > div > div:hover {
        border-color: rgba(201, 167, 122, 0.4) !important;
    }
    .stDateInput input,
    .stTimeInput input {
        background: transparent !important;
        color: #E8E0D2 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #C9A77A !important;
        box-shadow: 0 0 0 4px rgba(201, 167, 122, 0.15) !important;
    }
    .stSlider [data-baseweb="slider"] > div > div > div { background: #C9A77A !important; }
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] {
        color: #6E6A5E !important; font-size: 0.7rem !important;
    }

    .stCheckbox label {
        color: #E8E0D2 !important; font-size: 0.9rem !important; font-weight: 400 !important;
    }
    .stCheckbox label > div:first-child {
        background: #161B22 !important; border-color: rgba(232, 224, 210, 0.2) !important;
    }

    .stButton > button {
        background: #1E1B16 !important; color: #E8E0D2 !important;
        border: 2px solid #C9A77A !important;
        padding: 1.1rem 2rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important; font-weight: 700 !important;
        letter-spacing: 0.25em !important; text-transform: uppercase !important;
        border-radius: 14px !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 20px rgba(201, 167, 122, 0.15);
    }
    .stButton > button:hover {
        background: #C9A77A !important; border-color: #C9A77A !important;
        color: #0E1116 !important; transform: translateY(-2px);
        box-shadow: 0 8px 28px rgba(201, 167, 122, 0.4) !important;
    }

    .clear-btn-wrap .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(232, 224, 210, 0.15) !important;
        color: #9A9486 !important;
        padding: 0.5rem 1.2rem !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.2em !important;
        box-shadow: none !important;
    }
    .clear-btn-wrap .stButton > button:hover {
        background: rgba(232, 110, 110, 0.1) !important;
        border-color: rgba(232, 110, 110, 0.4) !important;
        color: #E86E6E !important;
        transform: none !important;
        box-shadow: none !important;
    }

    hr {
        border: none !important;
        border-top: 1px solid rgba(232, 224, 210, 0.08) !important;
        margin: 3rem 0 !important;
    }

    .stat-tile {
        background: #161B22; border: 1px solid rgba(232, 224, 210, 0.06);
        border-radius: 14px; padding: 1.25rem 1.5rem; text-align: left;
    }
    .stat-value {
        font-family: 'Playfair Display', serif;
        font-size: 2rem; font-weight: 600; color: #C9A77A; line-height: 1;
    }
    .stat-label {
        font-size: 0.65rem; letter-spacing: 0.2em;
        text-transform: uppercase; color: #6E6A5E; margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Initialize session state for prediction history
# =============================================================================
if 'predictions' not in st.session_state:
    st.session_state.predictions = []

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
st.markdown("<h1>Predicting Flight Delays<br/><em style='font-style:italic;color:#C9A77A;'>Before Takeoff</em></h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>"
    "A machine learning model trained on 2,201 commercial flights between "
    "Washington, D.C. and New York in January 2004. Enter pre-departure details "
    "to estimate delay probability."
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='hero-image-wrap'>"
    f"<img src='{HERO_IMAGE}' alt='Aerial flight view'/>"
    f"<div class='hero-overlay'>"
    f"<div class='hero-overlay-title'>\"Predict the unpredictable.\"</div>"
    f"<div class='hero-overlay-sub'>MACHINE LEARNING · AVIATION · OPERATIONS</div>"
    f"</div>"
    f"</div>",
    unsafe_allow_html=True,
)

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
    flight_date = st.date_input(
        "Flight Date",
        value=date(2004, 1, 15),
        min_value=date(2004, 1, 1),
        max_value=date(2004, 1, 31),
        help="Training data covers January 2004",
    )

    day_week = flight_date.weekday() + 1
    day_of_month = flight_date.day

    day_dict = info['categorical_unique_values']['DAY_WEEK']
    st.caption(f"📅 {day_dict[day_week]} · Day {day_of_month} of January 2004")

    # ---- Single time picker replaces hour + minute sliders ----
    departure_time = st.time_input(
        "Departure Time",
        value=time(14, 0),  # default 2:00 PM
        step=300,           # 5-minute steps when using arrows
        help="Scheduled departure time (browser shows AM/PM)",
    )

    # Derive hour and minute for the model
    dep_hour = departure_time.hour
    dep_minute = departure_time.minute

    # Friendly 12-hour display caption so users have NO doubt about AM/PM
    period = "AM" if dep_hour < 12 else "PM"
    display_hour = dep_hour if 1 <= dep_hour <= 12 else (dep_hour - 12 if dep_hour > 12 else 12)
    st.caption(f"🕐 {display_hour}:{dep_minute:02d} {period}")

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
# Predict button — appends to session_state
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
    delay_prob = float(probabilities[1])
    ontime_prob = float(probabilities[0])

    if delay_prob >= 0.7:
        status_text, status_color = "HIGH RISK", "#E86E6E"
    elif delay_prob >= 0.5:
        status_text, status_color = "MODERATE RISK", "#C9A77A"
    elif delay_prob >= 0.3:
        status_text, status_color = "LOW RISK", "#C9A77A"
    else:
        status_text, status_color = "ON-TIME", "#7CC48E"

    # Build 12-hour formatted time for display in the result card
    period = "AM" if dep_hour < 12 else "PM"
    display_hour = dep_hour if 1 <= dep_hour <= 12 else (dep_hour - 12 if dep_hour > 12 else 12)
    pretty_time = f"{display_hour}:{dep_minute:02d} {period}"

    prediction_record = {
        "delay_prob": delay_prob,
        "ontime_prob": ontime_prob,
        "status_text": status_text,
        "status_color": status_color,
        "origin": origin_label,
        "dest": dest_label,
        "carrier_code": carrier_label,
        "carrier_name": carrier_dict[carrier_label],
        "day_name": day_dict[day_week],
        "date_full": flight_date.strftime("%b %d, %Y"),
        "date_short": flight_date.strftime("%b %-d"),
        "distance": distance,
        "dep_time": pretty_time,
        "weather_text": "Adverse" if weather else "Clear",
        "model_name": "Random Forest" if model_choice == "random_forest" else "Logistic Regression",
        "subtitle": f"{carrier_label} · {flight_date.strftime('%a')} {pretty_time}",
    }
    st.session_state.predictions.append(prediction_record)

# =============================================================================
# Results carousel
# =============================================================================
predictions = st.session_state.predictions

if len(predictions) == 0:
    st.markdown(
        "<div style='text-align:center; padding: 3rem 1rem; border: 1px dashed rgba(232,224,210,0.15); border-radius: 24px; margin-top: 1rem;'>"
        "<div style='font-family: Playfair Display, serif; font-size: 1.5rem; color: #6E6A5E; font-style: italic;'>Your predictions will appear here</div>"
        "<div style='font-size: 0.85rem; color: #6E6A5E; margin-top: 0.5rem; letter-spacing: 0.05em;'>Click <b>RUN PREDICTION</b> above to add your first card</div>"
        "</div>",
        unsafe_allow_html=True,
    )
else:
    predictions_json = json.dumps(predictions)
    total = len(predictions)

    hdr_col1, hdr_col2, hdr_col3 = st.columns([1, 2, 1])
    with hdr_col1:
        st.markdown(f"<div class='eyebrow' style='margin-bottom:0; padding-top:1rem;'>PREDICTIONS · {total}</div>", unsafe_allow_html=True)
    with hdr_col3:
        st.markdown("<div class='clear-btn-wrap' style='text-align:right;'>", unsafe_allow_html=True)
        if st.button("CLEAR HISTORY", key="clear_history"):
            st.session_state.predictions = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    carousel_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;900&family=Inter:wght@300;400;500;600;700&display=swap');
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: transparent;
            font-family: 'Inter', sans-serif;
            min-height: 700px;
            overflow: hidden;
            user-select: none;
        }}
        .carousel-container {{
            position: relative;
            width: 100%;
            height: 640px;
            display: flex;
            align-items: center;
            justify-content: center;
            perspective: 1500px;
        }}
        .carousel-track {{
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .ticket-card {{
            position: absolute;
            width: 360px;
            height: 540px;
            border-radius: 24px;
            overflow: hidden;
            background: linear-gradient(145deg, #1A1F2A 0%, #161B22 100%);
            border: 1px solid rgba(232, 224, 210, 0.08);
            transform-style: preserve-3d;
            transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1),
                        opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            cursor: pointer;
        }}
        .ticket-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #C9A77A, #E8E0D2, #C9A77A);
            z-index: 5;
        }}
        .pos-active {{ transform: translateX(0) scale(1) rotateY(0); opacity: 1; z-index: 10; }}
        .pos-prev {{ transform: translateX(-360px) scale(0.78) rotateY(20deg); opacity: 0.5; z-index: 5; filter: brightness(0.7); }}
        .pos-next {{ transform: translateX(360px) scale(0.78) rotateY(-20deg); opacity: 0.5; z-index: 5; filter: brightness(0.7); }}
        .pos-prev-far {{ transform: translateX(-540px) scale(0.6) rotateY(25deg); opacity: 0; z-index: 1; pointer-events: none; }}
        .pos-next-far {{ transform: translateX(540px) scale(0.6) rotateY(-25deg); opacity: 0; z-index: 1; pointer-events: none; }}
        .pos-active:hover {{
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.6),
                        0 0 60px var(--glow, rgba(201, 167, 122, 0.4));
        }}
        .shine {{
            position: absolute;
            inset: 0;
            border-radius: 24px;
            background: radial-gradient(circle at var(--mx, 50%) var(--my, 50%), rgba(201, 167, 122, 0.2) 0%, rgba(201, 167, 122, 0) 50%);
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            z-index: 4;
        }}
        .pos-active:hover .shine {{ opacity: 1; }}
        .card-image-wrap {{
            position: relative;
            height: 160px;
            overflow: hidden;
        }}
        .card-image-wrap img {{
            width: 100%; height: 100%;
            object-fit: cover;
            filter: brightness(0.5) saturate(0.85);
        }}
        .card-image-wrap::after {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(14,17,22,0.3) 0%, rgba(26,31,42,1) 100%);
        }}
        .card-image-overlay {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            z-index: 2;
            padding: 1.25rem 1.5rem 0.75rem 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .card-eyebrow {{
            font-size: 0.6rem;
            font-weight: 600;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: #C9A77A;
        }}
        .card-route {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .card-route-code {{
            font-family: 'Playfair Display', serif;
            font-size: 1.9rem;
            font-weight: 700;
            color: #E8E0D2;
            letter-spacing: 0.05em;
            text-shadow: 0 2px 12px rgba(0,0,0,0.5);
        }}
        .card-route-line {{
            flex: 1;
            margin: 0 0.6rem;
            position: relative;
            height: 1px;
            background: rgba(232, 224, 210, 0.4);
        }}
        .card-route-line::before {{
            content: '✈';
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background: rgba(14,17,22,0.85);
            padding: 0.25rem 0.55rem;
            border-radius: 100px;
            color: #C9A77A;
            font-size: 0.75rem;
            border: 1px solid rgba(201,167,122,0.3);
        }}
        .card-subtitle {{
            font-size: 0.7rem;
            color: #9A9486;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            text-shadow: 0 1px 4px rgba(0,0,0,0.5);
        }}
        .card-body {{
            padding: 1rem 1.5rem 1.25rem 1.5rem;
        }}
        .prob-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 1rem;
        }}
        .prob-num {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            font-weight: 700;
            line-height: 1;
            letter-spacing: -0.04em;
        }}
        .prob-label {{
            font-size: 0.55rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: #6E6A5E;
            margin-top: 0.3rem;
        }}
        .time-display {{
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem;
            font-weight: 600;
            color: #E8E0D2;
            text-align: right;
        }}
        .time-label {{
            font-size: 0.55rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: #6E6A5E;
            margin-top: 0.3rem;
            text-align: right;
        }}
        .status-pill {{
            display: inline-block;
            padding: 0.35rem 0.85rem;
            border-radius: 100px;
            font-size: 0.6rem;
            font-weight: 600;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-top: 0.4rem;
            background: rgba(255, 255, 255, 0.05);
        }}
        .detail-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.45rem 0;
            border-bottom: 1px dashed rgba(232, 224, 210, 0.08);
        }}
        .detail-row:last-child {{ border-bottom: none; }}
        .detail-label {{
            font-size: 0.6rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: #6E6A5E;
        }}
        .detail-value {{
            font-size: 0.8rem;
            color: #E8E0D2;
            font-weight: 500;
        }}
        .nav-arrow {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: rgba(22, 27, 34, 0.9);
            border: 1px solid rgba(201, 167, 122, 0.3);
            color: #C9A77A;
            font-size: 1.2rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 20;
            transition: all 0.2s ease;
            backdrop-filter: blur(10px);
        }}
        .nav-arrow:hover:not(:disabled) {{
            background: #C9A77A;
            color: #0E1116;
            border-color: #C9A77A;
            transform: translateY(-50%) scale(1.1);
        }}
        .nav-arrow:disabled {{
            opacity: 0.25;
            cursor: not-allowed;
        }}
        .nav-arrow.prev {{ left: 5%; }}
        .nav-arrow.next {{ right: 5%; }}
        .counter {{
            text-align: center;
            margin-top: 1rem;
            font-size: 0.7rem;
            letter-spacing: 0.3em;
            color: #6E6A5E;
            font-weight: 500;
        }}
        .counter-current {{
            color: #C9A77A;
            font-size: 1rem;
            font-family: 'Playfair Display', serif;
            font-weight: 600;
        }}
        .dots {{
            display: flex;
            justify-content: center;
            gap: 6px;
            margin-top: 0.75rem;
        }}
        .dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: rgba(232, 224, 210, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .dot.active {{
            background: #C9A77A;
            width: 24px;
            border-radius: 3px;
        }}
        .dot:hover:not(.active) {{
            background: rgba(232, 224, 210, 0.4);
        }}
    </style>
    </head>
    <body>
        <div class='carousel-container' id='carousel'>
            <button class='nav-arrow prev' id='prevBtn' aria-label='Previous'>‹</button>
            <div class='carousel-track' id='track'></div>
            <button class='nav-arrow next' id='nextBtn' aria-label='Next'>›</button>
        </div>
        <div class='counter'>
            <span class='counter-current' id='counterCurrent'>1</span>
            <span style='margin: 0 0.5rem;'>/</span>
            <span id='counterTotal'>1</span>
        </div>
        <div class='dots' id='dots'></div>
        <script>
            const predictions = {predictions_json};
            let activeIndex = predictions.length - 1;
            const track = document.getElementById('track');
            const prevBtn = document.getElementById('prevBtn');
            const nextBtn = document.getElementById('nextBtn');
            const counterCurrent = document.getElementById('counterCurrent');
            const counterTotal = document.getElementById('counterTotal');
            const dotsContainer = document.getElementById('dots');
            const TILT_RANGE = 10;

            function makeCard(p, index) {{
                const card = document.createElement('div');
                card.className = 'ticket-card';
                card.dataset.index = index;
                card.style.setProperty('--glow', `${{p.status_color}}66`);
                const escape = (s) => String(s).replace(/[&<>'"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}})[c]);
                card.innerHTML = `
                    <div class='shine'></div>
                    <div class='card-image-wrap'>
                        <img src='{TICKET_IMAGE}' alt='Flight'/>
                        <div class='card-image-overlay'>
                            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                                <div class='card-eyebrow'>PREDICTION #${{index + 1}}</div>
                                <div class='card-subtitle'>${{escape(p.subtitle)}}</div>
                            </div>
                            <div class='card-route'>
                                <div class='card-route-code'>${{escape(p.origin)}}</div>
                                <div class='card-route-line'></div>
                                <div class='card-route-code'>${{escape(p.dest)}}</div>
                            </div>
                        </div>
                    </div>
                    <div class='card-body'>
                        <div class='prob-row'>
                            <div>
                                <div class='prob-num' style='color:${{p.status_color}};'>${{(p.delay_prob * 100).toFixed(1)}}%</div>
                                <div class='prob-label'>DELAY PROBABILITY</div>
                                <div class='status-pill' style='color:${{p.status_color}}; border:1px solid ${{p.status_color}}55;'>${{escape(p.status_text)}}</div>
                            </div>
                            <div>
                                <div class='time-display'>${{escape(p.dep_time)}}</div>
                                <div class='time-label'>DEPARTURE</div>
                            </div>
                        </div>
                        <div>
                            <div class='detail-row'><div class='detail-label'>Carrier</div><div class='detail-value'>${{escape(p.carrier_name)}}</div></div>
                            <div class='detail-row'><div class='detail-label'>Date</div><div class='detail-value'>${{escape(p.day_name)}}, ${{escape(p.date_full)}}</div></div>
                            <div class='detail-row'><div class='detail-label'>Distance</div><div class='detail-value'>${{p.distance}} mi</div></div>
                            <div class='detail-row'><div class='detail-label'>Weather</div><div class='detail-value'>${{escape(p.weather_text)}}</div></div>
                            <div class='detail-row'><div class='detail-label'>Model</div><div class='detail-value'>${{escape(p.model_name)}}</div></div>
                        </div>
                    </div>
                `;
                card.addEventListener('click', () => {{
                    if (parseInt(card.dataset.index) !== activeIndex) {{
                        activeIndex = parseInt(card.dataset.index);
                        render();
                    }}
                }});
                return card;
            }}

            function applyPositions() {{
                const cards = track.querySelectorAll('.ticket-card');
                cards.forEach(card => {{
                    const idx = parseInt(card.dataset.index);
                    card.classList.remove('pos-active', 'pos-prev', 'pos-next', 'pos-prev-far', 'pos-next-far');
                    if (idx === activeIndex) card.classList.add('pos-active');
                    else if (idx === activeIndex - 1) card.classList.add('pos-prev');
                    else if (idx === activeIndex + 1) card.classList.add('pos-next');
                    else if (idx < activeIndex - 1) card.classList.add('pos-prev-far');
                    else card.classList.add('pos-next-far');
                }});
                counterCurrent.textContent = activeIndex + 1;
                counterTotal.textContent = predictions.length;
                prevBtn.disabled = activeIndex === 0;
                nextBtn.disabled = activeIndex === predictions.length - 1;
                const dots = dotsContainer.querySelectorAll('.dot');
                dots.forEach((dot, i) => dot.classList.toggle('active', i === activeIndex));
            }}

            function render() {{ applyPositions(); }}

            predictions.forEach((p, i) => track.appendChild(makeCard(p, i)));
            predictions.forEach((_, i) => {{
                const dot = document.createElement('div');
                dot.className = 'dot';
                dot.addEventListener('click', () => {{ activeIndex = i; render(); }});
                dotsContainer.appendChild(dot);
            }});

            prevBtn.addEventListener('click', () => {{ if (activeIndex > 0) {{ activeIndex--; render(); }} }});
            nextBtn.addEventListener('click', () => {{ if (activeIndex < predictions.length - 1) {{ activeIndex++; render(); }} }});

            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft' && activeIndex > 0) {{ activeIndex--; render(); }}
                else if (e.key === 'ArrowRight' && activeIndex < predictions.length - 1) {{ activeIndex++; render(); }}
            }});

            document.addEventListener('mousemove', (e) => {{
                const activeCard = track.querySelector('.pos-active');
                if (!activeCard) return;
                const rect = activeCard.getBoundingClientRect();
                const cx = rect.left + rect.width / 2;
                const cy = rect.top + rect.height / 2;
                const x = e.clientX - cx;
                const y = e.clientY - cy;
                if (Math.abs(x) < rect.width * 0.8 && Math.abs(y) < rect.height * 0.8) {{
                    const rotateY = (x / (rect.width / 2)) * TILT_RANGE;
                    const rotateX = -(y / (rect.height / 2)) * TILT_RANGE;
                    activeCard.style.transform = `translateX(0) scale(1.02) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
                    const shine = activeCard.querySelector('.shine');
                    if (shine) {{
                        shine.style.setProperty('--mx', `${{((e.clientX - rect.left) / rect.width) * 100}}%`);
                        shine.style.setProperty('--my', `${{((e.clientY - rect.top) / rect.height) * 100}}%`);
                    }}
                }} else {{
                    activeCard.style.transform = '';
                }}
            }});

            render();
        </script>
    </body>
    </html>
    """
    components.html(carousel_html, height=720)
