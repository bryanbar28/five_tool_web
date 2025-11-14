import streamlit as st
from openai import OpenAI  # ✅ OpenAI client import

st.set_page_config(page_title="Five-Tool App", layout="wide")

# ✅ Session state setup
if "initial_review" not in st.session_state:
    st.session_state.initial_review = ""
    
if "show_repository" not in st.session_state:
    st.session_state.show_repository = False

# ✅ OpenAI client setup
client = OpenAI(api_key="your-openai-api-key")  # or use os.getenv("OPENAI_API_KEY")

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
    "Page 1: AI HR Assistant - Job Reviews",
    "Page 2: Job Descriptions Generator",
    "Page 3: The 5 Tool Employee Framework",
    "page 4: The 5 Tool Employee Framework: Deep Research Version", 
    "Page 5: Management Training",
    "Page 6: Behavior Under Pressure Grid",
    "Page 7: Behavioral Calibration Grid",
    "Page 8: Toxicity in the Workplace",
    "Page 9: Leadership Eligibility",
    "Page 10: SWOT 2.0",
    "Page 11: M&A Intelligence",
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
def generate_job_review(role, notes=None):
    st.info(f"🔍 Generating realistic job review for: **{role}**")

    prompt = f"""
    Write a realistic, role-specific job review for the position: {role}.
    Use a clear, professional tone with practical insights. Include:

    - Job Summary
    - Key Responsibilities
    - Required Skills and Tools
    - Compensation and Schedule
    - Pros and Cons
    - Interview Tips
    - Career Path

    Avoid generic corporate language. Make it useful for someone considering this job.
    """

    if notes:
        prompt += f"\n\nIncorporate these user-provided notes into the review:\n{notes}"

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
    st.title("🤖 AI HR Assistant — Job Reviews")
    st.markdown("⚠️ **Disclaimer:** All work generated on this page will not be saved unless you subscribe to Repository Access.")

    # 1️⃣ Conversational Discovery
    role_query = st.text_input("Ask me anything about job reviews, templates, or phrases", placeholder="e.g., steel machinist, mechanic, I need help writing a review")
    if role_query:
        st.markdown(f"🔍 You asked: **{role_query}**")
        role = role_query.lower()

        if "what is a job review" in role or "define job review" in role:
            st.markdown("### 📘 What Is a Job Review?")
            st.markdown("""
            A **job review** is a structured evaluation of an employee's performance, responsibilities, and contributions in a specific role. It often includes:
            - A summary of duties and expectations  
            - Feedback on strengths and areas for improvement  
            - Discussion of goals, compensation, or promotion potential  
            - A record for HR and future reference  
            """)
            return

        if "help" in role or "phrases" in role or "statements" in role:
            st.markdown("### 💬 Helpful Job Review Phrases & Comments")
            st.markdown("- [Status.net: Job Knowledge Phrases](https://status.net/articles/job-knowledge-performance-review-phrases-paragraphs-examples/)")
            st.markdown("- [BuddiesHR: 75 Review Phrases](https://blog.buddieshr.com/75-effective-performance-review-phrases-examples/)")
            st.markdown("- [Engage & Manage: 120 Review Comments](https://engageandmanage.com/blog/performance-review-example-phrases-comments/)")
            return

        st.markdown("### 🌐 General Review Templates and Examples")
        st.markdown("- [Native Teams: 30 Role-Based Review Examples](https://nativeteams.com/blog/performance-review-examples)")
        st.markdown("- [BetterUp: 53 Performance Review Examples](https://www.betterup.com/blog/performance-review-examples)")
        st.markdown("- [Indeed: Review Template Library](https://www.indeed.com/career-advice/career-development/performance-review-template)")

    # 2️⃣ Role Input
    review_input = st.text_input("Enter a role to generate a custom review", placeholder="e.g., diesel mechanic, federal grant writer")

    # 3️⃣ Generate Review Button
    if st.button("Generate Review"):
        if review_input:
            review_text = generate_job_review(review_input)
            st.session_state.initial_review = review_text
            st.session_state.show_repository = True
        else:
            st.warning("Please enter a role to generate a review.")

    # 4️⃣ Notes Input
    notes_input = st.text_area("Notes to add (optional)", placeholder="e.g., I work second shift, handle QA reports, and train new hires")

    # 5️⃣ Regenerate Review Button
    if st.button("Regenerate Review"):
        if review_input:
            combined_notes = f"{st.session_state.initial_review}\n\nAdditional notes:\n{notes_input}"
            generate_job_review(review_input, combined_notes)
            st.session_state.show_repository = True
        else:
            st.warning("Please enter a role to regenerate the review.")
        
# -------------------------------
# 🎬 Job Description Generator (Page 2)
# -------------------------------
def generate_job_description(role, notes=None):
    st.info(f"🔍 Generating job description for: **{role}**")

    prompt = f"""
    Write a detailed, professional job description for the role: {role}.
    Include:
    - Job Title
    - Job Summary
    - Key Responsibilities
    - Required Skills & Qualifications
    - Preferred Experience
    - Compensation & Benefits
    - Work Schedule
    - Career Path
    """

    if notes:
        prompt += f"\n\nIncorporate these user-provided notes:\n{notes}"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an HR specialist writing accurate and engaging job descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=900
        )

        description_text = response.choices[0].message.content
        st.markdown("### 🧾 Generated Job Description")
        st.write(description_text)
        return description_text

    except Exception as e:
        st.error(f"❌ Error generating job description: {e}")

def render_module_2():
    st.title("📄 Job Description Generator")
    st.markdown("⚠️ **Disclaimer:** All work generated on this page will not be saved unless you subscribe to Repository Access.")

    # 1️⃣ Conversational Discovery
    query = st.text_input(
        "Ask me anything about creating a job description",
        placeholder="e.g., how to write a job description for a project manager",
        key="job_desc_query"
    )

    if query:
        st.markdown(f"🔍 You asked: **{query}**")
        q_lower = query.lower()

        if "what is a job description" in q_lower or "define job description" in q_lower:
            st.markdown("### 📘 What Is a Job Description?")
            st.markdown("""
            A **job description** is a formal document outlining the duties, responsibilities, qualifications, and expectations for a specific role. It helps:
            - Attract qualified candidates
            - Set clear performance standards
            - Align hiring with organizational goals
            """)
            return  # ✅ inside the function

        if "help" in q_lower or "examples" in q_lower or "templates" in q_lower:
            st.markdown("### 🌐 Helpful Job Description Resources")
            st.markdown("- Indeed: Job Description Samples")
            st.markdown("- [BetterTeam: Job Description Templates")
            st.markdown("- BetterTeam: Job Description Templates")
            st.markdown("- SHRM: Writing Effective Job Descriptions")
            return  # ✅ inside the function

        # ✅ AI fallback
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an HR expert answering questions about job descriptions."},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=500
            )
            ai_answer = response.choices[0].message.content
            st.markdown("### 🤖 AI Response")
            st.write(ai_answer)

        except Exception as e:
            st.error(f"❌ Error generating AI response: {e}")

    # ✅ Other UI elements
    role_input = st.text_input(
        "Enter a generic role to create a skeleton of the job description",
        placeholder="e.g., software engineer, HR manager",
        key="job_desc_role"
    )

    if st.button("Generate Job Description", key="generate_job_desc"):
        if role_input:
            description_text = generate_job_description(role_input)
            st.session_state.initial_description = description_text
            st.session_state.show_repository = True
        else:
            st.warning("Please enter a role to generate a job description.")

    notes_input = st.text_area(
        "Notes to add (optional)",
        placeholder="e.g., remote work, bilingual preferred, experience with ERP systems",
        key="job_desc_notes"
    )

    if st.button("Regenerate Job Description", key="regenerate_job_desc"):
        if role_input:
            combined_notes = f"{st.session_state.initial_description}\n\nAdditional notes:\n{notes_input}"
            generate_job_description(role_input, combined_notes)
            st.session_state.show_repository = True
        else:
            st.warning("Please enter a role to regenerate the job description.")
def render_module_3():
    st.title("The 5 Tool Employee Framework")

    # ✅ Display intro content
    st.markdown("### _Introduction into the 5 Tool Employee Framework_")
    st.markdown("_An Interchangeable Model_")
    st.markdown("#### 5 Tool Baseball Player")
    st.markdown("""
    - **Hitting for Average** – Consistently making contact and getting on base.
    - **Hitting for Power** – Ability to drive the ball for extra bases or home runs.
    - **Speed** – Quickness on the bases and in the field.
    - **Fielding** – Defensive ability, including range and reaction time.
    - **Arm Strength** – Throwing ability, especially for outfielders and infielders.
    """)

    st.markdown("#### Baseball Tools vs. Professional Skills")
    st.markdown("""
    - ⚾ **Hitting → Technical Competence**
    - 🧠 **Fielding → Problem-Solving Ability**
    - ⚡ **Speed → Adaptability & Continuous Learning**
    - 💪 **Arm Strength → Communication & Leadership**
    - 🚀 **Power → Strategic Decision-Making**
    """)

    st.markdown("---")

    # ✅ Persistent AI Chatbox
    st.subheader("🤖 Ask AI About the Framework")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask a question (e.g., 'Tell me more about the framework', 'Can you recommend trainings?')")

    if st.button("Send Question"):
        if user_question.strip():
            try:
                # ✅ Curated training links for common topics
                curated_links = """
                Recommended Online Training:
                - [Agile Decision-Making Frameworks – Coursera](https://www.coursera.org/learn/agile-decision-making-frameworks)
                - [Effective Communication for Today’s Leader – Coursera](https://www.coursera.org/learn/effective-communication-for-todays-leader)
                - [Strategic Thinking – IMD Online](https://www.imd.org/strategy/st/online-course-strategy/)
                - [Conflict Resolution Skills – UC Irvine on Coursera](https://www.coursera.org/courses?query=conflict%20resolution)
                - [Adaptability & Resilience – Coursera](https://www.coursera.org/courses?query=adaptability)
                """

                # ✅ System prompt includes logic for training recommendations
                system_prompt = f"""
                You are an expert on the 5 Tool Employee Framework and baseball analytics.
                If the user asks for training recommendations, provide curated links like these:
                {curated_links}
                Also, search for additional relevant resources if possible.
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.7,
                    max_tokens=700
                )
                ai_answer = response.choices[0].message.content
                st.session_state.chat_history.append((user_question, ai_answer))
            except Exception as e:
                st.error(f"❌ Error generating AI response: {e}")
        else:
            st.warning("Please enter a question before sending.")

    # ✅ Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        for q, a in st.session_state.chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**AI:** {a}")
            st.markdown("---")

    st.markdown("---")

    # ✅ Notes section for custom 5 Tool Employee
    st.subheader("🛠 Add notes to create your own 5 Tool Employee")
    notes_input = st.text_area("Enter notes about your ideal employee or evaluation criteria", placeholder="e.g., strong leadership, adaptable, great communicator")

    if st.button("Generate 5 Tool Employee"):
        if notes_input.strip():
            try:
                # ✅ Hidden Deep-Research Framework embedded in system prompt
                deep_research_framework = """
                The Deep-Research 5-Tool Employee Framework:
                - Speed: Cognitive & Behavioral Agility
                - Power: Ownership, Initiative & Decisiveness
                - Fielding: Strategic Foresight & System Protection
                - Hitting for Average: Reliability, Rhythm & Repeatability
                - Arm Strength: Communication Reach & Influence
                Each includes Natural Gift, High-Functioning Expression, Dysfunction Signals, Behavioral Insights, and Where It Shows Up.
                """

                prompt = f"""
                Use the following framework (hidden from user) to generate a layman-friendly, business-focused 5 Tool Employee profile:
                {deep_research_framework}

                User notes: {notes_input}

                Output should:
                - Be clear and practical (avoid jargon).
                - Include sections for: Technical Competence, Problem-Solving Ability, Adaptability & Continuous Learning, Communication & Leadership, Strategic Decision-Making.
                - Provide strengths and improvement areas.
                - Avoid baseball references completely.
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an HR strategist using a behavioral framework to create practical employee profiles."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=700
                )
                profile = response.choices[0].message.content
                st.markdown("### 🧾 Your Custom 5 Tool Employee Profile")
                st.write(profile)
            except Exception as e:
                st.error(f"❌ Error generating profile: {e}")
        else:
            st.warning("Please add notes before generating the profile.")
    
def render_module_4():
    st.title("The 5 Tool Employee Framework: Deep Research Version")
    st.image("images/module5_calibration_grid.png")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_5():
    st.title("📚 Management Training — AI Resource Finder")
    st.markdown("### Ask AI for any training, article, video, or resource in leadership, HR, or management topics.")

    # ✅ Initialize chat history
    if "training_chat_history" not in st.session_state:
        st.session_state.training_chat_history = []

    # ✅ User input
    user_query = st.text_input("Ask about any training topic (e.g., 'Delegation 101', 'Conflict Resolution', 'Executive Coaching')")

    if st.button("Send Query"):
        if user_query.strip():
            try:
                # ✅ Embed the full topic list into the system prompt for retrieval
                topic_list = """
                INTRO LEVEL:
                Transition from Individual Contributor to Leader, Delegation 101, Time Management for New Managers,
                Giving & Receiving Feedback (SBI model), Running Effective 1:1s, Basic Goal Setting (SMART),
                Intro to Emotional Intelligence, Active Listening, Motivation Hygiene Theory (Herzberg),
                Recognizing Burnout Signs, Anti-Harassment Basics, FMLA Overview, Payroll & Overtime Rules,
                Documenting Performance Conversations, Tuckman Stages, Running Your First Team Meeting,
                Ice-Breakers & Psychological Safety.

                MID-LEVEL:
                Situational Leadership II, Coaching vs. Mentoring, Crucial Conversations, Managing Up & Across,
                Setting OKRs, Calibration Sessions, PIP Design & Legal Safety, 360 Feedback Systems,
                Bias in Performance Reviews, Job Analysis & Competency Modeling, Selection Interview Techniques,
                Validity & Reliability of Assessments, Employee Engagement Surveys, Change Management (Kotter 8-Step),
                Conflict Resolution Styles (Thomas-Kilmann), Team Decision-Making Biases, Culture Audits,
                IDP Creation, Succession Planning Basics, Learning Agility, Micro-Learning Design,
                EEOC, ADA, Title VII Case Studies, Global Mobility & Expat Packages, Data Privacy (GDPR/CCPA).

                EXPERT LEVEL:
                Balanced Scorecard, Leadership Pipeline, Stakeholder Mapping, Scenario Planning,
                Predictive Turnover Models, Network Analysis of Collaboration, Diversity Metrics & ROI,
                Skills Ontology & Gap Analysis, Matrix vs. Functional Structures, Agile @ Scale for Non-Tech,
                Span of Control Optimization, M&A Cultural Integration, Leadership Assessment Centers,
                Psychometric Validation Studies, Counterproductive Work Behavior, High-Potential Identification,
                ADKAR Deep Dive, Prosci Certification Modules, Resistance Typology, Transformation Playbooks,
                Pay Equity Analysis, LTI Design, Clawback Policies, Say-on-Pay Prep, Works Council Negotiation,
                International Assignment Policy, Cultural Intelligence (CQ).

                EXECUTIVE LEVEL:
                HR as Business Partner, Workforce Planning @ Board Level, ESG & Human Capital Reporting,
                CEO Succession, Executive Termination Protocols, Whistleblower Systems, DEI Crisis Comms,
                Labor Union Strategy, AI-Augmented Workforce, Gig Economy Governance, Remote/Hybrid Operating Models,
                Skills-Based Org, Comp Committee Charter, Human Capital Metrics in 10-K, Say-on-Pay Defense,
                Activist Investor Prep, Executive Derailers, Dark Triad Screening, Neuroscience of Decision-Making,
                Cultural Due Diligence Playbook, Retention Bonus Modeling, Synergy Capture via People.

                CROSS-LEVEL MODULES:
                Inclusive Leadership & Allyship, Mental Health First Aid, Data Literacy for Managers,
                AI Ethics in HR, Storytelling with Data, Negotiation Mastery.
                """

                system_prompt = f"""
                You are an AI resource curator for management and HR training. Match user queries to the closest topics
                from this list and provide:
                - A short explanation of the topic
                - Recommended training resources (courses, articles, videos)
                - Practical tips or frameworks
                Topic list:
                {topic_list}
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_query}
                    ],
                    temperature=0.7,
                    max_tokens=700
                )

                ai_answer = response.choices[0].message.content
                st.session_state.training_chat_history.append((user_query, ai_answer))

            except Exception as e:
                st.error(f"❌ Error generating AI response: {e}")
        else:
            st.warning("Please enter a query before sending.")

    # ✅ Display chat history
    if st.session_state.training_chat_history:
        st.markdown("### 💬 Conversation History")
        for q, a in st.session_state.training_chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**AI:** {a}")
            st.markdown("---")

def render_module_6():
    st.title("Behavior Under Pressure")
    st.markdown("### What is the Behavior Under Pressure Grid?")
    st.markdown("""
    This grid shows how behavioral tools manifest in two states:
    - **Intentional Use:** Calm, focused, deliberate behavior.
    - **Under Duress:** How traits distort under stress.
    
    Use this tool for leadership diagnostics, hiring decisions, and team development.
    """)

    # ✅ Display the grid as a table
    data = {
        "Tool": ["Power", "Speed", "Fielding", "Hitting Avg.", "Arm Strength"],
        "Intentional Use": [
            "Drives results, owns outcomes",
            "Reflects, adjusts, integrates",
            "Foresees risks, protects systems",
            "Delivers consistently and reliably",
            "Aligns and influences with clarity"
        ],
        "Under Duress": [
            "Overreaches, avoids feedback",
            "Reacts, deflects, performs for show",
            "Freezes, rigidifies, blocks learning",
            "Checks out, avoids stretch or change",
            "Charms without clarity, dominates without connection"
        ]
    }
    st.table(data)

    # ✅ Add comments input
    user_comments = st.text_area("Add your comments or observations", placeholder="e.g., This candidate freezes under pressure but excels in planning.")

    # ✅ Generate AI insights
    if st.button("Generate Grid with Insights"):
        if user_comments.strip():
            st.subheader("🔍 AI Insights Based on Your Comments")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an organizational psychologist analyzing behavior under pressure."},
                    {"role": "user", "content": f"Analyze this comment in context of the Behavior Under Pressure Grid: {user_comments}"}
                ],
                temperature=0.7,
                max_tokens=400
            )
            st.write(response.choices[0].message.content)
        else:
            st.warning("Please add comments before generating insights.")


def render_module_7():
    st.title("🧠 Behavioral Calibration Grid")
    st.image("images/module5_calibration_grid.png")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_8():
    st.title("☢️ Toxicity in the Workplace")
    st.image("images/module6_toxicity_scale.png")
    st.image("images/module6_toxicity_scoring.png")
    st.text_area("AI Chat: Ask about Padilla, Hogan, Kaiser, Machiavellianism")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_9():
    st.title("🏆 Leadership Eligibility")
    st.image("images/module7_calibration_grid.png")
    st.image("images/module7_eligibility_filter.png")
    st.image("images/module7_scoring_scale.png")
    st.image("images/module7_diagnostic_rubric.png")
    st.image("images/module7_outcomes.png")

def render_module_10():
    st.title("📊 SWOT 2.0 Strategic Framework")
    st.markdown("Designed by Bryan Barrera &amp; Microsoft Copilot")

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

def render_module_11():
    st.title("🏢 M&amp;A Intelligence (Premium)")
    st.warning("Subscription required")
    st.file_uploader("Upload Resumes", accept_multiple_files=True)
    st.file_uploader("Upload Job Descriptions", accept_multiple_files=True)
    st.file_uploader("Upload Performance Reviews", accept_multiple_files=True)
    st.file_uploader("Upload Training &amp; Education Records", accept_multiple_files=True)
    st.text_area("Branch Data: Name, Location, Benefits")
    st.button("Generate Analysis")

def render_module_12():
    st.title("🚧 Page 12: Under Construction")
    st.markdown("This page is not yet implemented.")
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
    PAGES[11]: render_module_12,
}

if selected_page in PAID_PAGES and not is_unlocked(selected_page):
    unlock_page(selected_page, PAID_PAGES[selected_page])
else:
    PAGE_RENDERERS[selected_page]() 
