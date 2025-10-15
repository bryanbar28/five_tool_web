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
    "diagnostic": "You are a behavioral strategist trained in the 5-Tool Framework. You diagnose performance drift, recalibrate strengths under pressure, and guide users through leadership, hiring, and cultural alignment. You speak plainly, challenge assumptions, and offer actionable insights tailored to high-stakes roles.",
    "coaching": "You are a performance coach using the 5-Tool Framework. You help users unlock strengths, overcome drift, and build leadership capacity under pressure. You ask sharp questions and offer strategic nudges.",
    "hiring": "You are a hiring strategist using the 5-Tool Framework. You assess candidates for resilience, adaptability, and strategic alignment. You help users craft interview questions and decode behavioral signals.",
    "mna": "You are a behavioral strategist specializing in Mergers & Acquisitions. You use the 5-Tool Framework to compare branches, decode team dynamics, and identify high-performing sites. You analyze resumes, reviews, and demographic patterns to uncover behavioral truths—like how top performers often come from nontraditional backgrounds, working multiple jobs while pursuing online education. You help executives replicate success across failing sites by surfacing what works, where, and why."
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

    if page == "🧠 Behavioral Strategist Chat":
        st.title("🧠 5-Tool Behavioral Intelligence Chat")
        st.caption("Talk to your behavioral strategist. Diagnose, recalibrate, and strategize.")
        mode = st.selectbox("Choose your strategic lens:", list(SYSTEM_PROMPTS.keys()))
        st.session_state["mode"] = mode

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask your strategist anything...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            messages = [{"role": "system", "content": SYSTEM_PROMPTS[mode]}] + st.session_state.messages
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )
            assistant_reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            with st.chat_message("assistant"):
                st.markdown(assistant_reply)    elif page == "🔧 5-Tool Analyzer":
        st.title("🔧 5-Tool Employee Framework Analyzer")
        main_input = st.text_area("📄 Role or Resume Context", height=200)
        notes_input = st.text_area("📝 Additional Notes or Updates", height=150)
        if st.button("🚀 Generate Profile"):
            if not main_input:
                st.warning("Please enter role or resume context.")
            else:
                full_context = f"{main_input}\n\nAdditional Notes:\n{notes_input}"
                prompt = f"""
                You are a behavioral strategist using the 5-Tool Framework. Score the individual from 1–5 on:
                - Speed
                - Ownership
                - Fielding
                - Hitting for Average
                - Arm Strength

                Then interpret the profile using Bryan Barrera’s leadership criteria. Input: {full_context}
                """
                completion = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = completion.choices[0].message.content
                st.session_state.last_analysis = result
                st.markdown("### 🧠 Ideal 5-Tool Profile")
                st.markdown(result)
        if 'last_analysis' in st.session_state:
            st.markdown("---")
            st.markdown("### 🗂️ Last Generated Profile")
            st.markdown(st.session_state.last_analysis)

    elif page == "📂 Repository ($9.99)":
        st.title("📂 Repository")
        if st.text_input("Enter access code ($9.99)", type="password") == "PAID999":
            dept = st.text_input("Department")
            pos = st.text_input("Position")
            data_type = st.selectbox("Data Type", ["Job Desc", "Resume", "Review", "Interview", "Notes"])
            content = st.text_area("Content")
            if st.button("Save"):
                supabase.table('repo').insert({
                    'user_id': st.session_state.user_id,
                    'department': dept,
                    'position': pos,
                    'data_type': data_type,
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                }).execute()
                st.success("Saved!")
            data = supabase.table('repo').select('*').eq('user_id', st.session_state.user_id).execute().data
            for item in data:
                st.markdown(f"**{item['department']} – {item['position']} ({item['data_type']})**")
                st.markdown(item['content'])
                st.markdown("---")

    elif page == "🔄 360 Feedback":
        st.title("🔄 360 Degree Feedback (5-Tool Style)")

        # Section 1: Scoring Scale Reference
        st.markdown("### 1️⃣ Scoring Scale Reference")
        st.markdown("""
        | **Total Score** | **Interpretation** | **Action** |
        |----------------|--------------------|------------|
        | **21–25** | Leadership-Ready: A reliable “5-tool player” who adapts, owns outcomes, protects systems, delivers consistently, and inspires teams. Minimal behavioral drift; aligns with team standards. | Retain in leadership or promote. Monitor for minor drift (e.g., stress or burnout). Coach any low scores (1–2). |
        | **15–20** | Stretch-Capable: Solid but shows gaps, like inconsistent reliability or weak forecasting. Risking 90-day employee effectiveness. Behavioral drift may indicate personal or team disruption. | Coach on low scores. Address drift triggers. Retest leadership project. Reassess after 3–6 months. |
        | **Below 15** | High-Risk (90-Day Alert): Likely showing behavioral drift (e.g., blaming others, inconsistency, divisiveness). Risks team disruption. | Do not promote. Address drift directly. Consider role change or exit if drift is chronic. |
        """)

        # Section 2: Scoring Breakdown
        st.markdown("### 2️⃣ Scoring Breakdown Rubric")
        st.markdown("""
        | **Tool** | **Definition** | **Scoring Guidance** |
        |---------|----------------|-----------------------|
        | Speed | Cognitive & Behavioral Agility | 1 = Rigid, 5 = Adaptive |
        | Ownership | Initiative & Decisiveness | 1 = Passive, 5 = Proactive |
        | Fielding | Strategic Perception & Sensemaking | 1 = Reactive, 5 = Anticipatory |
        | Hitting for Average | Reliability, Rigor & Execution | 1 = Inconsistent, 5 = Dependable |
        | Arm Strength | Reach & Influence | 1 = Isolated, 5 = Impactful |
        """)

        # Section 3: Ask About Other Models
        st.markdown("### 3️⃣ Ask About Other 360 Models")
        chat_query = st.text_input("Ask your strategist about other feedback models...")
        if chat_query:
            chat_prompt = f"""
            A user asked: "{chat_query}"
            Recommend other 360-degree feedback models (e.g., Bracken, Church, Korn Ferry) and explain how they compare to the 5-Tool approach.
            """
            chat_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": chat_prompt}],
                temperature=0.7
            )
            st.markdown("#### 🧠 Strategist Response")
            st.markdown(chat_response.choices[0].message.content)

        # Generate Button
        st.markdown("### 🚀 Generate Feedback Profile")
        role_context = st.text_area("📄 Role or Resume Context", height=200)
        notes_context = st.text_area("📝 Additional Notes or Updates", height=150)
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

        if 'last_feedback' in st.session_state:
            st.markdown("---")
            st.markdown("### 🗂️ Last Generated Feedback")
            st.markdown(st.session_state.last_feedback)

    # Scaffold remaining pages
    elif page in [
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
    ]:
        st.title(page)
        st.info("This module is coming soon. Stay tuned.")
