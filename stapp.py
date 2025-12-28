import streamlit as st
from inference.predictor import predict
from src.website_feature_extraction import FeatureExtractor

# ======================
# APP CONFIG
# ======================
st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="centered",
)

# ======================
# INIT
# ======================
extractor = FeatureExtractor()

# ======================
# UI
# ======================
st.title("🛡️ PhishGuard AI")
st.subheader("Phishing Website Detection")

st.markdown(
    """
Enter a website URL to analyze whether it is **SAFE**, **SUSPICIOUS**, or **PHISHING**
using machine learning models.
"""
)

# ======================
# FORM
# ======================
with st.form("phishing_form"):
    url = st.text_input("🔗 Website URL", placeholder="https://example.com")
    model_type = st.selectbox(
        "🤖 Select ML Model",
        options=["xgboost", "ann"],
        index=0,
    )

    submitted = st.form_submit_button("🔍 Scan Website")

# ======================
# PROCESS
# ======================
if submitted:
    if not url.strip():
        st.warning("⚠️ Please enter a valid URL")
    else:
        try:
            with st.spinner("Extracting features and analyzing URL..."):
                # Feature extraction
                features = extractor.extract(url)

                # Prediction
                result = predict(features, model_type=model_type)

            # ======================
            # RESULT DISPLAY
            # ======================
            st.success("✅ Scan completed")

            st.markdown("### 🧠 Model Result")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Prediction",
                    value="PHISHING 🚨" if result["prediction"] == 0 else "SAFE ✅",
                )

            with col2:
                if result.get("phishing_probability") is not None:
                    st.metric(
                        label="Phishing Probability",
                        value=f"{result['phishing_probability'] * 100:.2f} %",
                    )

            st.markdown("### 📊 Details")
            st.json(result)

        except Exception as e:
            st.error("❌ Error occurred during analysis")
            st.code(str(e), language="text")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("© PhishGuard AI | Cybersecurity Detection System")
