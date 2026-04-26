"""
Flight Delay Predictor — Streamlit App
Asian Avengers · CIS 412 · Spring 2026
"""
import streamlit as st
import pandas as pd
import pickle

# =============================================================================
# Page config (must be the first Streamlit call)
# =============================================================================
st.set_page_config(
    page_title="Flight Delay Predictor",
    page_icon="✈️",
    layout="wide",
)

# =============================================================================
# Custom CSS — matches the rose-gold deck aesthetic
# =============================================================================
st.markdown("""
<style>
    .main { background-color: #EDE4DA; }
    .stApp { background-color: #EDE4DA; }
    h1, h2, h3 { color: #B08968 !important; font-family: 'Georgia', serif; }
    .stButton>button {
        background-color: #B08968;
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #8B6F47;
        color: white;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #B08968;
        margin-bottom: 1rem;
    }
    div[data-testid="stMetricValue"] { color: #2C2C2C; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Load model and metadata
# =============================================================================
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as f:        # 'rb' = read binary
        return pickle.load(f)

@st.cache_resource
def load_data_info():
    with open('data_info.pkl', 'rb') as f:
        return pickle.load(f)

models = load_model()
info = load_data_info()

# =============================================================================
# Header
# =============================================================================
st.title("✈️ Predicting Flight Delays Before Takeoff")
st.markdown(
    "<p style='color: #6B6056; font-size: 1.1rem;'>"
    "A Machine Learning Approach Using 2004 DC-to-NY Commercial Flight Data"
    "</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# =============================================================================
# Sidebar — model selector and info
# =============================================================================
with st.sidebar:
    st.header("⚙️ Model Settings")

    model_choice = st.radio(
        "Select Model",
        options=['random_forest', 'logistic_regression'],
        format_func=lambda x: 'Random Forest' if x == 'random_forest' else 'Logistic Regression',
    )

    st.markdown("---")
    st.subheader("📊 Model Performance")
    metrics = info['model_metrics'][model_choice]
    st.metric("Test Accuracy", f"{metrics['test_accuracy']:.1%}")
    st.metric("Test F1 Score", f"{metrics['test_f1']:.1%}")
    st.metric("Test Recall", f"{metrics['test_recall']:.1%}")

    st.markdown("---")
    st.caption(
        "**Asian Avengers** · CIS 412 · Spring 2026\n\n"
        "Trained on 2,201 flights from January 2004 (DC → NY corridor)."
    )

# =============================================================================
# Input form
# =============================================================================
st.subheader("Flight Details")

col1, col2 = st.columns(2)

with col1:
    # CARRIER dropdown — show friendly labels, store original code
    carrier_dict = info['categorical_unique_values']['CARRIER']
    carrier_label = st.selectbox(
        "Carrier",
        options=list(carrier_dict.keys()),
        format_func=lambda code: carrier_dict[code],
        index=2,  # Default: DL
    )

    origin_dict = info['categorical_unique_values']['ORIGIN']
    origin_label = st.selectbox(
        "Origin Airport",
        options=list(origin_dict.keys()),
        format_func=lambda code: origin_dict[code],
        index=1,  # Default: DCA
    )

    dest_dict = info['categorical_unique_values']['DEST']
    dest_label = st.selectbox(
        "Destination Airport",
        options=list(dest_dict.keys()),
        format_func=lambda code: dest_dict[code],
        index=1,  # Default: JFK
    )

    distance_min, distance_max, distance_default = info['numeric_ranges']['DISTANCE']
    distance = st.slider("Flight Distance (miles)", distance_min, distance_max, distance_default)

with col2:
    day_dict = info['categorical_unique_values']['DAY_WEEK']
    day_week = st.selectbox(
        "Day of Week",
        options=list(day_dict.keys()),
        format_func=lambda d: day_dict[d],
        index=2,
    )

    dom_min, dom_max, dom_default = info['numeric_ranges']['DAY_OF_MONTH']
    day_of_month = st.slider("Day of Month", dom_min, dom_max, dom_default)

    h_min, h_max, h_default = info['numeric_ranges']['CRS_DEP_HOUR']
    dep_hour = st.slider(f"Scheduled Departure Hour", h_min, h_max, h_default)

    m_min, m_max, m_default = info['numeric_ranges']['CRS_DEP_MINUTE']
    dep_minute = st.slider("Scheduled Departure Minute", m_min, m_max, m_default)

    weather_checked = st.checkbox("⛈️ Adverse weather forecasted", value=False)
    weather = 1 if weather_checked else 0

st.markdown("---")

# =============================================================================
# Prediction logic
# =============================================================================
def build_input_row(carrier, origin, dest, distance, weather, day_week,
                    day_of_month, dep_hour, dep_minute, expected_columns):
    """Build a feature row matching the training schema exactly.

    Replicates the same encoding the notebook used:
    - Numeric columns kept as-is
    - One-hot encode CARRIER, DEST, ORIGIN with drop_first=True
    - All output columns aligned to expected_columns (fills missing with 0)
    """
    # Start with all expected columns set to 0
    row = {col: 0 for col in expected_columns}

    # Fill numeric columns
    row['DISTANCE'] = distance
    row['Weather'] = weather
    row['DAY_WEEK'] = day_week
    row['DAY_OF_MONTH'] = day_of_month
    row['MONTH'] = 1  # All training data was January
    row['CRS_DEP_HOUR'] = dep_hour
    row['CRS_DEP_MINUTE'] = dep_minute

    # One-hot encode categoricals (drop_first=True style — first value is reference)
    # CARRIER reference is the alphabetically first (CO), all others get a 1 if matched
    carrier_col = f'CARRIER_{carrier}'
    if carrier_col in row:
        row[carrier_col] = 1

    origin_col = f'ORIGIN_{origin}'
    if origin_col in row:
        row[origin_col] = 1

    dest_col = f'DEST_{dest}'
    if dest_col in row:
        row[dest_col] = 1

    # Build DataFrame in the EXACT column order the model expects
    return pd.DataFrame([row])[expected_columns]


# =============================================================================
# Prediction button
# =============================================================================
if st.button("🔮 PREDICT FLIGHT STATUS", use_container_width=True):

    # Build input
    input_df = build_input_row(
        carrier=carrier_label,
        origin=origin_label,
        dest=dest_label,
        distance=distance,
        weather=weather,
        day_week=day_week,
        day_of_month=day_of_month,
        dep_hour=dep_hour,
        dep_minute=dep_minute,
        expected_columns=info['expected_columns'],
    )

    # Predict
    selected_model = models[model_choice]
    prediction = selected_model.predict(input_df)[0]
    probabilities = selected_model.predict_proba(input_df)[0]

    delay_prob = probabilities[1]
    ontime_prob = probabilities[0]

    # =========================================================================
    # Results display
    # =========================================================================
    st.markdown("### Prediction Results")

    res_col1, res_col2, res_col3 = st.columns([1, 1, 1])

    with res_col1:
        if prediction == 1:
            st.error("### ⚠️ DELAYED")
            st.caption("Model predicts this flight will be delayed (≥15 min)")
        else:
            st.success("### ✅ ON-TIME")
            st.caption("Model predicts this flight will arrive on time")

    with res_col2:
        st.metric("Delay Probability", f"{delay_prob:.1%}")

    with res_col3:
        st.metric("On-Time Probability", f"{ontime_prob:.1%}")

    # Probability bar
    st.markdown("#### Probability Breakdown")
    prob_df = pd.DataFrame({
        'Status': ['On-Time', 'Delayed'],
        'Probability': [ontime_prob, delay_prob],
    })
    st.bar_chart(prob_df.set_index('Status'), color='#B08968')

    # Risk interpretation
    if delay_prob >= 0.7:
        st.warning("🔴 **High delay risk** — Consider buffer time for connections.")
    elif delay_prob >= 0.5:
        st.warning("🟠 **Moderate delay risk** — Possible disruption.")
    elif delay_prob >= 0.3:
        st.info("🟡 **Low delay risk** — Likely on-time but monitor.")
    else:
        st.success("🟢 **Very likely on-time** — Standard flight conditions.")

# =============================================================================
# Footer
# =============================================================================
st.markdown("---")
st.caption(
    "⚠️ This model is trained on historical 2004 data and is for educational "
    "purposes only. Current flight predictions would require retraining on "
    "recent data."
)
