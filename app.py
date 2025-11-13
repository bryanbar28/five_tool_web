import streamlit as st
from openai import OpenAI

# =============================================
# ✅ Unified Streamlit App with AI-Powered SWOT
# =============================================

# -------------------------------
# 🔐 Subscription Logic (Placeholder)
# -------------------------------
PAID_PAGES = {
    "Page 9: M&A Intelligence": "$19.99/mo",
    "Page 10: Finding the Right Fit": "$3.99/mo",
    "Page 11: Your Ego": "$3.99/mo",
    "Page 12: Repository": "$9.99/mo"
}

def is_unlocked(page):
    # Placeholder logic for subscription check
    return False

def unlock_page(page, price):
    st.warning(f"This page requires a subscription: {price}")
    st.button("Unlock Now")

# -------------------------------
# 📚 Module Navigation
# -------------------------------
PAGES = [
    "Page 1: Behavioral Intelligence",
    "Page 2: Job Description Generator",
    "Page 3: Performance Review Generator",
    "Page 4: Behavior Under Pressure Grid",
    "Page 5: Behavioral Calibration Grid",
    "Page 6: Toxicity in the Workplace",
    "Page 7: Leadership Eligibility",
    "Page 8: SWOT 2.0",
    "Page 9: M&A Intelligence",
    "Page 10: Finding the Right Fit",
    "Page 11: Your Ego",
    "Page 12: Repository"
]

selected_page = st.sidebar.selectbox("Choose a page", PAGES)

# -------------------------------
# 🔍 OpenAI Setup
client = OpenAI()

# -------------------------------
# 🧠 Template Discovery Module
# -------------------------------
def render_template_discovery():
# your template discovery logic...
# -------------------------------
# 🎬 Gritty Job Review Generator
# -------------------------------
def generate_job_review(query):
    st.info(f"🎥 Generating gritty, role-specific job review for: **{query}**")

    prompt = f"""
    Write a brutally honest, insider-style job review for the role: {query}.
    Use the voice of a veteran in the field. Include:
    - Overall rating (1–5)
    - What the job actually involves (percent breakdown)
    - Pay, hours, bonuses
    - Pros and cons (real talk)
    - Red flags to ask in interviews
    - Career path
    - A hot take to close it out

    Make it sound like a voiceover script for a video. Use bullet points and bold formatting.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a gritty, experienced tradesperson writing job reviews for video scripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=800
        )

        review_text = response.choices[0].message.content
        st.markdown("### 🎬 Real-World Job Review")
        st.write(review_text)

    except Exception as e:
        st.error(f"❌ Error generating review: {e}")
# -------------------------------
# ✅ Module 1 Wrapper
# -------------------------------
def render_module_1():
    render_template_discovery()

    # Add a second input field and button to trigger review generation
    role_input = st.text_input("Want a gritty video-style job review?", placeholder="e.g., steel machinist, diesel mechanic")
    if st.button("🎬 Generate Real-World Review"):
        if role_input:
            generate_job_review(role_input)
        else:
            st.warning("Please enter a role to generate a review.")
    
def render_module_2():
    st.title("📄 Job Description Generator")
    st.text_area("Paste job description or request one by role")

def render_module_3():
    st.title("📋 Performance Review Generator")
    st.text_area("Paste review or request one by role")

def render_module_4():
    st.title("⚾ Behavior Under Pressure Grid")
    st.image("images/module4_behavior_grid.png")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_5():
    st.title("🧠 Behavioral Calibration Grid")
    st.image("images/module5_calibration_grid.png")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_6():
    st.title("☢️ Toxicity in the Workplace")
    st.image("images/module6_toxicity_scale.png")
    st.image("images/module6_toxicity_scoring.png")
    st.text_area("AI Chat: Ask about Padilla, Hogan, Kaiser, Machiavellianism")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_7():
    st.title("🏆 Leadership Eligibility")
    st.image("images/module7_calibration_grid.png")
    st.image("images/module7_eligibility_filter.png")
    st.image("images/module7_scoring_scale.png")
    st.image("images/module7_diagnostic_rubric.png")
    st.image("images/module7_outcomes.png")

def render_module_8():
    st.title("📊 SWOT 2.0 Strategic Framework")
    st.markdown("Designed by Bryan Barrera & Microsoft Copilot")

    notes = st.text_area("Additional Notes and Input")
    ai_chat = st.text_area("AI Chat: Ask for SWOT templates, Lean tools, Fishbone diagrams")

    if st.button("🎯 Generate AI-Powered SWOT"):
        strengths = f"Strengths based on input: {notes[:50]}..."
        weaknesses = f"Weaknesses based on input: {notes[:50]}..."
        opportunities = f"Opportunities based on input: {ai_chat[:50]}..."
        threats = f"Threats based on input: {ai_chat[:50]}..."

        st.subheader("✅ Generated SWOT Analysis")
        st.write("**Strengths:**", strengths)
        st.write("**Weaknesses:**", weaknesses)
        st.write("**Opportunities:**", opportunities)
        st.write("**Threats:**", threats)

def render_module_9():
    st.title("🏢 M&A Intelligence (Premium)")
    st.warning("Subscription required")
    st.file_uploader("Upload Resumes", accept_multiple_files=True)
    st.file_uploader("Upload Job Descriptions", accept_multiple_files=True)
    st.file_uploader("Upload Performance Reviews", accept_multiple_files=True)
    st.file_uploader("Upload Training & Education Records", accept_multiple_files=True)
    st.text_area("Branch Data: Name, Location, Benefits")
    st.button("Generate Analysis")

def render_module_10():
    st.title("📘 Finding the Right Fit (Book)")
    st.warning("Subscription required")
    st.markdown("Coming Soon: AI-assisted workbook experience")

def render_module_11():
    st.title("📕 Your Ego: The Real Reason Your Business is Failing")
    st.warning("This book requires a $3.99/mo subscription.")
    st.markdown("Coming Soon: Interactive reading experience")

def render_module_12():
    st.title("🗂️ Repository (Premium)")
    st.warning("This module requires a $9.99/mo subscription.")
    st.file_uploader("Upload any file to store")
    st.text_area("Save generated profiles or notes")
    st.button("Save to Repository")

# -------------------------------
# 🚀 Module Execution
# -------------------------------
PAGE_RENDERERS = {
    PAGES[0]: render_module_1,
    PAGES[1]: render_module_2,
    PAGES[2]: render_module_3,
    PAGES[3]: render_module_4,
    PAGES[4]: render_module_5,
    PAGES[5]: render_module_6,
    PAGES[6]: render_module_7,
    PAGES[7]: render_module_8,
    PAGES[8]: render_module_9,
    PAGES[9]: render_module_10,
    PAGES[10]: render_module_11,
    PAGES[11]: render_module_12
}

if selected_page in PAID_PAGES and not is_unlocked(selected_page):
    unlock_page(selected_page, PAID_PAGES[selected_page])
else:
    PAGE_RENDERERS[selected_page]()
