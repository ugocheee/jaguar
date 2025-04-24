
import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="Jaguar: Burnout Dashboard", layout="centered")
st.title("🧠 Jaguar: Predictive Burnout Assistant")

# --- TABS ---
tab1, tab2 = st.tabs(["📋 Employee Lookup", "🛠️ What-If Simulation"])

# --- TAB 1: EMPLOYEE LOOKUP ---
with tab1:
    st.subheader("Lookup Burn Rate by Employee ID")

    @st.cache_data
    def load_data():
        url = "https://raw.githubusercontent.com/ugocheee/burnoutpredictor2/main/predicted_burn_rate.csv"
        return pd.read_csv(url)

    data = load_data()
    employee_id = st.selectbox("Select Employee ID:", sorted(data['Employee_ID'].unique()))
    predicted_rate = data.loc[data['Employee_ID'] == employee_id, 'Predicted_Burn_Rate'].values[0]
    st.metric(label=f"Predicted Burn Rate for {employee_id}", value=f"{predicted_rate:.2f}")
    
    if predicted_rate <= 0.45:
        st.success("✅ You should be good. No signs of burnout.")
    elif 0.45 < predicted_rate <= 0.65:
        st.warning("⚠️ Watch out. This employee may be at risk.")
    else:
        st.error("🚨 Take action today. This employee is likely burned out.")

    st.markdown("""---
##### Jaguar by Ugochi""")

    st.markdown("### 📊 Burn Rate Distribution")
    st.bar_chart(data.set_index('Employee_ID')['Predicted_Burn_Rate'])

# --- TAB 2: WHAT-IF SIMULATION ---
with tab2:
    st.subheader("Simulate Scenarios Based on Team Member Info")

    fatigue = st.slider("Mental Fatigue Score", 0.0, 10.0, 5.0)
    resources = st.slider("Resource Allocation", 1, 10, 5)
    designation = st.selectbox("Designation Level", [0, 1, 2, 3, 4, 5])
    wfh = st.selectbox("WFH Setup Available", ["Yes", "No"])
    company_type = st.selectbox("Company Type", ["Product", "Service"])
    gender = st.selectbox("Gender", ["Male", "Female"])
    years = st.slider("Years in Current Company", 0.0, 20.0, 5.0)

    # Linear model formula with 0–1 scale output
    burn_rate = (
        -0.1031
        + 0.0068 * (1 if gender == "Male" else 0)
        + 0.00003 * (1 if company_type == "Service" else 0)
        - 0.0171 * (1 if wfh == "Yes" else 0)
        + 0.00896 * designation
        + 0.0309 * resources
        + 0.0672 * fatigue
        + 0.00108 * years
    )

    burn_score = round(burn_rate, 2)
    st.markdown(f"### 🔥 Predicted Burn Rate: `{burn_score}`")

    if burn_score <= 0.45:
        st.success("✅ You should be good. No signs of burnout.")
    elif 0.45 < burn_score <= 0.65:
        st.warning("⚠️ Watch out. This employee may be at risk.")
    else:
        st.error("🚨 Take action today. This employee is likely burned out.")

    st.markdown("""---
##### Jaguar by Ugochi""")
