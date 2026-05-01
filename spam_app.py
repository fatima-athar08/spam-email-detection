import streamlit as st
import pickle
import re
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('spam_vectorizer.pkl', 'rb'))

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    words = text.split()
    words = [stemmer.stem(w) for w in words if w not in stop_words and len(w) > 2]
    return ' '.join(words)


st.set_page_config(page_title="Spam Email Detector", page_icon="📧", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* ── Hide all Streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stTop"],
.stAppHeader, .css-1dp5vir, .css-18ni7ap {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    visibility: hidden !important;
}

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    margin: 0; padding: 0;
}

/* ── Full page gradient ── */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* ── Center content, no weird gaps ── */
.block-container {
    max-width: 660px !important;
    padding: 3rem 1.5rem 4rem !important;
    margin-top: 0 !important;
}

/* ════════════════════════════
   STYLE THE STREAMLIT ELEMENTS
   DIRECTLY — no wrapper divs
   ════════════════════════════ */

/* Page title via st.markdown */
h1 {
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.02em !important;
    margin: 0 0 0.4rem !important;
    line-height: 1.15 !important;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}

/* Subtitle */
h1 + p, .subtitle {
    font-size: 1rem !important;
    color: rgba(255,255,255,0.75) !important;
    font-weight: 400 !important;
    margin: 0 0 2rem !important;
}

/* ── Stats chips row ── */
.stats-row {
    display: flex;
    gap: 12px;
    margin-bottom: 2rem;
}
.stat-chip {
    flex: 1;
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(10px);
    border-radius: 14px;
    padding: 16px 10px;
    text-align: center;
    border: 1.5px solid rgba(255,255,255,0.28);
}
.stat-num {
    display: block;
    font-size: 1.1rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    line-height: 1.2;
}
.stat-lbl {
    display: block;
    font-size: 0.64rem;
    color: rgba(255,255,255,0.65);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Input section card ── */
.input-card {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 1.1rem 1.6rem;
    border: 1.5px solid rgba(255,255,255,0.3);
    margin-bottom: 14px;
}
.input-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: 0.01em;
}

/* ── Textarea ── */
textarea {
    background: #f6f5ff !important;
    border: 2px solid #e4e0f8 !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 400 !important;
    line-height: 1.7 !important;
    padding: 0.9rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
textarea:focus {
    border-color: #667eea !important;
    background: #fff !important;
    box-shadow: 0 0 0 4px rgba(102,126,234,0.12) !important;
    outline: none !important;
}
textarea::placeholder {
    color: #c0bdd8 !important;
    font-style: italic !important;
}
/* Hide the label Streamlit renders */
.stTextArea > label { display: none !important; }

/* ── Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.5rem !important;
    margin-top: 0.8rem !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    box-shadow: 0 6px 22px rgba(102,126,234,0.4) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(102,126,234,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Result cards ── */
.result-box {
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    margin-top: 1.2rem;
}
.result-box.spam {
    background: linear-gradient(135deg, #fff2f2, #ffe4e4);
    border-left: 6px solid #ef4444;
}
.result-box.ham {
    background: linear-gradient(135deg, #f0fff6, #dcfce7);
    border-left: 6px solid #22c55e;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
}
.result-icon { font-size: 1.8rem; line-height: 1; }
.result-title {
    font-size: 1.3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.01em;
}
.result-box.spam .result-title { color: #dc2626; }
.result-box.ham  .result-title { color: #16a34a; }
.result-subtitle {
    font-size: 0.84rem;
    font-weight: 500;
    color: #aaa;
    margin: 0 0 14px;
}
.conf-track {
    background: rgba(0,0,0,0.08);
    border-radius: 100px;
    height: 9px;
    overflow: hidden;
    margin-bottom: 7px;
}
.conf-fill { height: 100%; border-radius: 100px; }
.result-box.spam .conf-fill { background: linear-gradient(90deg, #fca5a5, #ef4444); }
.result-box.ham  .conf-fill { background: linear-gradient(90deg, #86efac, #22c55e); }
.conf-label { font-size: 0.82rem; font-weight: 600; }
.result-box.spam .conf-label { color: #ef4444; }
.result-box.ham  .conf-label { color: #22c55e; }

/* ── Footer ── */
.app-footer {
    text-align: center;
    margin-top: 1.8rem;
    font-size: 0.74rem;
    color: rgba(255,255,255,0.38);
    font-weight: 500;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ── Title (on gradient, above the card) ──
st.markdown("# 📧 Spam Email Detector")
st.markdown('<p class="subtitle">Paste any email or SMS — the model instantly tells you if it\'s spam.</p>', unsafe_allow_html=True)

# ── Stats row (on gradient, glassmorphism chips) ──
st.markdown("""
<div class="stats-row">
    <div class="stat-chip">
        <span class="stat-num">98.6%</span>
        <span class="stat-lbl">Accuracy</span>
    </div>
    <div class="stat-chip">
        <span class="stat-num">5,572</span>
        <span class="stat-lbl">Messages</span>
    </div>
    <div class="stat-chip">
        <span class="stat-num">Naïve Bayes</span>
        <span class="stat-lbl">Model</span>
    </div>
    <div class="stat-chip">
        <span class="stat-num">TF-IDF</span>
        <span class="stat-lbl">Vectorizer</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input card header ──
st.markdown("""
<div class="input-card">
    <p class="input-card-title">✉️ &nbsp;Enter your message below</p>
</div>
""", unsafe_allow_html=True)

# ── Textarea + button (Streamlit native, styled via CSS) ──
input_email = st.text_area(
    label="message",
    height=185,
    placeholder="e.g. Congratulations! You've won a FREE iPhone. Click here to claim your prize now...",
    label_visibility="collapsed"
)

check_clicked = st.button("🔍  Detect Spam")

# ── Result ──
if check_clicked:
    if input_email.strip() == "":
        st.warning("Please paste a message to analyze.")
    else:
        cleaned = clean_text(input_email)
        if cleaned.strip() == "":
            st.warning("Message is too short or has no recognizable words.")
        else:
            vector      = vectorizer.transform([cleaned])
            prediction  = model.predict(vector)[0]
            probability = model.predict_proba(vector)[0]

            if prediction == 1:
                confidence = round(probability[1] * 100, 1)
                st.markdown(f"""
<div class="result-box spam">
    <div class="result-header">
        <span class="result-icon">🚨</span>
        <p class="result-title">SPAM Detected</p>
    </div>
    <p class="result-subtitle">This message contains spam signals. Be careful!</p>
    <div class="conf-track">
        <div class="conf-fill" style="width:{confidence}%"></div>
    </div>
    <span class="conf-label">Confidence: {confidence}%</span>
</div>
""", unsafe_allow_html=True)
            else:
                confidence = round(probability[0] * 100, 1)
                st.markdown(f"""
<div class="result-box ham">
    <div class="result-header">
        <span class="result-icon">✅</span>
        <p class="result-title">Not Spam</p>
    </div>
    <p class="result-subtitle">This message looks safe and legitimate.</p>
    <div class="conf-track">
        <div class="conf-fill" style="width:{confidence}%"></div>
    </div>
    <span class="conf-label">Confidence: {confidence}%</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="app-footer">Built with Python · Scikit-learn · Streamlit</p>', unsafe_allow_html=True)

