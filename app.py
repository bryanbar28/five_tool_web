import streamlit as st
from openai import OpenAI
from supabase import create_client
import hashlib
from datetime import datetime

# Load secrets from Streamlit Cloud
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Check keys
if not all([OPENAI_API_KEY, SUPABASE_URL, SUPABASE_KEY]):
    st.error("Missing API keys! Check Streamlit secrets.")
    st.stop()

try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Failed to initialize connections: {str(e)}")
    st.stop()

# Hash password
def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Login/Registration
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        try:
            user = supabase.table('users').select('id, password_hash').eq('username', username).execute().data
            if user and user[0]['password_hash'] == hash_password(password):
                st.session_state.user_id = user[0]['id']
                st.session_state.logged_in = True
                st.sidebar.success("Logged in!")
            else:
                st.sidebar.error("Invalid username or password")
        except Exception as e:
            st.sidebar.error(f"Login error: {str(e)}. Ensure 'users' table exists with columns: id, username, password_hash.")
    if st.sidebar.button("Register"):
        try:
            if not username or not password:
                st.sidebar.error("Username and password cannot be empty")
            else:
                existing = supabase.table('users').select('id').eq('username', username).execute().data
                if existing:
                    st.sidebar.error("Username already taken")
                else:
                    supabase.table('users').insert({
                        'username': username,
                        'password_hash': hash_password(password)
                    }).execute()
                    st.sidebar.success("Registered! Please log in.")
        except Exception as e:
            st.sidebar.error(f"Registration error: {str(e)}. Ensure 'users' table has columns: id (int8, primary key, identity), username (text, unique), password_hash (text).")

# Main app
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("5-Tool Dashboard")
    pages = [
        "🔧 5-Tool Analyzer",
        "💬 AI Chat & Ideal Employee",
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

    if page == "🔧 5-Tool Analyzer":
        st.title("🔧 5-Tool Employee Framework Analyzer")
        employee_info = st.text_area(
            "Paste employee details (e.g., performance reviews, 360 feedback, bio):",
            height=200,
            placeholder="John excels in routine tasks but struggles with quick changes."
        )
        if st.button("🚀 Generate Analysis"):
            if not employee_info:
                st.warning("Please paste some info first!")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        prompt = f"""
                        Analyze using 5-Tool Framework:
                        - Hitting for Average: Technical competence, consistency.
                        - Power: Strategic impact, decision-making.
                        - Speed: Adaptability, quick learning.
                        - Arm Strength: Teamwork, collaboration.
                        - Fielding: Stress resilience, reliability.
                        Employee info: {employee_info}
                        Score 1-10 each, 1-2 insights. Markdown format.
                        """
                        completion = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.markdown("### 📊 Analysis")
                        st.markdown(completion.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}. Check OpenAI API key.")

    elif page == "💬 AI Chat & Ideal Employee":
        st.title("💬 AI Chat: Build Ideal 5-Tool Profile")
        st.write("Enter job descriptions, resumes, etc., to build an ideal employee profile. Feature coming soon...")

    elif page == "📂 Repository ($9.99)":
        st.title("📂 Repository")
        if st.text_input("Enter access code ($9.99)", type="password") == "PAID999":
            st.session_state['Repository'] = True
            st.subheader("Repository")
            dept = st.text_input("Department")
            pos = st.text_input("Position")
            data_type = st.selectbox("Data Type", ["Job Desc", "Good Resume", "Bad Resume", "Good Review", "Bad Review", "Good Interview", "Bad Interview", "Notes"])
            content = st.text_area("Content")
            if st.button("Save"):
                try:
                    supabase.table('repo').insert({
                        'user_id': st.session_state.user_id,
                        'department': dept,
                        'position': pos,
                        'data_type': data_type,
                        'content': content,
                        'timestamp': datetime.now().isoformat()
                    }).execute()
                    st.success("Saved!")
                except Exception as e:
                    st.error(f"Save error: {str(e)}")
            st.subheader("Stored Data")
            try:
                data = supabase.table('repo').select('*').eq('user_id', st.session_state.user_id).execute().data
                for row in data:
                    st.write(f"{row['department']} - {row['position']} ({row['data_type']}): {row['content']} [{row['timestamp']}]")
            except Exception as e:
                st.error(f"Fetch error: {str(e)}")
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
            try:
                prompt = f"Score 360 feedback based on grid for: {notes}"
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Analysis error: {str(e)}")

    else:
        st.title(page)
        st.write("Feature coming soon...")

    st.sidebar.markdown("Logout")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
