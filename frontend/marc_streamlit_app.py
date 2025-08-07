import streamlit as st
import streamlit.components.v1 as components
import requests

# -- Config
BACKEND_URL = "https://mvp1-581249984477.europe-west1.run.app/predict"
PRESENTATION_IFRAME = """
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vSd6sqMH6BgucBaB7Evgw9VlVbc93lF7jjsKkO7PlNmoI84wCqUHbjUoKXNYtoxXO8MeLF-oCLlBoB1/pubembed?start=false&loop=false&delayms=3000"
  frameborder="0" width="100%" height="600" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
"""
PRESENTATION_DOWNLOAD = "https://onedrive.live.com/download?resid=591D3DA00F260D17%211352&authkey=!ANL3EMmxUjDFm2g"

# -- Conditions
conditions_list = [
    'Pain', 'Other', 'High Blood Pressure', 'Depression', 'Birth Control',
    'Neuropathic Pain', 'Chronic Trouble Sleeping', 'Type 2 Diabetes Mellitus',
    'Attention Deficit Disorder with Hyperactivity', 'Bipolar Depression',
    'Migraine Prevention', 'Panic Disorder', 'Major Depressive Disorder', 'Overweight',
    'Repeated Episodes of Anxiety', 'Rheumatoid Arthritis', 'High Cholesterol',
    'Disorder characterized by Stiff, Tender & Painful Muscles', 'Migraine Headache',
    'Underactive Thyroid', 'Chronic Pain', 'Anxious', 'Acne', 'Cough',
    '"Change of Life" Signs', 'Asthma', 'Joint Damage causing Pain and Loss of Function',
    'Pain Originating From a Nerve', 'Condition in which Stomach Acid is Pushed Into the Esophagus',
    'Stop Smoking', 'Muscle Spasm', 'Emptying of the Bowel', 'Osteoporosis',
    'Decreased Bone Mass Following Menopause', 'Combined High Blood Cholesterol and Triglyceride Level',
    'Chronic Pain with Narcotic Drug Tolerance', 'Bacterial Urinary Tract Infection',
    'Abnormally Long or Heavy Periods', 'Enlarged Prostate', 'Inflammation of the Nose due to an Allergy',
    'Disease of Ovaries with Cysts', 'Osteoarthritis of the Knee', 'Epileptic Seizure',
    'Painful Periods', 'Extreme Discomfort in Calves when Sitting or Lying Down',
    'Inability to have an Erection', 'Bipolar I Disorder with Most Recent Episode Mixed',
    'Yeast Infection of Vagina and Vulva', 'Manic-Depression',
    'Acute Bacterial Infection of the Sinuses'
]

# -- Custom CSS Styling
st.markdown("""
<style>
    /* Main app styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Title styling */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-align: center !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Section headers */
    .section-header {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin: 1.5rem 0 !important;
        padding: 1rem !important;
        background: linear-gradient(90deg, #74b9ff, #0984e3);
        border-radius: 15px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* Form container */
    .form-container {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 2.5rem !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        margin: 2rem 0 !important;
        border: 2px solid #e74c3c !important;
    }
    
    /* Input labels */
    .stSelectbox label, .stNumberInput label, .stSlider label, .stTextInput label, .stTextArea label {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Radio button styling */
    .stRadio label {
        font-size: 1.6rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
    }
    
    /* Input fields */
    .stSelectbox div[data-baseweb="select"],
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        font-size: 1.3rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    /* Slider values */
    .stSlider .st-bd {
        font-size: 1.3rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 4px 15px rgba(238, 90, 36, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(238, 90, 36, 0.6) !important;
    }
    
    /* Reset button styling */
    .reset-button {
        background: linear-gradient(45deg, #74b9ff, #0984e3) !important;
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.4) !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(45deg, #00b894, #00cec9) !important;
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3) !important;
        margin: 1rem 0 !important;
    }
    
    /* Error message styling */
    .error-message {
        background: linear-gradient(45deg, #e17055, #d63031) !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 1.5rem !important;
        border-radius: 15px !important;
        text-align: center !important;
        box-shadow: 0 4px 15px rgba(225, 112, 85, 0.3) !important;
        margin: 1rem 0 !important;
    }
    
    /* Presentation container */
    .presentation-container {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
        margin: 2rem 0 !important;
    }
    
    /* Download link styling */
    .download-link {
        display: inline-block !important;
        background: linear-gradient(45deg, #6c5ce7, #a29bfe) !important;
        color: white !important;
        text-decoration: none !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 1rem 2rem !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.4) !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }
    
    .download-link:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(108, 92, 231, 0.6) !important;
        text-decoration: none !important;
        color: white !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -- Page Config
st.set_page_config(page_title="💊 Drug Recommendation App", layout="centered", initial_sidebar_state="collapsed")

# Custom title with animation
st.markdown('<h1 class="main-title">💊 Drug Recommendation App</h1>', unsafe_allow_html=True)

# Initialize session state if not exists
if "age" not in st.session_state:
    st.session_state["age"] = 25
if "gender" not in st.session_state:
    st.session_state["gender"] = "male"
if "condition" not in st.session_state:
    st.session_state["condition"] = "Pain"
if "effectiveness" not in st.session_state:
    st.session_state["effectiveness"] = 3
if "ease_of_use" not in st.session_state:
    st.session_state["ease_of_use"] = 3
if "satisfaction" not in st.session_state:
    st.session_state["satisfaction"] = 3
if "reset_form" not in st.session_state:
    st.session_state["reset_form"] = False

# -- Navigation UI with enhanced styling
st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
view_choice = st.radio(
    "🎯 Choose what you want to do:",
    ["🎬 View Presentation", "💊 Use the App"],
    horizontal=True
)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# 🎬 View Presentation
# -------------------------
if view_choice == "🎬 View Presentation":
    st.markdown('<div class="presentation-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">🎬 Project Presentation</h2>', unsafe_allow_html=True)
    components.html(PRESENTATION_IFRAME, height=550)
    st.markdown(f'<a href="{PRESENTATION_DOWNLOAD}" class="download-link" target="_blank">⬇️ Download PDF Presentation</a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# 💊 Use the App
# -------------------------
elif view_choice == "💊 Use the App":
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">💊 Get Your Personalized Medicine Recommendation</h2>', unsafe_allow_html=True)

    # Handle reset form
    if st.session_state.get("reset_form", False):
        st.session_state["age"] = 25
        st.session_state["gender"] = "male"
        st.session_state["condition"] = "Pain"
        st.session_state["effectiveness"] = 3
        st.session_state["ease_of_use"] = 3
        st.session_state["satisfaction"] = 3
        st.session_state["reset_form"] = False

    with st.form("medicine_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input(
                "👤 Age", 
                min_value=0, 
                max_value=120, 
                step=1, 
                value=st.session_state["age"],
                key="age"
            )
            gender = st.selectbox(
                "⚧️ Gender", 
                ["male", "female"], 
                index=0 if st.session_state["gender"] == "male" else 1,
                key="gender"
            )
            condition = st.selectbox(
                "🏥 Medical Condition", 
                conditions_list, 
                index=conditions_list.index(st.session_state["condition"]),
                key="condition"
            )
        
        with col2:
            effectiveness = st.slider(
                "⭐ Desired Effectiveness", 
                1, 5, 
                value=st.session_state["effectiveness"],
                key="effectiveness"
            )
            ease_of_use = st.slider(
                "🎯 Ease of Use", 
                1, 5, 
                value=st.session_state["ease_of_use"],
                key="ease_of_use"
            )
            satisfaction = st.slider(
                "😊 Expected Satisfaction", 
                1, 5, 
                value=st.session_state["satisfaction"],
                key="satisfaction"
            )

        # Form buttons
        col_submit, col_reset = st.columns([2, 1])
        
        with col_submit:
            submitted = st.form_submit_button("🚀 Get My Recommendation", use_container_width=True)
        
        with col_reset:
            reset_clicked = st.form_submit_button("🔄 Reset Form", use_container_width=True)

    # Handle reset button click
    if reset_clicked:
        st.session_state["reset_form"] = True
        st.rerun()

    # Handle form submission
    if submitted:
        data = {
            "age": st.session_state["age"],
            "gender": st.session_state["gender"],
            "condition": st.session_state["condition"],
            "effectiveness": st.session_state["effectiveness"],
            "ease_of_use": st.session_state["ease_of_use"],
            "satisfaction": st.session_state["satisfaction"]
        }

        # Show loading spinner
        with st.spinner('🔍 Analyzing your profile and finding the best recommendation...'):
            try:
                response = requests.post(BACKEND_URL, json=data, timeout=30)
                if response.status_code == 200:
                    recommendation = response.json().get("medicine", "No recommendation found.")
                    st.markdown(f'''
                    <div class="success-message">
                        <h3>🎉 Your Personalized Recommendation</h3>
                        <p style="font-size: 1.5rem; margin: 1rem 0;">
                            <strong>💊 {recommendation}</strong>
                        </p>
                        <p style="font-size: 1rem; opacity: 0.9;">
                            This recommendation is based on your profile and preferences. 
                            Please consult with your healthcare provider before taking any medication.
                        </p>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="error-message">
                        <h3>❌ Error Occurred</h3>
                        <p>Error {response.status_code}: {response.text}</p>
                        <p>Please try again or contact support if the problem persists.</p>
                    </div>
                    ''', unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown('''
                <div class="error-message">
                    <h3>⏰ Request Timeout</h3>
                    <p>The request took too long to process. Please try again.</p>
                </div>
                ''', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'''
                <div class="error-message">
                    <h3>⚠️ Connection Error</h3>
                    <p>Request failed: {str(e)}</p>
                    <p>Please check your internet connection and try again.</p>
                </div>
                ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 15px;">
    <p style="color: #2c3e50; font-size: 1.1rem; font-weight: 500;">
        🏥 <strong>Disclaimer:</strong> This app provides suggestions based on data analysis. 
        Always consult with qualified healthcare professionals before making medical decisions.
    </p>
    <p style="color: #74b9ff; font-size: 1rem; margin-top: 1rem;">
        Made with ❤️ using Streamlit | © 2024 Drug Recommendation System
    </p>
</div>
""", unsafe_allow_html=True)
