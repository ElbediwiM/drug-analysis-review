import streamlit as st
import requests

BACKEND_URL = "https://mvp1-581249984477.europe-west1.run.app/predict"

conditions_list = ['Other',
 'Pain',
 'High Blood Pressure',
 'Depression',
 'Birth Control',
 'Neuropathic Pain',
 'Chronic Trouble Sleeping',
 'Type 2 Diabetes Mellitus',
 'Attention Deficit Disorder with Hyperactivity',
 'Bipolar Depression',
 'Migraine Prevention',
 'Panic Disorder',
 'Major Depressive Disorder',
 'Overweight',
 'Repeated Episodes of Anxiety',
 'Rheumatoid Arthritis',
 'High Cholesterol',
 'Disorder characterized by Stiff, Tender & Painful Muscles',
 'Migraine Headache',
 'Underactive Thyroid',
 'Chronic Pain',
 'Anxious',
 'Acne',
 'Cough',
 '"Change of Life" Signs',
 'Asthma',
 'Joint Damage causing Pain and Loss of Function',
 'Pain Originating From a Nerve',
 'Condition in which Stomach Acid is Pushed Into the Esophagus',
 'Stop Smoking',
 'Muscle Spasm',
 'Emptying of the Bowel',
 'Osteoporosis',
 'Decreased Bone Mass Following Menopause',
 'Combined High Blood Cholesterol and Triglyceride Level',
 'Chronic Pain with Narcotic Drug Tolerance',
 'Bacterial Urinary Tract Infection',
 'Abnormally Long or Heavy Periods',
 'Enlarged Prostate',
 'Inflammation of the Nose due to an Allergy',
 'Disease of Ovaries with Cysts',
 'Osteoarthritis of the Knee',
 'Epileptic Seizure',
 'Painful Periods',
 'Extreme Discomfort in Calves when Sitting or Lying Down',
 'Inability to have an Erection',
 'Bipolar I Disorder with Most Recent Episode Mixed',
 'Yeast Infection of Vagina and Vulva',
 'Manic-Depression',
 'Acute Bacterial Infection of the Sinuses']

st.title("💊 Medicine Recommender")

with st.form("medicine_form"):
    age = st.number_input("Age", min_value=0, max_value=120, step=1, key="age")
    gender = st.selectbox("Gender", ["male", "female"], key="gender")
    condition = st.selectbox("Medical condition", conditions_list, key="condition")
    effectiveness = st.slider("How effective should the medicine be?", 1, 5, 3, key="effectiveness")
    ease_of_use = st.slider("How easy should it be for the patient to use the medicine?", 1, 5, 3, key="ease_of_use")
    satisfaction = st.slider("How satisfied with the medicine can the patient be?", 1, 5, 3, key="satisfaction")

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
            st.success(f"💊 Your recommended medicine: **{recommendation}**")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
