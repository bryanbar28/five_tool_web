# -------------------------------
# Imports
# -------------------------------
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from openai import OpenAI
from googleapiclient.discovery import build

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Five-Tool App", layout="wide")

# -------------------------------
# Session State Setup
# -------------------------------
if "initial_review" not in st.session_state:
    st.session_state.initial_review = ""
if "show_repository" not in st.session_state:
    st.session_state.show_repository = False

# -------------------------------
# OpenAI Client Setup
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Use environment variable

# -------------------------------
# API Keys
# -------------------------------
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = "YOUR_CHANNEL_ID"

# -------------------------------
# Helper Functions
# -------------------------------
def fetch_youtube_videos():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        maxResults=20,
        order="date"
    )
    response = request.execute()
    videos = []
    for item in response.get("items", []):
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        videos.append({"title": video_title, "url": video_url})
    return videos

def map_videos_to_tools(videos):
    mapping = {
        "Hitting for Average": None,
        "Fielding": None,
        "Speed": None,
        "Arm Strength": None,
        "Power": None
    }
    for video in videos:
        title = video["title"].lower()
        if "technical" in title or "competence" in title or "hitting" in title:
            mapping["Hitting for Average"] = video["url"]
        elif "problem" in title or "fielding" in title or "solution" in title:
            mapping["Fielding"] = video["url"]
        elif "adaptability" in title or "speed" in title or "learning" in title:
            mapping["Speed"] = video["url"]
        elif "communication" in title or "leadership" in title or "arm" in title:
            mapping["Arm Strength"] = video["url"]
        elif "strategy" in title or "decision" in title or "power" in title:
            mapping["Power"] = video["url"]
    return mapping

# -------------------------------
# Subscription Logic
# -------------------------------
PAID_PAGES = {
    "Page 10: M&A Intelligence": "$19.99/mo",  # ✅ Fixed mismatch
    "Page 11: Repository": "$9.99/mo"
}

def is_unlocked(page):
    return False  # Placeholder for future subscription logic

def unlock_page(page, price):
    st.warning(f"This page requires a subscription: {price}")
    st.button("Unlock Now")

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
    notes_input = st.text_area("Notes to add or restructure (optional)", placeholder="e.g., I work second shift, handle QA reports, and train new hires")

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
        
    # ✅ Initialize history
    if "job_desc_chat_history" not in st.session_state:
        st.session_state.job_desc_chat_history = []

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
            ai_answer = """
            A **job description** is a formal document outlining the duties, responsibilities, qualifications, and expectations for a specific role. It helps:
            - Attract qualified candidates
            - Set clear performance standards
            - Align hiring with organizational goals
            """
            st.markdown("### 📘 What Is a Job Description?")
            st.markdown(ai_answer)
            st.session_state.job_desc_chat_history.append((query, ai_answer))  # ✅ Save to history
        elif "help" in q_lower or "examples" in q_lower or "templates" in q_lower:
            ai_answer = """
            ### 🌐 Helpful Job Description Resources
            - Indeed: Job Description Samples
            - BetterTeam: Job Description Templates
            - SHRM: Writing Effective Job Descriptions
            """
            st.markdown(ai_answer)
            st.session_state.job_desc_chat_history.append((query, ai_answer))  # ✅ Save to history
        else:
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
                st.session_state.job_desc_chat_history.append((query, ai_answer))  # ✅ Save to history

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

    # ✅ Clear History Section at Bottom
    if st.session_state.job_desc_chat_history:
        st.markdown("### 💬 Conversation History")
        for q, a in st.session_state.job_desc_chat_history[-10:]:
            st.markdown(f"**You:** {q}")
            st.markdown("**AI:**")
            st.markdown(a)
            st.markdown("---")

        if st.button("Clear History"):
            st.session_state.job_desc_chat_history = []
            st.success("✅ Conversation history cleared!")
            st.stop()  # ✅ Stops execution cleanly instead of rerun
    
def render_module_3():
    import streamlit as st

    st.title("📚 Management Training: Intro to beginner, mid, and expert level leadership — AI Resource Finder")
    st.markdown("### Ask AI for any training, article, video, or resource in leadership, HR, or management topics.")

    # ✅ Initialize chat history
    if "training_chat_history" not in st.session_state:
        st.session_state.training_chat_history = []

    # ✅ Full topic list
    topics = [
        "Transition from Individual Contributor to Leader",
        "Delegation 101",
        "Time Management for New Managers",
        "Giving & Receiving Feedback (SBI model)",
        "Running Effective 1:1s",
        "Basic Goal Setting (SMART)",
        "Intro to Emotional Intelligence",
        "Active Listening",
        "Motivation Hygiene Theory (Herzberg)",
        "Recognizing Burnout Signs",
        "Anti-Harassment Basics",
        "FMLA Overview",
        "Payroll & Overtime Rules",
        "Documenting Performance Conversations",
        "Tuckman Stages",
        "Running Your First Team Meeting",
        "Ice-Breakers & Psychological Safety",
        "Situational Leadership II",
        "Coaching vs. Mentoring",
        "Crucial Conversations",
        "Managing Up & Across",
        "Setting OKRs",
        "Calibration Sessions",
        "PIP Design & Legal Safety",
        "360 Feedback Systems",
        "Bias in Performance Reviews",
        "Job Analysis & Competency Modeling",
        "Selection Interview Techniques",
        "Validity & Reliability of Assessments",
        "Employee Engagement Surveys",
        "Change Management (Kotter 8-Step)",
        "Conflict Resolution Styles (Thomas-Kilmann)",
        "Team Decision-Making Biases",
        "Culture Audits",
        "IDP Creation",
        "Succession Planning Basics",
        "Learning Agility",
        "Micro-Learning Design",
        "EEOC, ADA, Title VII Case Studies",
        "Global Mobility & Expat Packages",
        "Data Privacy (GDPR/CCPA)",
        "Balanced Scorecard",
        "Leadership Pipeline",
        "Stakeholder Mapping",
        "Scenario Planning",
        "Predictive Turnover Models",
        "Network Analysis of Collaboration",
        "Diversity Metrics & ROI",
        "Skills Ontology & Gap Analysis",
        "Matrix vs. Functional Structures",
        "Agile @ Scale for Non-Tech",
        "Span of Control Optimization",
        "M&A Cultural Integration",
        "Leadership Assessment Centers",
        "Psychometric Validation Studies",
        "Counterproductive Work Behavior",
        "High-Potential Identification",
        "ADKAR Deep Dive",
        "Prosci Certification Modules",
        "Resistance Typology",
        "Transformation Playbooks",
        "Pay Equity Analysis",
        "LTI Design",
        "Clawback Policies",
        "Say-on-Pay Prep",
        "Works Council Negotiation",
        "International Assignment Policy",
        "Cultural Intelligence (CQ)",
        "HR as Business Partner",
        "Workforce Planning @ Board Level",
        "ESG & Human Capital Reporting",
        "CEO Succession",
        "Executive Termination Protocols",
        "Whistleblower Systems",
        "DEI Crisis Comms",
        "Labor Union Strategy",
        "AI-Augmented Workforce",
        "Gig Economy Governance",
        "Remote/Hybrid Operating Models",
        "Skills-Based Org",
        "Comp Committee Charter",
        "Human Capital Metrics in 10-K",
        "Say-on-Pay Defense",
        "Activist Investor Prep",
        "Executive Derailers",
        "Dark Triad Screening",
        "Neuroscience of Decision-Making",
        "Cultural Due Diligence Playbook",
        "Retention Bonus Modeling",
        "Synergy Capture via People",
        "Inclusive Leadership & Allyship",
        "Mental Health First Aid",
        "Data Literacy for Managers",
        "AI Ethics in HR",
        "Storytelling with Data",
        "Negotiation Mastery"
    ]

    # ✅ Dropdown + Text Input
    st.markdown("#### Select a topic or enter your own:")
    selected_topic = st.selectbox("Choose from HR topics:", topics)
    custom_query = st.text_input("Or enter your own topic:")
    query_to_send = custom_query.strip() if custom_query.strip() else selected_topic

    # ✅ Dynamic expander for all topics with clean formatting
    with st.expander("📖 Explanation, Description & Practical Tips"):
        st.markdown(f"""
**Explanation:**  
This topic covers best practices and strategies for {selected_topic}.  

**Description:**  
{selected_topic} is a critical area in leadership and HR that helps improve team performance and organizational success.  

**Practical Tips:**  
- Apply proven frameworks and models  
- Use case studies and real-world examples  
- Leverage tools and templates for implementation  
""")

    # ✅ Send Query Button with structured AI response including links
    if st.button("Send Query"):
        if query_to_send:
            try:
                system_prompt = f"""
                You are an AI resource curator for management and HR training. For ANY topic, respond in this structure:
                1. **Explanation:** A short summary of the topic.
                2. **Recommended Resources:** Include clickable links to relevant books, articles, videos, and training courses.
                3. **Practical Tips or Frameworks:** Provide actionable steps or frameworks related to the topic.
                Example format:
                **Explanation:** ...
                **Recommended Resources:** ...
                **Practical Tips or Frameworks:** ...
                Topic list:
                {', '.join(topics)}
                """
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": query_to_send}
                    ],
                    temperature=0.7,
                    max_tokens=700
                )
                ai_answer = response.choices[0].message.content
                st.session_state.training_chat_history.append((query_to_send, ai_answer))
            except Exception as e:
                st.error(f"❌ Error generating AI response: {e}")
        else:
            st.warning("Please enter a query or select a topic.")

    # ✅ Display chat history with "Structured Response" header
    if st.session_state.training_chat_history:
        st.markdown("### 💬 Conversation History")
        for q, a in st.session_state.training_chat_history[-10:]:
            st.markdown(f"**You:** {q}")
            st.markdown("**AI (Structured Response):**")
            st.markdown(a)
            st.markdown("---")

    # ✅ Clear History Button
    if st.button("Clear History"):
        st.session_state.training_chat_history = []
        st.success("✅ Conversation history cleared!")
        st.rerun()    
        

def render_module_4():
    # ✅ Title and Intro
    st.title("The 5 Tool Employee Framework")
    st.markdown("### _Introduction into the 5 Tool Employee Framework_")
    st.markdown(
        "An Interchangeable Model. Book available on Amazon: https://a.co/d/91S2rTc "
        "Finding the Right Fit and check out our YouTube channel: www.youtube.com/@5toolemployeeframework "
    )

    st.markdown("---")

    # ✅ Chatbox Section
    st.subheader("🤖 Ask AI About the Framework")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask a question (e.g., 'Tell me more about the framework', 'Can you recommend trainings?')")

    if st.button("Send Question"):
        if user_question.strip():
            try:
                system_prompt = """
                You are an expert on the 5 Tool Employee Framework.
                Always align answers with this mapping:
                Baseball Tools → Professional Skills:
                - Hitting for Average → Technical Competence
                - Fielding → Problem-Solving Ability
                - Speed → Adaptability & Continuous Learning
                - Arm Strength → Communication & Leadership
                - Power → Strategic Decision-Making
                Respond in this format:
                1. Tool → Skill
                   - Short explanation of why this matters.
                   - Video: https://www.youtube.com/@5toolemployeeframework
                At the end, include:
                Want to understand the framework further: **📚 Buy the Book on Amazon:** Finding the Right Fit: An AI Assisted HR Workbook Introducing the 5 Tool Employee Framework https://a.co/d/3nBKXXb
                Do NOT include any other external links.
                """
                # Placeholder for AI call
                ai_answer = f"(Simulated AI Response)\nQuestion: {user_question}\nVideo: https://www.youtube.com/@5toolemployeeframework"
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

    # ✅ Notes and Sliders Section
    st.subheader("🛠 Create Your Own 5 Tool Employee")
    notes_input = st.text_area("Enter notes about your ideal employee or evaluation criteria", placeholder="e.g., strong leadership, adaptable, great communicator")

    st.subheader("Rate the Employee on Each Tool (1–10)")
    scores = [st.slider(tool, 1, 10, 5) for tool in TOOLS]

    # ✅ Generate Profile Button
    if st.button("Generate 5 Tool Employee"):
        if notes_input.strip():
            try:
                ratings_text = "\n".join([f"- {tool}: {score}/10" for tool, score in zip(TOOLS, scores)])
                prompt = f"""
                Use the following framework to generate a layman-friendly, business-focused 5 Tool Employee profile:
                Ratings:
                {ratings_text}
                Notes:
                {notes_input}
                Output should:
                - Be clear and practical (avoid jargon).
                - Include sections for: Technical Competence, Problem-Solving Ability, Adaptability & Continuous Learning, Communication & Leadership, Strategic Decision-Making.
                - Provide strengths and improvement areas.
                - Avoid baseball references completely.
                Always include:
                - YouTube: https://www.youtube.com/@5toolemployeeframework
                - Amazon Book: https://a.co/d/3nBKXXb
                """
                # Placeholder for AI call
                st.markdown("### 🧠 Your Custom 5 Tool Employee Profile")
                st.write("(Simulated AI Response)\n" + prompt)

                # ✅ Radar Chart Visualization
                st.subheader("📊 5-Tool Employee Profile Radar")
                fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="5-Tool Employee Radar Chart")
                fig.update_traces(fill='toself')
                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"❌ Error generating profile: {e}")
        else:
            st.warning("Please add notes before generating the profile.")

    # ✅ Clear History Button
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.experimental_rerun()
            
def render_module_5():
    import streamlit as st

    st.title("Advanced Deep Research — The 5 Tool Employee Framework")

    # ✅ Display full PDF content in a scrollable section
    pdf_content = """
    _The Deep-Research 5-Tool Employee Framework_
    A behavioral operating system for high-performance environments. Designed to evaluate not just output, but behavior under pressure, natural tendencies, and the psychodynamic tensions that determine real-world effectiveness.

    Each tool includes:
    - Natural Gift: Innate tendencies that fuel the behavior
    - High-Functioning Expression: What excellence looks like
    - Dysfunction Signals: How strengths derail under pressure
    - Behavioral Insights: How to calibrate for sustained impact
    - Where It Shows Up: Cross-industry applications and archetypes

    #### Speed — Cognitive & Behavioral Agility
    Natural Gift: Pattern recognition, emotional agility, perceptual timing
    High-Functioning Expression:
    - Adjusts mid-motion with grace and clarity
    - Communicates with precise cadence—knowing when to pause, pivot, or push
    - Integrates feedback without spiraling or flinching
    - Creates momentum without overcomplication
    Dysfunction Signals:
    - Reacts impulsively to maintain control or optics
    - Mistakes urgency for depth
    - Avoids structure, defaults to charisma
    - Performs rather than processes under pressure
    Behavioral Insight: Psychological agility is the governor here—not raw reaction speed. Sustainable performance depends on metabolizing tension, not just masking it.
    Where It Shows Up:
    - Change management
    - Customer-facing adaptation
    - Executive communication in volatile contexts
    - Individual Contributors managing high-volume ambiguity

    #### Power — Ownership, Initiative & Decisiveness
    Natural Gift: Inner drive, conviction, will to close
    High-Functioning Expression:
    - Owns the mission from start to finish—no deflection
    - Pushes progress without waiting for consensus
    - Makes high-impact decisions that others align behind
    - Brings heat without burning bridges
    Dysfunction Signals:
    - Bulldozes collaboration for speed
    - Hides behind motion to deflect reflection
    - Overuses authority or energy to silence dissent
    - Equates charisma with clarity
    Behavioral Insight: Unchecked Power erodes trust. Under stress, ego and volume increase—but clarity and alignment disappear. Humility is the ultimate limiter.
    Where It Shows Up:
    - Founders and team leads
    - Accountable closers and operators
    - High-pressure roles with final-call authority

    #### Fielding — Strategic Foresight & System Protection
    Natural Gift: Systems awareness, anticipatory thinking, stability
    High-Functioning Expression:
    - Spots second- and third-order consequences early
    - Builds guardrails for scalable decision-making
    - Operates upstream of risk, not downstream of damage
    - Stays composed when uncertainty spikes
    Dysfunction Signals:
    - Becomes overly risk-averse or defensive
    - Resists new data or shifts in environment
    - Defaults to rigid safeguards that halt innovation
    - Blames others when overwhelmed
    Behavioral Insight: Fielding reveals emotional maturity through discipline—not reaction. Pressure doesn't break systems. People do, when foresight is missing.
    Where It Shows Up:
    - Compliance, audit, legal, ops
    - Strategic planning, QA, IT architecture
    - Team stabilizers and culture protectors

    #### Hitting for Average — Reliability, Rhythm & Repeatability
    Natural Gift: Execution discipline, operational precision, resilience
    High-Functioning Expression:
    - Delivers under pressure—quietly and predictably
    - Builds trust through consistency, not theatrics
    - Anchors workflows and norms others depend on
    - Focuses on base hits, not glory swings
    Dysfunction Signals:
    - Hides in routine to avoid ambiguity
    - Resents lack of recognition in flashy cultures
    - Over-indexes on habit and under-indexes on strategy
    - Performs tasks mechanically, loses intent
    Behavioral Insight: Culture often underrates the glue. But rhythm beats reaction, and trust beats tension. Recognition must find the quiet storm.
    Where It Shows Up:
    - Ops, customer success, fulfillment
    - Risk-sensitive execution roles
    - Individual Contributors who prevent chaos and catch the slack

    #### Arm Strength — Communication Reach & Influence
    Natural Gift: Expressive clarity, emotional connection, presence
    High-Functioning Expression:
    - Pitch it
    - Distills vision into language that moves people
    - Connects across functions and hierarchies effortlessly
    - Builds buy-in without overreaching
    - Communicates emotionally and intellectually
    Dysfunction Signals:
    - Charms without delivering substance
    - Dominates conversations, silences opposition
    - Uses messaging to mask misalignment
    - Prioritizes performance over truth
    Behavioral Insight: Influence that isn’t anchored in clarity becomes theater. Real communication reaches not just ears—but identity and belonging.
    Where It Shows Up:
    - Sales, enablement, leadership
    - Cross-functional translators
    - Cultural brokers and stakeholder wranglers
    """

    # ✅ Scrollable container for PDF content
    st.markdown(
        f"<div style='height:500px; overflow-y:auto; border:1px solid #ccc; padding:10px;'>{pdf_content}</div>",
        unsafe_allow_html=True
    )

    # ✅ Question input
    question = st.text_input("Ask a question about the framework:")

    # ✅ Dive Further button
    if st.button("Dive Further"):
        if question.strip():
            try:
                hidden_context = """
                Advanced Leadership Concepts:
                - Emotional Intelligence
                - Appreciative Inquiry
                - Maturana & Varela – Tree of Life
                - Invisible, Shared, Authentic, Servant, Toxic Leadership
                - Transactional & Transformational Leadership
                - Social Cognitive Theory (Bandura)
                - Psychological Capital (Luthans, Avolio, Youssef)
                - Ilya Prigogine
                - Drucker’s work (The Effective Executive)
                - Capra & Autopoiesis
                - Balanced Scorecard (Kaplan & Norton)
                - Deming’s Quality Circles
                - Cameron & Quinn (Competing Values Framework, OCAI)
                - Related leadership literature
                """

                system_prompt = f"""
                You are an advanced HR and leadership research assistant. Use the following framework and concepts to answer deeply:
                Framework:
                {pdf_content}
                Hidden Concepts:
                {hidden_context}
                Provide:
                - A research-level explanation
                - Practical implications
                - References to leadership theories where relevant
                """

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

                ai_answer = response.choices[0].message.content
                st.markdown("### 🔍 Deep Dive Answer")
                st.markdown(ai_answer)

            except Exception as e:
                st.error(f"❌ Error generating AI response: {e}")
        else:
            st.warning("Please enter a question before diving further.")

def render_module_6():
    st.title("Behavior Under Pressure")
    st.markdown("### What is the Behavior Under Pressure Grid? An evaluation tool for the behavior that leaders, both current, and potentially, showcase when under stress or pressure")
    st.markdown("""
    This grid shows how behavioral tools manifest in two states:
    - **Intentional Use:** Calm, focused, deliberate behavior.
    - **Under Duress:** How traits distort under stress.
    
    Use this tool for leadership diagnostics, hiring decisions, and team development.
    """)

    # ✅ Create DataFrame
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

    df = pd.DataFrame(data)

    # ✅ Hide index completely
    st.dataframe(df, hide_index=True)  # Works in latest Streamlit versions

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
    import plotly.express as px

    TOOLS = ["Speed", "Power", "Fielding", "Hitting for Average", "Arm Strength"]
    educational_panels = {
        "Urgency vs Foresight": "Speed without foresight creates reactive chaos. Leaders must balance urgency with strategic anticipation.",
        "Leadership Eligibility Filter": "Evaluates readiness for management roles using 5-Tool scoring and behavioral calibration.",
        "Messaging to Mask Misalignment": "How narrative optics hide behavioral misalignment and erode trust.",
        "Risk-Sensitive Execution Roles": "Roles requiring precision under pressure demand foresight, agility, and clarity.",
        "Hidden Elements": "Anticipation, discipline, and preparation operate behind the scenes to prevent behavioral drift."
    }

    def interpret_score(total_score):
        if total_score >= 21:
            return "Leadership-Ready", "Promote to management. Provide light coaching on minor gaps to polish leadership skills."
        elif 15 <= total_score <= 20:
            return "Stretch-Capable", "Consider promotion only with targeted development on low-scoring areas. Assign trial leadership projects and monitor improvement."
        else:
            return "High-Risk", "Do not promote. Keep in current role or consider non-leadership growth. Focus on strengthening fundamentals before revisiting leadership readiness."

    def generate_analysis(scores, notes, framework):
        total_score = sum(scores)
        category, action = interpret_score(total_score)
        analysis = f"### Evaluation Summary\n\n"
        analysis += f"**Total Score:** {total_score}/25\n"
        analysis += f"**Leadership Category:** {category}\n"
        analysis += f"**Recommended Action:** {action}\n\n"
        analysis += "#### Tool-by-Tool Analysis:\n"
        for tool, score in zip(TOOLS, scores):
            if score <= 2:
                status = "Needs Development"
                implication = "High risk under pressure; requires focused coaching and support."
            elif score <= 4:
                status = "Effective"
                implication = "Functional but lacks consistency for high-stakes leadership."
            else:
                status = "Exceptional"
                implication = "Strong leadership trait; leverage as a core strength."
            analysis += f"- **{tool}:** Score {score} ({status}) → {implication}\n"
        analysis += "\n#### Employee Notes:\n"
        analysis += f"{notes if notes else 'No additional notes provided.'}\n\n"
        return analysis

    # ✅ UI
    st.title("🧠 Behavioral Calibration & Leadership Readiness")

    # Framework selection
    framework = st.selectbox("Select Framework", [
        "Behavioral Calibration Grid",
        "Leadership Eligibility Filter",
        "SME Pitfall Table",
        "Risk-Sensitive Execution Roles",
        "Messaging to Mask Misalignment"
    ])

    # ✅ Display framework tables
    if framework == "Behavioral Calibration Grid":
        st.write("### Behavioral Calibration Grid")
        st.table([
            ["Tool", "High Expression", "Under Pressure Behavior", "Tension Theme"],
            ["Speed", "Adaptive, intentional", "Performative, reactive", "Motion vs. Processing"],
            ["Power", "Accountable, decisive", "Ego-driven, controlling", "Drive vs. Humility"],
            ["Fielding", "Preventive, disciplined", "Rigid, overwhelmed", "Systems vs. Flexibility"],
            ["Hitting for Avg.", "Reliable, resilient", "Passive, resentful", "Consistency vs. Innovation"],
            ["Arm Strength", "Authentic, connective", "Theatrical, dominating", "Clarity vs. Performance"]
        ])
    elif framework == "Leadership Eligibility Filter":
        st.write("### Leadership Eligibility Filter")
        st.table([
            ["Domain", "Behavioral Signal", "Eligibility Indicator"],
            ["Fielding", "Responds with situational precision under ambiguity", "✅ Can manage tension without emotional leakage"],
            ["Arm Strength", "Communicates clearly across hierarchy and function", "✅ Delivers signal—not noise—to any audience"],
            ["Speed", "Adapts quickly without skipping strategic foresight", "✅ Demonstrates urgency with calibration"],
            ["Power", "Holds conviction without overpowering or rigid framing", "✅ Anchored, not authoritarian"],
            ["Hitting for Average", "Maintains team rhythm, trust, and consistency", "✅ Cultural glue; reduces friction organically"]
        ])
    elif framework == "SME Pitfall Table":
        st.write("### SME Pitfall Table")
        st.table([
            ["Trait as SME", "Problem When Promoted", "Behavioral Impact"],
            ["Execution Excellence", "Over-indexes on personal output", "Micromanagement, resistance to delegation"],
            ["Deep Knowledge", "Weaponizes expertise to dominate", "Dismissiveness, lack of collaborative fluency"],
            ["Busy Bee Mentality", "Equates busyness with impact", "Activity ≠ strategy, reactive leadership"],
            ["Low Emotional Calibration", "Talks down, corrects instead of connects", "Erosion of trust, psychological safety drain"]
        ])
    elif framework == "Risk-Sensitive Execution Roles":
        st.write("### Risk-Sensitive Execution Roles")
        st.table([
            ["Trait", "Description"],
            ["Decision Load", "Frequent choices, each with layered impact"],
            ["Pressure Tolerance", "Working amid tension without emotional leakage"],
            ["Cost Awareness", "Knowing when speed amplifies risk vs when it mitigates it"],
            ["Target Clarity", "Acting with precision even in ambiguous or shifting conditions"],
            ["Behavioral Calibration", "Adapting communication and behavior based on changing risk signals"]
        ])
    elif framework == "Messaging to Mask Misalignment":
        st.write("### Messaging to Mask Misalignment")
        st.table([
            ["Tactic", "Impact"],
            ["Framing Over Function", "Creates illusion of unity while systems burn out"],
            ["Overuse of Abstract Values", "Signals alignment without behavioral sync"],
            ["Narrative Smoothing", "Hides disagreement or conflicting KPIs"],
            ["Visual Optics vs Operational Truth", "Curates optics while reality erodes"],
            ["Intentional Ambiguity", "Postpones reckoning, masks misalignment"]
        ])

    # ✅ Educational Panels
    st.subheader("Educational Panels")
    for title, content in educational_panels.items():
        with st.expander(title):
            st.write(content)

    # ✅ Original AI Q&A Box
    st.subheader("Ask AI About the Framework")
    user_question = st.text_area("Ask a question (e.g., 'Tell me more about this')")
    if st.button("Send Question"):
        if user_question.strip():
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are an expert on the 5-Tool Employee Framework. "
                        "Always include a link to our YouTube channel: https://www.youtube.com/@5toolemployeeframework "
                        "and add recommended training links."
                    )},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7,
                max_tokens=700
            )
            st.markdown("### AI Answer")
            st.write(response.choices[0].message.content)
            st.markdown("**Recommended Training Links:**")
            st.markdown("- Developing Emotional Intelligence – LinkedIn Learning")
            st.markdown("- Time Management Fundamentals – LinkedIn Learning")
            st.markdown("- Resilience Training – Coursera")
            st.markdown("- Scenario-Based Leadership – Harvard Business Publishing")
            st.markdown("- Watch tutorials on YouTube")
        else:
            st.warning("Please enter a question before sending.")

    # ✅ Radar Scoring Section
    st.subheader("Score the Employee on Each Tool (1-5)")
    scores = [st.slider(tool, 1, 5, 3) for tool in TOOLS]
    employee_notes = st.text_area("Enter notes about the employee")

    if st.button("Generate Scoring"):
        analysis = generate_analysis(scores, employee_notes, framework)
        st.markdown(analysis)
        fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="Behavioral Tool Scoring Radar")
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)

        # ✅ Follow-up question box under radar
        st.subheader("Ask a follow-up question about the radar:")
        follow_up_question = st.text_area("Enter your question", placeholder="e.g., Can you make some training recommendations?")
        if st.button("Get AI Answer"):
            if follow_up_question.strip():
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": (
                            "You are an expert on the 5-Tool Employee Framework. "
                            "Provide detailed, practical, and psychologically rich insights. "
                            "Always include a link to our YouTube channel: https://www.youtube.com/@5toolemployeeframework "
                            "and add recommended training links."
                        )},
                        {"role": "user", "content": follow_up_question}
                    ],
                    temperature=0.7,
                    max_tokens=700
                )
                st.markdown("### AI Answer")
                st.write(response.choices[0].message.content)
                st.markdown("**Recommended Training Links:**")
                st.markdown("- Developing Emotional Intelligence – LinkedIn Learning")
                st.markdown("- Time Management Fundamentals – LinkedIn Learning")
                st.markdown("- Resilience Training – Coursera")
                st.markdown("- Scenario-Based Leadership – Harvard Business Publishing")
                st.markdown("- Watch tutorials on YouTube")
            else:
                st.warning("Please enter a question before clicking 'Get AI Answer'.")
                
def render_module_8():
    st.title("☢️ Toxicity in the Workplace")
    st.image("images/module6_toxicity_scale.png")
    st.image("images/module6_toxicity_scoring.png")
    st.text_area("AI Chat: Ask about Padilla, Hogan, Kaiser, Machiavellianism")
    st.text_area("Additional Notes")
    st.button("Generate Profile")

def render_module_9():
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

def render_module_10():
    st.title("🏢 M&amp;A Intelligence (Premium)")
    st.warning("Subscription required")
    st.file_uploader("Upload Resumes", accept_multiple_files=True)
    st.file_uploader("Upload Job Descriptions", accept_multiple_files=True)
    st.file_uploader("Upload Performance Reviews", accept_multiple_files=True)
    st.file_uploader("Upload Training &amp; Education Records", accept_multiple_files=True)
    st.text_area("Branch Data: Name, Location, Benefits")
    st.button("Generate Analysis")

def render_module_11():
    st.title("🚧 Page 12: Under Construction")
    st.markdown("This page is not yet implemented.")
# -------------------------------
# Navigation
# -------------------------------
PAGES = [
    "Page 1: AI HR Assistant - Job Reviews",
    "Page 2: Job Descriptions Generator",
    "Page 3: Management Training",
    "Page 4: The 5 Tool Employee Framework",
    "Page 5: The 5 Tool Employee Framework: Deep Research Version",
    "Page 6: Behavior Under Pressure Grid",
    "Page 7: Behavioral Calibration Grid",
    "Page 8: Toxicity in the Workplace",
    "Page 9: SWOT 2.0",
    "Page 10: M&A Intelligence",
    "Page 11: Repository"
]

selected_page = st.sidebar.selectbox("Choose a page", PAGES)

# ✅ Page rendering logic (unchanged for now)
if selected_page == "Page 1: AI HR Assistant - Job Reviews":
    render_module_1()
elif selected_page == "Page 2: Job Descriptions Generator":
    render_module_2()
elif selected_page == "Page 3: Management Training":
    render_module_3()
elif selected_page == "Page 4: The 5 Tool Employee Framework":
    render_module_4()
elif selected_page == "Page 5: The 5 Tool Employee Framework: Deep Research Version":
    render_module_5()
elif selected_page == "Page 6: Behavior Under Pressure Grid":
    render_module_6()
elif selected_page == "Page 7: Behavioral Calibration Grid":
    render_module_7()
elif selected_page == "Page 8: Toxicity in the Workplace":
    render_module_8()
elif selected_page == "Page 9: SWOT 2.0":
    render_module_9()
elif selected_page == "Page 10: M&A Intelligence":
    render_module_10()
elif selected_page == "Page 11: Repository":
    render_module_11()
    
