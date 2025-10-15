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
            SYSTEM_PROMPTS = {
    "diagnostic": "You are an AI in HR Consultant trained in the 5-Tool Framework...",
    "coaching": "You are an AI in HR Consultant helping users unlock strengths...",
    "hiring": "You are an AI in HR Consultant assessing candidates...",
    "mna": "You are an AI in HR Consultant specializing in M&A..."
}

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("5-Tool Dashboard")
    pages = [
        "🤖 AI in HR Consultant",
        "🔧 5-Tool Analyzer",
        "🔄 360 Feedback"]
    page = st.sidebar.selectbox("Select Feature", pages)
    if page == "🤖 AI in HR Consultant":
        st.title("🤖 AI in HR Consultant Chat")
        st.caption("Talk to your AI HR consultant. Diagnose, recalibrate, and strategize.")
        mode = st.selectbox("Choose your strategic lens:", list(SYSTEM_PROMPTS.keys()))
        st.session_state["mode"] = mode

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask your consultant anything...")
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
        st.markdown("### 📘 Reference: Introduction into the 5 Tool Employee Framework")
        st.markdown(\"\"\"
        **5 Tool Baseball Player**
        1. Hitting for Average – Consistently making contact and getting on base.
        2. Hitting for Power – Ability to drive the ball for extra bases or home runs.
        3. Speed – Quickness on the bases and in the field.
        4. Fielding – Defensive ability, including range and reaction time.
        5. Arm Strength – Throwing ability, especially for outfielders and infielders.

        **Baseball Tools vs. Professional Skills**
        1. ⚾ Hitting → Technical Competence
        2. 🧤 Fielding → Problem-Solving Ability
        3. ⚡ Speed → Adaptability & Continuous Learning
        4. 💪 Arm Strength → Communication & Leadership
        5. 🚀 Power → Strategic Decision-Making
        \"\"\")

        main_input = st.text_area("📄 Role or Resume Context", height=200)
        notes_input = st.text_area("📝 Additional Notes or Updates", height=150)
        if st.button("🚀 Generate Profile"):
            if not main_input:
                st.warning("Please enter role or resume context.")
            else:
                full_context = f"{main_input}\n\nAdditional Notes:\n{notes_input}"
                prompt = f\"\"\"
                You are an AI in HR Consultant using the 5-Tool Framework. Score the individual from 1–5 on:
                - Speed
                - Ownership
                - Fielding
                - Hitting for Average
                - Arm Strength

                Then interpret the profile using Bryan Barrera’s leadership criteria. Input: {full_context}
                \"\"\"
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
            elif page == "🔄 360 Feedback":
        st.title("🔄 360 Degree Feedback (5-Tool Style)")

        # Section 1: Scale Reference
        st.markdown("### 1️⃣ 360 Scale Reference")
        st.markdown("""
        | **Tool** | **Needs Development (1–2)** | **Effective (3–4)** | **Exceptional (5)** | **Behavioral Drift Triggers** |
        |---------|------------------------------|---------------------|---------------------|-------------------------------|
        | Speed | Reacts impulsively or freezes under pressure | Adjusts quickly to changes with clarity | Seamlessly adapts mid-motion with grace | Tardiness, distraction, disengagement |
        | Power | Hesitates to own outcomes | Takes initiative and makes decisive calls | Owns the mission fully | Blame-shifting, absence |
        | Fielding | Misses risks or becomes rigid | Spots risks early and builds guardrails | Anticipates consequences | Neglecting morale, pushing untested changes |
        | Hitting for Average | Avoids ambiguity or sticks to routine | Delivers consistently under pressure | Anchors team rhythm quietly | Inconsistent delivery, disengagement |
        | Arm Strength | Isolated or lacks influence | Builds trust and influence | Inspires and aligns teams | Withdrawal, lack of collaboration |
        """)

        # Section 2: Scoring Breakdown
        st.markdown("### 2️⃣ Scoring Breakdown Rubric")
        st.markdown("""
        | **Total Score** | **Interpretation** | **Action** |
        |----------------|--------------------|------------|
        | **21–25** | Leadership-Ready: Reliable “5-tool player” | Promote or retain; monitor minor drift |
        | **15–20** | Stretch-Capable: Solid but shows gaps | Coach low scores; reassess in 3–6 months |
        | **Below 15** | High-Risk: Likely showing behavioral drift | Address drift; consider role change or exit |
        """)

        # Section 3: Generate Feedback Profile
        st.markdown("### 3️⃣ Generate Feedback Profile")
        role_context = st.text_area("📄 Role or Resume Context", height=200)
        notes_context = st.text_area("📝 Additional Notes or Updates", height=150)
        if st.button("Generate Feedback Profile"):
            if not role_context:
                st.warning("Please enter role or resume context.")
            else:
                full_input = f"{role_context}\n\nAdditional Notes:\n{notes_context}"
                scoring_prompt = f"""
                You are an AI in HR Consultant using the 5-Tool Framework to assess 360-degree feedback.
                Score the individual from 1–5 on:
                - Speed
                - Power
                - Fielding
                - Hitting for Average
                - Arm Strength

                Then calculate the total score (out of 25) and interpret it using Bryan Barrera's rubric.
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

        # Section 4: AI Chat on Other 360 Models
        st.markdown("### 4️⃣ Ask About Other 360 Models")
        chat_query = st.text_input("Ask your consultant about other feedback models...")
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
            st.markdown("#### 🧠 Consultant Response")
            st.markdown(chat_response.choices[0].message.content)

        # Section 5: Scorecard Generator
        st.markdown("### 5️⃣ Generate Scorecard")
        score_input = st.text_area("Paste the feedback profile here to generate a scorecard")
        if st.button("Generate Scorecard"):
            score_prompt = f"""
            Based on the following feedback profile, generate a scorecard using Bryan Barrera's 5-Tool rubric:
            {score_input}
            """
            score_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": score_prompt}],
                temperature=0.7
            )
            st.markdown("### 📊 Scorecard")
            st.markdown(score_response.choices[0].message.content)
