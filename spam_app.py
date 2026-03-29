import streamlit as st
import pickle
import re
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# =========================
# Load model + vectorizer
# =========================
model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('spam_vectorizer.pkl', 'rb'))

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))


# =========================
# Preprocessing — same as notebook
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words and len(w) > 2]
    return ' '.join(words)


# =========================
# UI
# =========================
st.set_page_config(page_title="Email Spam Detector", page_icon="📧")

st.title("📧 Email Spam Detector")
st.write("Paste an email or message below to check if it is spam or not.")

input_email = st.text_area("Enter email / message:", height=200,
                            placeholder="e.g. Congratulations! You've won a free iPhone. Click here to claim...")

# =========================
# Prediction
# =========================
if st.button("Check for Spam"):

    if input_email.strip() == "":
        st.warning("Please enter some text first.")
    else:
        cleaned = clean_text(input_email)

        if cleaned.strip() == "":
            st.warning("Text is too short or has no meaningful words after cleaning.")
        else:
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)[0]
            probability = model.predict_proba(vector)[0]

            st.divider()

            if prediction == 1:
                confidence = round(probability[1] * 100, 2)
                st.error(f"🚨 SPAM detected! (Confidence: {confidence}%)")
                st.progress(confidence / 100)
            else:
                confidence = round(probability[0] * 100, 2)
                st.success(f"✅ Looks safe — Not spam (Confidence: {confidence}%)")
                st.progress(confidence / 100)
