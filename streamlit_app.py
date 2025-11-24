import streamlit as st
from hybrid_predict import hybrid_predict, offline_ai_predict

st.set_page_config(page_title="Hybrid Fake News Detector", layout="centered")

st.title("Hybrid Fake News Detector (AI + Online Verification)")
st.write("Enter any news text and choose how you want to verify it.")

text = st.text_area("Enter your news text:", height=150)

# Utility function for colored verdict boxes
def verdict_box(label, reason):
    if label == "TRUE" or label == "REAL":
        st.success(f"Final Verdict: {label}\n\n{reason}")
    elif label == "FAKE":
        st.error(f"Final Verdict: {label}\n\n{reason}")
    else:
        st.warning(f"Final Verdict: {label}\n\n{reason}")


# -------------------------
# AI ONLY PREDICTION
# -------------------------
if st.button("AI Only Prediction"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        label, prob = offline_ai_predict(text)
        st.subheader("AI Prediction:")
        st.write(f"Prediction: **{label}**")
        st.write(f"Confidence: **{prob:.4f}**")


# -------------------------
# HYBRID ONLINE + AI PREDICTION
# -------------------------
if st.button("Hybrid (AI + Online Fact Check)"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        st.subheader("Processing...")
        result = hybrid_predict(text)

        # AI Part
        st.subheader("Offline AI Result:")
        st.write(f"Prediction: **{result['ai_label']}**")
        st.write(f"Confidence: **{result['ai_confidence']:.4f}**")

        # Online Sources
        st.subheader("Wikipedia Summary:")
        wiki = result["online_verification"]["wikipedia"]
        st.write(wiki if wiki else "No information found.")

        st.subheader("GNews Headlines:")
        gnews = result["online_verification"]["gnews"]
        st.write(gnews if gnews else "No related news found.")

        st.subheader("Google Fact Check Results:")
        fact = result["online_verification"]["google_factcheck"]
        if fact:
            st.json(fact)
        else:
            st.write("No fact check info found.")

        # Final Verdict
        from online_verify import final_verdict
        label, reason = final_verdict(
            text,
            {"label": result['ai_label'], "confidence": result['ai_confidence']},
            wiki,
            gnews,
            fact
        )

        st.subheader("Final Result:")
        verdict_box(label, reason)
