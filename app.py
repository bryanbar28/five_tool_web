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
    st.title("🧠 Behavioral Intelligence App — Template Discovery")

    role_query = st.text_input(
        "Ask me anything about job reviews, templates, or phrases",
        placeholder="e.g., steel machinist, mechanic, I need help writing a review"
    )

    if role_query:
        st.markdown(f"🔍 You asked: **{role_query}**")
        role = role_query.lower()

        # ✅ Conversational explanation for open-ended questions
        if "what is a job review" in role or "define job review" in role:
            st.markdown("### 📘 What Is a Job Review?")
            st.markdown("""
            A **job review** is a structured evaluation of an employee's performance, responsibilities, and contributions in a specific role. It often includes:
            - A summary of duties and expectations  
            - Feedback on strengths and areas for improvement  
            - Discussion of goals, compensation, or promotion potential  
            - A record for HR and future reference  

            Job reviews can be formal (annual performance reviews) or informal (feedback sessions), and they vary by industry and company culture.
            """)
            return

        # ✅ Conversational fallback for vague help requests
        if "help" in role or "phrases" in role or "statements" in role:
            st.markdown("### 💬 Helpful Job Review Phrases & Comments")
            st.markdown("- [Status.net: Job Knowledge Phrases](https://status.net/articles/job-knowledge-performance-review-phrases-paragraphs-examples/)")
            st.markdown("- [BuddiesHR: 75 Review Phrases](https://blog.buddieshr.com/75-effective-performance-review-phrases-examples/)")
            st.markdown("- [Engage & Manage: 120 Review Comments](https://engageandmanage.com/blog/performance-review-example-phrases-comments/)")
            return

        # ✅ Role-specific or general template links
        st.markdown("### 🌐 General Review Templates and Examples")
        st.markdown("- [Native Teams: 30 Role-Based Review Examples](https://nativeteams.com/blog/performance-review-examples)")
        st.markdown("- [BetterUp: 53 Performance Review Examples](https://www.betterup.com/blog/performance-review-examples)")
        st.markdown("- [Indeed: Review Template Library](https://www.indeed.com/career-advice/career-development/performance-review-template)")
# -------------------------------
# 🎬 Gritty Job Review Generator
# -------------------------------
def generate_job_review(query):
    st.info(f"🔍 Generating realistic job review for: **{query}**")

    prompt = f"""
    Write a realistic, role-specific job review for the position: {query}.
    Use a clear, professional tone with practical insights. Include:

    - Job Summary: What the role typically involves
    - Key Responsibilities: 3–5 bullet points
    - Required Skills and Tools
    - Compensation and Schedule (typical ranges)
    - Pros: What employees tend to appreciate
    - Cons: Common challenges or frustrations
    - Interview Tips: Questions to ask or red flags to watch for
    - Career Path: Typical progression in this role

    Avoid generic corporate language. Make it useful for someone considering this job.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a workplace analyst writing realistic job reviews for professionals."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        review_text = response.choices[0].message.content
        st.markdown("### 🧾 Realistic Job Review")
        st.write(review_text)

    except Exception as e:
        st.error(f"❌ Error generating review: {e}")
# -------------------------------
# ✅ Module 1 Wrapper
# -------------------------------
def render_module_1():
    st.title("🧠 Behavioral Intelligence App — Job Review Explorer")

    # Section 1: Ask me anything
    role_query = st.text_input("Ask me anything about job reviews, templates, or phrases", placeholder="e.g., steel machinist, mechanic, I need help writing a review")

    if role_query:
        st.markdown(f"🔍 Searching for job review resources related to: **{role_query}**")
        role = role_query.lower()

        # Conversational fallback
        if "help" in role or "phrases" in role or "statements" in role:
            st.markdown("### 💬 Helpful Job Review Phrases & Comments")
            st.markdown("- [Status.net: Job Knowledge Phrases](https://status.net/articles/job-knowledge-performance-review-phrases-paragraphs-examples/)")
            st.markdown("- [BuddiesHR: 75 Review Phrases](https://blog.buddieshr.com/75-effective-performance-review-phrases-examples/)")
            st.markdown("- [Engage & Manage: 120 Review Comments](https://engageandmanage.com/blog/performance-review-example-phrases-comments/)")
            return

        # Role-specific examples
        st.markdown("### 🌐 General Review Templates and Examples")
        st.markdown("- [Native Teams: 30 Role-Based Review Examples](https://nativeteams.com/blog/performance-review-examples)")
        st.markdown("- [BetterUp: 53 Performance Review Examples](https://www.betterup.com/blog/performance-review-examples)")
        st.markdown("- [Indeed: Review Template Library](https://www.indeed.com/career-advice/career-development/performance-review-template)")

    # Section 2: Generate custom review
    st.markdown("---")
    st.subheader("🧾 Generate a Custom Job Review")

    review_input = st.text_input("Enter a role to generate a custom review", placeholder="e.g., diesel mechanic, tribal grant writer")

    if st.button("Generate Review"):
        if review_input:
            generate_job_review(review_input)
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
