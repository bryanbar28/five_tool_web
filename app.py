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
                You are a behavioral strategist advising a founder in the injection molding and medical device space...
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

        st.markdown("---")
        st.markdown("### 📘 5-Tool Framework Reference")
        st.markdown("""
        **Introduction into the 5 Tool Employee Framework**  
        *An Interchangeable Model*

        #### ⚾ 5 Tool Baseball Player
        1. **Hitting for Average** – Consistently making contact and getting on base  
        2. **Hitting for Power** – Ability to drive the ball for extra bases or home runs  
        3. **Speed** – Quickness on the bases and in the field  
        4. **Fielding** – Defensive ability, including range and reaction time  
        5. **Arm Strength** – Throwing ability, especially for outfielders and infielders  

        #### 🧠 Baseball Tools vs. Professional Skills
        1. ⚾ **Hitting → Technical Competence**  
        2. 🧤 **Fielding → Problem-Solving Ability**  
        3. ⚡ **Speed → Adaptability & Continuous Learning**  
        4. 💪 **Arm Strength → Communication & Leadership**  
        5. 🚀 **Power → Strategic Decision-Making**
        """)

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
            
