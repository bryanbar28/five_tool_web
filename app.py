import streamlit as st
from openai import OpenAI
from supabase import create_client, Client
import hashlib
from datetime import datetime

# Load secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Disable text selection to protect proprietary content
st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] {
        user-select: none;
    }
    textarea, input {
        user-select: text;
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'reset_mode' not in st.session_state:
    st.session_state.reset_mode = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# Login system
def login():
    st.sidebar.title("Login")

    if st.session_state.reset_mode:
        st.sidebar.subheader("Reset Password")
        reset_email = st.sidebar.text_input("Registered Email", key="reset_email")
        new_password = st.sidebar.text_input("New Password", type="password", key="reset_pw")
        if st.sidebar.button("Confirm Reset"):
            user = supabase.table('users').select('id').eq('email', reset_email).execute().data
            if user:
                supabase.table('users').update({
                    'password_hash': hash_password(new_password)
                }).eq('email', reset_email).execute()
                st.sidebar.success("Password reset successful. Please log in.")
                st.session_state.reset_mode = False
            else:
                st.sidebar.error("Email not found.")
        if st.sidebar.button("Back to Login"):
            st.session_state.reset_mode = False
    else:
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = supabase.table('users').select('id, password_hash').eq('email', email).execute().data
            if user and user[0]['password_hash'] == hash_password(password):
                st.session_state.user_id = user[0]['id']
                st.session_state.logged_in = True
                st.sidebar.success("Logged in!")
            else:
                st.sidebar.error("Invalid email or password")
        if st.sidebar.button("Register"):
            if not email or not password:
                st.sidebar.error("Email and password cannot be empty")
            else:
                existing = supabase.table('users').select('id').eq('email', email).execute().data
                if existing:
                    st.sidebar.error("Email already registered")
                else:
                    supabase.table('users').insert({
                        'email': email,
                        'password_hash': hash_password(password)
                    }).execute()
                    st.sidebar.success("Registered! Please log in.")
        if st.sidebar.button("Reset Password"):
            st.session_state.reset_mode = True

# Strategist modes
SYSTEM_PROMPTS = {
    "diagnostic": "You are a behavioral strategist trained in the 5-Tool Framework...",
    "coaching": "You are a performance coach using the 5-Tool Framework...",
    "hiring": "You are a hiring strategist using the 5-Tool Framework...",
    "mna": "You are a behavioral strategist specializing in Mergers & Acquisitions..."
}

# Main app logic
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("5-Tool Dashboard")
    pages = [
        "🧠 Behavioral Strategist Chat",
        "🔧 5-Tool Analyzer",
        "📂 Repository ($9.99)",
        "🔄 360 Feedback",
        "😓 Behavior Under Pressure",
        "⚖️ Behavioral Calibration",
        "⚠️ Toxicity Grid",
        "📋 Hiring Rubric",
        "👑 Leadership Calibration",
        "✅ Leadership Eligibility",
        "🎯 Risk-Sensitive Roles",
        "🚨 SME Derailment",
        "🧰 Deep-Research Framework",
        "📊 SWOT 2.0 ($3.99)",
        "📚 Book Reader ($5.99)",
        "📰 Articles Uploader ($5.99)"
    ]
    page = st.sidebar.selectbox("Select Feature", pages)

    if page == "🔄 360 Feedback":
        st.title("🔄 360 Degree Feedback (5-Tool Style)")

        # 📊 Scoring Scale Reference
        st.markdown("### 📊 Scoring Scale Reference")
        st.markdown("""
        | **Total Score** | **Interpretation** | **Action** |
        |----------------|--------------------|------------|
        | **21–25** | Leadership-Ready: A reliable “5-tool player” who adapts, owns outcomes, protects systems, delivers consistently, and inspires teams. Minimal behavioral drift; aligns with team standards. | Retain in leadership or promote. Monitor for minor drift (e.g., stress or burnout). Coach any low scores (1–2). |
        | **15–20** | Stretch-Capable: Solid but shows gaps, like inconsistent reliability or weak forecasting. Risking 90-day employee effectiveness. Behavioral drift may indicate personal or team disruption. | Coach on low scores. Address drift triggers. Retest leadership project. Reassess after 3–6 months. |
        | **Below 15** | High-Risk (90-Day Alert): Likely showing behavioral drift (e.g., blaming others, inconsistency, divisiveness). Risks team disruption. | Do not promote. Address drift directly. Consider role change or exit if drift is chronic. |
        """)

        # 📝 Input Section
        st.markdown("### 📝 Feedback Context")
        role_context = st.text_area("📄 Role or Resume Context", height=200)
        notes_context = st.text_area("📝 Additional Notes or Updates", height=150)

        # 🤖 Strategist Chat
        st.markdown("### 🤖 Ask About Other 360 Models")
        chat_query = st.text_input("Ask your strategist about other feedback models...")
        if chat_query:
            chat_prompt = f"""
            You are a behavioral strategist trained in the 5-Tool Framework. A user asked: "{chat_query}"
            Recommend other 360-degree feedback models (e.g., Bracken, Church, Korn Ferry) and explain how they compare to the 5-Tool approach.
            """
            chat_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": chat_prompt}],
                temperature=0.7
            )
            st.markdown("#### 🧠 Strategist Response")
            st.markdown(chat_response.choices[0].message.content)

        # 🚀 Generate Button
        st.markdown("### 🚀 Generate 5-Tool Feedback Profile")
        if st.button("Generate Feedback Profile"):
            if not role_context:
                st.warning("Please enter role or resume context.")
            else:
                full_input = f"{role_context}\n\nAdditional Notes:\n{notes_context}"
                scoring_prompt = f"""
                You are a behavioral strategist using the 5-Tool Framework to assess 360-degree feedback.
                Score the individual from 1–5 on each of the following tools:
                - Speed (Cognitive & Behavioral Agility)
                - Ownership, Initiative & Decisiveness
                - Fielding (Strategic Perception & Sensemaking)
                - Hitting for Average (Reliability, Rigor & Execution)
                - Arm Strength (Reach & Influence)

                Then calculate the total score (out of 25) and interpret it using this scale:
                - 21–25: Leadership-Ready
                - 15–20: Stretch-Capable
                - Below 15: High-Risk (90-Day Alert)

                Include behavioral drift triggers if relevant. Use markdown formatting.
                Input context: {full_input}
                """
                feedback = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": scoring_prompt}],
                    temperature=0.7
                )
                result = feedback.choices[0].message.content
                st.session_state.last_feedback = result
                st.markdown("### 🧠 Feedback Profile")
                st.markdown(result)

        # 🗂️ Last Generated Profile
        if 'last_feedback' in st.session_state:
            st.markdown("---")
            st.markdown("### 🗂️ Last Generated Feedback")
            st.markdown(st.session_state.last_feedback)
