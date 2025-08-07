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
st.set_page_config(page_title="Drug Recommendation App", layout="centered")
st.title(":pill: Drug Recommendation App")

# -- Helper Function
def load_css_from_url(url: str ):
    """Fetches and injects CSS from a URL into the Streamlit app."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        st.markdown(f"<style>{response.text}</style>", unsafe_allow_html=True)
    except requests.exceptions.RequestException as e:
        st.warning(f"Failed to load CSS from {url}. Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while loading CSS: {e}")

# -- Page Setup
st.set_page_config(page_title="Drug Recommendation App", layout="centered")
load_css_from_url(CSS_URL) # Load custom CSS
st.title(":pill: Drug Recommendation App")

# Function to reset form fields
def reset_form():
    st.session_state["age"] = 0
    st.session_state["gender"] = "male"
    st.session_state["condition"] = "Pain"
    st.session_state["effectiveness"] = 3
    st.session_state["ease_of_use"] = 3
    st.session_state["satisfaction"] = 3

# -- Navigation UI
view_choice = st.radio("Choose what you want to do:", ["View Presentation", "Use the App"])

# -------------------------
# :film_frames: View Presentation
# -------------------------
if view_choice == "View Presentation":
    st.markdown("### :film_projector: Project Presentation")
    components.html(PRESENTATION_IFRAME, height=550)
    st.markdown(f"[⬇️ Download PDF]({PRESENTATION_DOWNLOAD})")

# -------------------------
# :pill: Use the App
# -------------------------
elif view_choice == "Use the App":
    st.markdown("### :pill: Get Your Personalized Medicine Recommendation")

    with st.form("medicine_form"):
        age = st.number_input("Age", min_value=0, max_value=120, step=1, key="age")
        gender = st.selectbox("Gender", ["male", "female"], key="gender")
        condition = st.selectbox("Medical condition", conditions_list, key="condition")
        effectiveness = st.slider("Desired effectiveness", 1, 5, 3, key="effectiveness")
        ease_of_use = st.slider("Ease of use", 1, 5, 3, key="ease_of_use")
        satisfaction = st.slider("Expected satisfaction", 1, 5, 3, key="satisfaction")
        submitted = st.form_submit_button("Get Recommendation")

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
            response = requests.post(BACKEND_URL, json=data)
            if response.status_code == 200:
                recommendation = response.json().get("medicine", "No recommendation found.")
                st.success(f":pill: Your recommended medicine: **{recommendation}**")
            else:
                st.error(f":x: Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f":warning: Request failed: {e}")
