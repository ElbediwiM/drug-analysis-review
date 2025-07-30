import streamlit as st
import requests

# Replace with your actual deployed FastAPI endpoint URL
BACKEND_URL = "https://mvp-backend-581249984477.europe-west1.run.app"

st.title("Medicine Recommender")

# User input form
with st.form("medicine_form"):
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["male", "female", "other"])
    condition = st.text_input("Medical condition")
    effectiveness = st.slider("How effective do you want the medicine to be?", 1, 5, 3)
    ease_of_use = st.slider("How easy should it be to use?", 1, 5, 3)

    submitted = st.form_submit_button("Get Recommendation")

# Handle submission
if submitted:
    data = {
        "age": age,
        "gender": gender,
        "condition": condition,
        "effectiveness": effectiveness,
        "ease_of_use": ease_of_use
    }

    try:
        response = requests.post(BACKEND_URL, json=data)

        if response.status_code == 200:
            # Parse JSON response
            recommendation = response.json().get("medicine", "No recommendation found.")
            st.success(f"💊 Recommended medicine: **{recommendation}**")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
