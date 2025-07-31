import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import time
from io import BytesIO
import html
import fpdf
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="💊 Drug Review App", layout="wide", page_icon="💊")

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 18px !important;
        background-color: #FEECEC;
    }
    .stApp {
        background-image: url("https://raw.githubusercontent.com/lewagon/data-images/master/logo/lewagon-logo-png_seeklogo-586296.png");
        background-repeat: no-repeat;
        background-position: center 80px;
        background-size: 220px;
        opacity: 0.99;
    }
    .stButton>button {
        font-size: 18px !important;
        padding: 0.5em 1em;
    }
    td {
        text-align: left !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💊 Drug Review Satisfaction Prediction App")

uploaded_file = st.file_uploader("📄 Upload your WebMD CSV file", type=["csv"])

if uploaded_file:
    @st.cache_data
    def load_data(file):
        df = pd.read_csv(file)
        df['Age'] = df['Age'].replace({' ': np.nan, '6-Mar': '3-6', '12-Jul': '7-12'})
        df['Age'] = df['Age'].fillna('Unknown')
        df['Sex'] = df['Sex'].replace({' ': np.nan})
        df['Sex'] = df['Sex'].fillna('Unknown')
        df = df[(df['Satisfaction'] >= 1) & (df['Satisfaction'] <= 5)]
        df = df[(df['Effectiveness'] >= 1) & (df['Effectiveness'] <= 5)]
        df = df[(df['EaseofUse'] >= 1) & (df['EaseofUse'] <= 5)]
        return df

    df = load_data(uploaded_file)

    @st.cache_resource
    def train_model(dataframe):
        features = ['Age', 'Condition', 'Sex', 'Effectiveness', 'EaseofUse']
        target = 'Satisfaction'
        X = dataframe[features]
        y = dataframe[target]
        categorical_features = ['Age', 'Condition', 'Sex']
        preprocessor = ColumnTransformer(
            transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
            remainder='passthrough'
        )
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000))
        ])
        model.fit(X, y)
        return model

    with st.spinner('⏳ Training model...'):
        progress_train = st.progress(0)
        time.sleep(0.5)
        progress_train.progress(25)
        time.sleep(0.5)
        progress_train.progress(50)
        time.sleep(0.5)
        progress_train.progress(75)
        model_pipeline = train_model(df)
        time.sleep(0.5)
        progress_train.progress(100)

    def get_age_category(age):
        if age >= 75: return '75 or over'
        elif age >= 65: return '65-74'
        elif age >= 55: return '55-64'
        elif age >= 45: return '45-54'
        elif age >= 35: return '35-44'
        elif age >= 25: return '25-34'
        elif age >= 19: return '19-24'
        elif age >= 13: return '13-18'
        elif age >= 7: return '7-12'
        elif age >= 3: return '3-6'
        elif age >= 0: return '0-2'
        else: return 'Unknown'

    def stars_string(value):
        return "⭐️" * int(round(value)) + "☆" * (5 - int(round(value)))

    def predict_by_gender(model, age_group, condition, effectiveness, ease):
        inputs = []
        for sex in ['Male', 'Female']:
            inputs.append({
                'Age': age_group,
                'Condition': condition,
                'Sex': sex,
                'Effectiveness': effectiveness,
                'EaseofUse': ease
            })
        df_inputs = pd.DataFrame(inputs)
        preds = model.predict(df_inputs)
        scores = {sex: int(score) for sex, score in zip(['Male', 'Female'], preds)}
        scores['Both'] = int(round(np.mean(list(scores.values()))))
        return scores

    st.subheader("🎯 Predict Satisfaction")

    age_mode = st.radio("Age selection", ["Select Group", "Enter Range"])
    if age_mode == "Select Group":
        age_group = st.selectbox("Age", options=[str(x) for x in [1, 6, 10, 13, 18, 25, 30, 40, 50, 60, 70, 80]])
    else:
        age_min = st.number_input("From Age", min_value=0, max_value=120, value=30)
        age_max = st.number_input("To Age", min_value=0, max_value=120, value=39)
        age_mid = (age_min + age_max) // 2
        age_group = get_age_category(age_mid)

    condition = st.selectbox("Condition", sorted(df['Condition'].unique()))
    effectiveness = st.slider("Effectiveness", 1, 5, 3)
    ease = st.slider("Ease of Use", 1, 5, 3)

    if st.button("🔁 Recalculate Prediction"):
        with st.spinner("Calculating prediction..."):
            progress = st.progress(0)
            time.sleep(0.5)
            progress.progress(40)
            results = predict_by_gender(model_pipeline, age_group, condition, effectiveness, ease)
            progress.progress(100)

        for gender, score in results.items():
            st.success(f"{gender}: {score}/5 {stars_string(score)}")

        st.markdown("### 📊 All Condition Ratings")
        condition_stats = df.groupby('Condition').agg(
            avg_satisfaction=('Satisfaction', 'mean'),
            count=('Satisfaction', 'count')
        ).reset_index()
        condition_stats['avg_satisfaction'] = condition_stats['avg_satisfaction'].round(2)
        condition_stats = condition_stats.sort_values('avg_satisfaction', ascending=False)
        st.dataframe(condition_stats.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

        st.markdown("### 📈 Satisfaction Bar Chart")
        chart = alt.Chart(condition_stats.head(10)).mark_bar().encode(
            x='avg_satisfaction:Q',
            y=alt.Y('Condition:N', sort='-x'),
            color=alt.value('#ff4d4d')
        ).properties(width=700, height=400)
        st.altair_chart(chart, use_container_width=True)

        st.markdown("### 📊 Top 5 Conditions per Age Range (All Genders)")
        age_ranges = [(0, 20), (20, 30), (30, 40), (40, 50), (50, 60), (60, 70), (70, 80), (80, 90)]
        age_labels = ["0–20", "20–30", "30–40", "40–50", "50–60", "60–70", "70–80", "80–90"]
        age_chart_df = df.copy()

        # Use midpoint mapping to Age label
        def map_custom_range(age_text):
            for (low, high), label in zip(age_ranges, age_labels):
                try:
                    mid = int(age_text.split('-')[0])
                    if low <= mid < high:
                        return label
                except:
                    return "Unknown"
            return "Unknown"

        age_chart_df['age_group_range'] = age_chart_df['Age'].apply(map_custom_range)

        for label in age_labels:
            st.markdown(f"#### 🔹 Age Range: {label}")
            segment = age_chart_df[age_chart_df['age_group_range'] == label]
            segment_stats = segment.groupby('Condition').agg(
                avg_satisfaction=('Satisfaction', 'mean'),
                count=('Satisfaction', 'count')
            ).reset_index()
            segment_stats = segment_stats[segment_stats['count'] >= 10].sort_values('avg_satisfaction', ascending=False).head(5)
            if not segment_stats.empty:
                chart = alt.Chart(segment_stats).mark_bar().encode(
                    x=alt.X('avg_satisfaction:Q', title='Average Satisfaction'),
                    y=alt.Y('Condition:N', sort='-x', title='Condition'),
                    color=alt.value('#ff4d4d')
                ).properties(width=700, height=300)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Not enough data in this age range.")


    # 📄 PDF Export Section
    def stars_string(value):
        return "⭐️" * int(round(value)) + "☆" * (5 - int(round(value)))


    def generate_pdf_from_df(dataframe):

        buffer = BytesIO()
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Drug Review Satisfaction Dashboard", ln=1, align='C')
        pdf.ln(10)
        for _, row in dataframe.iterrows():
            stars = stars_string(row['avg_satisfaction'])
            try:
                line = f"{row['Condition']:<30} | Score: {row['avg_satisfaction']} / 5 | {stars} | Count: {row['count']}"
                pdf.multi_cell(0, 10, txt=line.encode('latin-1', 'replace').decode('latin-1'))
            except:
                pdf.multi_cell(0, 10, txt="Encoding error in row")
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

        buffer.seek(0)
        return buffer

    # Prepare and show download button
    if 'condition_stats' in locals():
        pdf_data = generate_pdf_from_df(condition_stats)
        st.download_button(
            label="📥 Export Dashboard (Full) as PDF",
            data=pdf_data,
            file_name="dashboard_full_export.pdf",
            mime="application/pdf"
        )
