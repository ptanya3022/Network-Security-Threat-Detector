import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

# Streamlit App Title
st.title("🔒 AI-Powered Network Security Threat Detector")

# File Upload Section
uploaded_file = st.file_uploader("📂 Upload a dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    # Read uploaded CSV file
    df = pd.read_csv(uploaded_file)

    st.write("### 🔍 Uploaded Data Preview:")
    st.write(df.head())

    # Ensure all non-numeric columns are removed
    df_numeric = df.select_dtypes(include=["number"])

    if df_numeric.shape[1] == 0:
        st.error("❌ No numeric columns found in the dataset. Please upload a valid file.")
    else:
        # Train Isolation Forest on the uploaded dataset dynamically
        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(df_numeric)

        # Predict Anomalies
        df["Threat_Detected"] = model.predict(df_numeric)

        # Convert predictions (-1 for anomalies, 1 for normal) with icons
        df["Threat_Detected"] = df["Threat_Detected"].map({1: "✅ Normal", -1: "❌ Suspicious"})

        # Apply styling only if the dataset is small
        if df.shape[0] * df.shape[1] <= 262144:
            def color_code(val):
                color = "green" if "✅" in val else "red"
                return f"background-color: {color}; color: white; font-weight: bold;"

            st.write("### 🚨 Processed Data with Anomaly Detection:")
            st.dataframe(df.style.applymap(color_code, subset=["Threat_Detected"]))
        else:
            st.warning("⚠️ Large dataset detected! Displaying results without styling.")
            st.write(df.head(100))  # Show only first 100 rows to avoid overload

        # Download Processed File
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Processed CSV",
            data=csv,
            file_name="processed_network_traffic.csv",
            mime="text/csv"
        )


   
       
