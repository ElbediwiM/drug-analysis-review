import streamlit as st
import streamlit.components.v1 as components
import requests

# -- Config
BACKEND_URL = "https://mvp1-581249984477.europe-west1.run.app/predict"
PRESENTATION_IFRAME = """
<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vSd6sqMH6BgucBaB7Evgw9VlVbc93lF7jjsKkO7PlNmoI84wCqUHbjUoKXNYtoxXO8MeLF-oCLlBoB1/pubembed?start=false&loop=false&delayms=3000"
  frameborder="0" width="100%" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
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

# -- Page Config
st.set_page_config(
    page_title="Drug Recommendation App", 
    layout="centered", 
    page_icon="💊",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #fafafa;
        }
        
        /* Radio buttons styling */
        .st-bb {
            background-color: white;
        }
        
        /* Form elements */
        .stTextInput, .stNumberInput, .stSelectbox, .stSlider {
            background-color: white;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Buttons */
        .stButton>button {
            border: none;
            color: white;
            background-color: #4b2e83;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.3s;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #3a2368;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Reset button specific styling */
        .stButton>button:contains("Reset") {
            background-color: #6c757d;
        }
        
        /* Slider styling */
        .stSlider>div>div>div>div {
            background-color: #4b2e83;
        }
        
        /* Tooltip styling */
        .css-1qg05tj {
            background-color: #4b2e83 !important;
            color: white !important;
        }
        
        /* Custom card styling */
        .custom-card {
            background-color: #e8f4f8;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #4b2e83;
            margin-top: 20px;
        }
        
        /* Title styling */
        .custom-title {
            color: #4b2e83;
            font-family: "Arial Rounded MT Bold", sans-serif;
        }
        
        /* Recommendation text */
        .recommendation-text {
            font-size: 24px;
            font-weight: bold;
            color: #2c7be5;
        }
    </style>
""", unsafe_allow_html=True)

# Main title with emoji and custom styling
st.markdown("""
    <h1 class="custom-title" style='text-align: center;'>
        💊 Drug Recommendation App
    </h1>
""", unsafe_allow_html=True)

# Function to reset form fields
def reset_form():
    st.session_state["age"] = 0
    st.session_state["gender"] = "male"
    st.session_state["condition"] = "Pain"
    st.session_state["effectiveness"] = 3
    st.session_state["ease_of_use"] = 3
    st.session_state["satisfaction"] = 3

# -- Navigation UI with custom styling
st.markdown("""
    <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <h3 style='color: #4b2e83;'>Choose what you want to do:</h3>
""", unsafe_allow_html=True)

view_choice = st.radio("", ["View Presentation", "Use the App"], horizontal=True, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# :film_frames: View Presentation
# -------------------------
if view_choice == "View Presentation":
    st.markdown("""
        <div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #4b2e83;'>🎬 Project Presentation</h2>
        </div>
    """, unsafe_allow_html=True)
    
    components.html(PRESENTATION_IFRAME, height=550)
    
    st.markdown(f"""
        <div style='text-align: center; margin-top: 20px;'>
            <a href='{PRESENTATION_DOWNLOAD}' style='background-color: #4b2e83; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-weight: bold;'>
                ⬇️ Download PDF
            </a>
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# :pill: Use the App
# -------------------------
elif view_choice == "Use the App":
    st.markdown("""
        <div style='background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h2 style='color: #4b2e83;'>💊 Get Your Personalized Medicine Recommendation</h2>
        </div>
    """, unsafe_allow_html=True)

    with st.form("medicine_form"):
        # Create columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, step=1, key="age")
            gender = st.selectbox("Gender", ["male", "female"], key="gender")
            condition = st.selectbox("Medical condition", conditions_list, key="condition")
            
        with col2:
            effectiveness = st.slider("Desired effectiveness (1-5)", 1, 5, 3, key="effectiveness",
                                    help="1 = Not important, 5 = Very important")
            ease_of_use = st.slider("Ease of use (1-5)", 1, 5, 3, key="ease_of_use",
                                  help="1 = Not important, 5 = Very important")
            satisfaction = st.slider("Expected satisfaction (1-5)", 1, 5, 3, key="satisfaction",
                                   help="1 = Not important, 5 = Very important")
        
        # Form buttons in columns
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            submitted = st.form_submit_button("Get Recommendation", 
                                           help="Click to get your personalized medicine recommendation")
        
        with col_btn2:
            reset_clicked = st.form_submit_button("Reset Form", 
                                               help="Click to reset all fields to default values",
                                               on_click=reset_form)
        
        # Add some space
        st.markdown("<br>", unsafe_allow_html=True)

    if submitted:
        data = {
            "age": st.session_state["age"],
            "gender": st.session_state["gender"],
            "condition": st.session_state["condition"],
            "effectiveness": st.session_state.get("effectiveness", 3),
            "ease_of_use": st.session_state["ease_of_use"],
            "satisfaction": st.session_state["satisfaction"]
        }

        try:
            with st.spinner('🔍 Finding the best medicine for you...'):
                response = requests.post(BACKEND_URL, json=data)
                
            if response.status_code == 200:
                recommendation = response.json().get("medicine", "No recommendation found.")
                st.markdown(f"""
                    <div class="custom-card">
                        <h3 style='color: #4b2e83;'>💊 Your Recommended Medicine:</h3>
                        <p class="recommendation-text">{recommendation}</p>
                        <p style='color: #666;'>Based on your preferences and medical condition.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")

# Add footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; color: #666; font-size: 14px;'>
        <hr style='border: 0.5px solid #eee;'>
        <p>Drug Recommendation App • Powered by Streamlit</p>
    </div>
""", unsafe_allow_html=True)
