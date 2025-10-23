import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
import os

# --- Get Absolute Path to Files ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
IMAGE_PATH = os.path.join(BASE_DIR, "house.jpg") 
SOUND_PATH = os.path.join(BASE_DIR, "great-success-384935.mp3")

# --- Page Configuration ---
st.set_page_config(
    page_title="EstimaHome - California",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded" # <-- Make sidebar open by default
)

# --- Function to load and encode image ---
@st.cache_data
def get_image_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Image file not found at: {file_path}. Please ensure 'house.jpg' is in the same folder as 'app.py'.") 
        return None

# --- Function to load and encode audio ---
@st.cache_data
def get_audio_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.warning(f"Sound file not found at: {file_path}. Prediction will work without sound.")
        return None

# --- Get encoded files ---
img_base64 = get_image_as_base64(IMAGE_PATH)
audio_base64 = get_audio_as_base64(SOUND_PATH)

# --- CSS Styling ---
if img_base64:
    background_css = f"""
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #FAFAFA;
        position: relative;
        padding-top: 5vh; 
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(15, 12, 41, 0.4); 
        z-index: 0; 
    }}
    """
else:
    background_css = """
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #FAFAFA;
        padding-top: 5vh;
    }}
    """

st.markdown(f"""
    <style>
    /* --- Apply background style --- */
    {background_css}

    /* --- Style the main content area (to be transparent) --- */
    [data-testid="stVerticalBlock"] {{
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        z-index: 1; /* Ensure title is above overlay */
    }}

    /* --- NEW: Style the Sidebar --- */
    [data-testid="stSidebar"] {{
        background: rgba(0, 0, 0, 0.4); /* Dark transparency */
        backdrop-filter: blur(15px); /* Frosted glass effect */
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1); /* Subtle edge */
        padding: 1.5rem;
        
        /* --- ADDED FOR SCROLLING --- */
        max-height: 100vh; /* Set max height to viewport height */
        overflow-y: auto;  /* Enable vertical scroll */
        overflow-x: hidden; /* Disable horizontal scroll */
        
        /* --- Firefox Scrollbar --- */
        scrollbar-width: thin;
        scrollbar-color: #2ECC71 rgba(0, 0, 0, 0.2);
    }}

    /* --- NEW: Webkit (Chrome/Safari) Scrollbar Styling --- */
    [data-testid="stSidebar"]::-webkit-scrollbar {{
        width: 8px;
    }}
    [data-testid="stSidebar"]::-webkit-scrollbar-track {{
        background: rgba(0, 0, 0, 0.2); /* Dark, transparent track */
        border-radius: 10px;
    }}
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {{
        background-color: #2ECC71; /* Green accent color */
        border-radius: 10px;
        border: 2px solid rgba(0, 0, 0, 0.2);
    }}
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {{
        background-color: #27AE60; /* Darker green on hover */
    }}


    /* --- Title (on main page) --- */
    h1, h3 {{
        text-align: center;
        color: #FFFFFF;
        text-shadow: 0 0 10px rgba(100, 220, 100, 0.7), 0 0 20px rgba(100, 220, 100, 0.5);
        z-index: 1;
        position: relative;
    }}
    h1 {{ font-size: 3rem; font-weight: 700; }}
    h3 {{ font-weight: 400; color: #E0E0E0; }}

    /* --- Subheaders (inside sidebar) --- */
    [data-testid="stSidebar"] h3 {{
        color: #FFFFFF; 
        text-shadow: 0 0 5px rgba(100, 220, 100, 0.5);
        text-align: left;
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1rem;
    }}

    /* --- Input Labels (inside sidebar) --- */
    [data-testid="stSidebar"] .stNumberInput label {{
        color: #E0E0E0 !important; 
        font-weight: 500;
        text-shadow: none;
    }}

    /* --- Input Widgets (inside sidebar) --- */
    [data-testid="stSidebar"] .stNumberInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.15); 
        color: #FAFAFA; 
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }}
    
    /* --- Number input buttons (inside sidebar) --- */
    [data-testid="stSidebar"] .stNumberInput button {{
        color: #2ECC71 !important; 
        border: none !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }}
    [data-testid="stSidebar"] .stNumberInput button:hover {{
        background: #27AE60 !important; 
        color: #FFFFFF !important;
    }}

    /* --- Predict Button (inside sidebar) --- */
    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        margin: 2rem auto 0 auto;
        display: block;
        padding: 12px 30px;
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
        background: linear-gradient(90deg, #27AE60 0%, #2ECC71 100%);
        border: none;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.4);
        transition: all 0.3s ease;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(46, 204, 113, 0.6);
    }}

    /* --- Success Message (inside sidebar) --- */
    [data-testid="stSidebar"] .stSuccess {{
        background-color: rgba(30, 200, 130, 0.2); 
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid #1EC882;
        border-radius: 10px;
        text-align: center;
        padding: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
        color: #FFFFFF; 
    }}
    [data-testid="stSidebar"] .stSuccess strong {{
        color: #FFFFFF;
        font-weight: 700;
    }}
    </style>
""", unsafe_allow_html=True)


# --- Load Artifacts ---
@st.cache_resource
def load_model_and_transformers():
    try:
        model = joblib.load("ridge_model_california.pkl")
        scaler = joblib.load("feature_scaler_california.pkl")
        pt = joblib.load("power_transformer.pkl")
        skewed_cols = joblib.load("skewed_cols_list.pkl")
        return model, scaler, pt, skewed_cols
    except FileNotFoundError:
        st.error("Model artifacts not found. Please ensure all .pkl files are in the same directory.")
        return None, None, None, None

model, scaler, pt, skewed_cols = load_model_and_transformers()

# ... (MODEL_FEATURES list is unchanged) ...
MODEL_FEATURES = [
    'Median_Income', 'Median_Age', 'Tot_Rooms', 'Tot_Bedrooms', 'Population',
    'Households', 'Latitude', 'Longitude', 'Distance_to_coast', 'Distance_to_LA',
    'Distance_to_SanDiego', 'Distance_to_SanJose', 'Distance_to_SanFrancisco'
]

# --- App Layout ---
if model: 
    
    # --- Title Section (on main page) ---
    st.title("🏠 EstimaHome California")
    st.markdown("### Predict California house prices with AI precision ✨")

    # --- NEW: Inputs moved to Sidebar ---
    with st.sidebar:
        st.markdown("### Key Features")
        median_income = st.number_input("Median Income (in tens of thousands)", min_value=0.5, max_value=15.0, value=3.5, step=0.1)
        median_age = st.number_input("Median House Age (years)", min_value=1.0, max_value=100.0, value=29.0, step=1.0)
        latitude = st.number_input("Latitude", min_value=32.0, max_value=42.0, value=34.05, step=0.01)
        longitude = st.number_input("Longitude", min_value=-125.0, max_value=-114.0, value=-118.25, step=0.01)

        st.markdown("### Property Size")
        tot_rooms = st.number_input("Total Rooms in Block", min_value=10, max_value=50000, value=2000, step=100)
        tot_bedrooms = st.number_input("Total Bedrooms in Block", min_value=2, max_value=10000, value=400, step=50)
        population = st.number_input("Population in Block", min_value=3, max_value=40000, value=1200, step=100)
        households = st.number_input("Households in Block", min_value=1, max_value=10000, value=380, step=50)

        st.markdown("### Location (Proximity in km)")
        dist_coast = st.number_input("Distance to Coast", min_value=0.0, max_value=300.0, value=20.0, step=1.0)
        dist_la = st.number_input("Distance to Los Angeles", min_value=0.0, max_value=1000.0, value=10.0, step=1.0)
        dist_sd = st.number_input("Distance to San Diego", min_value=0.0, max_value=1000.0, value=180.0, step=1.0)
        dist_sj = st.number_input("Distance to San Jose", min_value=0.0, max_value=1000.0, value=500.0, step=1.0)
        dist_sf = st.number_input("Distance to San Francisco", min_value=0.0, max_value=1000.0, value=550.0, step=1.0)

        # --- Prediction Button (inside sidebar) ---
        if st.button("Predict House Price"):
            
            # 1. Create DataFrame
            input_data = pd.DataFrame([[
                median_income, median_age, tot_rooms, tot_bedrooms, population,
                households, latitude, longitude, dist_coast, dist_la,
                dist_sd, dist_sj, dist_sf
            ]], columns=MODEL_FEATURES)

            try:
                # 2. Apply PowerTransform
                if skewed_cols:
                    input_data[skewed_cols] = pt.transform(input_data[skewed_cols])

                # 3. Apply StandardScaler
                input_scaled = scaler.transform(input_data)

                # 4. Predict
                pred_log = model.predict(input_scaled)[0]

                # 5. Inverse Transform
                pred_original = np.expm1(pred_log)

                # Display Result
                st.success(f"**Estimated House Price:** ${pred_original:,.2f}")
                st.balloons()
                
                # --- Play success sound ---
                if audio_base64:
                    st.markdown(f"""
                        <audio autoplay="true">
                            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                        </audio>
                    """, unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

