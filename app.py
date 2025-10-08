# app.py

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
}# Main app logic
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
                st.markdown(assistant_reply)

    elif page == "🔧 5-Tool Analyzer":
        st.title("🔧 5-Tool Employee Framework Analyzer")
        main_input = st.text_area("📄 Role or Resume Context", height=200)
        notes_input = st.text_area("📝 Additional Notes or Updates", height=150)
        if st.button("🚀 Generate Profile"):
            if not main_input:
                st.warning("Please enter role or resume context.")
            else:
                full_context = f"{main_input}\n\nAdditional Notes:\n{notes_input}"
                prompt = f"""
                You are a behavioral strategist advising a founder in the injection molding and medical device space.
                They are recruiting a board member with 3% equity who will:
                - Help secure ISO 13485 and FDA QSR certification
                - Mentor the internal team on regulatory and operational excellence
                - Act as a strategic consultant, not just a passive advisor
                - Engage with professional communities like:
                  - Society of Manufacturing Engineers (SME)
                  - MedAccred (medical OEM quality consortium)
                  - MedDevice, DeviceTalks, and similar forums
                Using the 5-Tool Employee Framework:
                - Hitting for Average: Technical competence, consistency
                - Power: Strategic impact, decision-making
                - Speed: Adaptability, quick learning
                - Arm Strength: Teamwork, collaboration
                - Fielding: Stress resilience, reliability
                Analyze the ideal board member profile for this role. Score each tool 1–10. Include behavioral traits, strategic value, and drift risks. Use markdown formatting.
                Input context: {full_context}
                """
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
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
            for row in data:
                st.write(f"{row['department']} - {row['position']} ({row['data_type']}): {row['content']} [{row['timestamp']}]")
        else:
            st.warning("Pay $9.99 to unlock full repository.")

    elif page == "🔄 360 Feedback":
        st.title("🔄 360 Degree Feedback")
        st.markdown("""
        | Tool | Needs Development (1-2) | Effective (3-4) | Exceptional (5) | Behavioral Drift Triggers |
        |------|-------------------------|-----------------|-----------------|--------------------------|
        | Speed | Reacts impulsively or freezes | Adjusts quickly | Seamlessly adapts | Sudden tardiness |
        | Power | Hesitates to own outcomes | Takes initiative | Owns mission fully | Blame-shifting |
        | Fielding | Misses risks, blames others | Spots risks early | Anticipates consequences | Neglecting morale |
        | Hitting for Avg. | Avoids ambiguity | Delivers consistently | Anchors team rhythm | Inconsistent delivery |
        | Arm Strength | Charms without substance | Communicates clearly | Inspires across hierarchies | Divisive communication |
        """)
        notes = st.text_area("Enter feedback notes")
        if st.button("Analyze"):
            prompt = f"Score 360 feedback based on grid for: {notes}"
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown("### 🧠 Feedback Analysis")
            st.markdown(completion.choices[0].message.content)

    # Add remaining modules below this line as needed
