# -------------------------------
# Imports
# -------------------------------
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from openai import OpenAI
from googleapiclient.discovery import build
import json

# ----------------------------
# Persistent Prompt Tracking
# ----------------------------
PROMPT_FILE = "prompt_usage.json"

def load_prompt_usage():
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r") as f:
            return json.load(f)
    return {}

def save_prompt_usage(data):
    with open(PROMPT_FILE, "w") as f:
        json.dump(data, f)
# ----------------------------
# Premium Upgrade Helper
# ----------------------------
def upgrade_to_premium():
    usage[user_id]["premium"] = True
    save_prompt_usage(usage)
    st.success("✅ Premium activated! Unlimited prompts and repository access.")
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
# ✅ Prompt limit setup
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

MAX_PROMPTS = 5  # Free tier limit
# ----------------------------
# Persistent User Tracking
# ----------------------------
user_id = "demo_user@example.com"  # Replace with actual login email later
usage = load_prompt_usage()
if user_id not in usage:
    usage[user_id] = {"count": 0, "month": "2025-11", "premium": False}

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

prompt = f"""
You are an organizational psychologist using the Five-Tool Employee Framework.
Interpret the following profile:

Context: {context_label}
Tools: {', '.join(tools)}
Scores: {scores}
Notes: {notes}

Instructions:
- Begin with a **Behavioral Summary** that ties together patterns across tools.
- For each tool, provide:
  • Expression at this score (how it shows up day-to-day)
  • Under-pressure risk (how it distorts under stress)
  • Calibration/Training (specific interventions to sustain impact)
- Explicitly weave in the framework’s tension themes:
  • Motion vs. Processing
  • Drive vs. Humility
  • Systems vs. Flexibility
  • Consistency vs. Innovation
  • Clarity vs. Performance
- End with a **Leadership Readiness Signal** and **Next 90-Day Interventions**.
- Tone: psychologically rich, diagnostic, and grounded in the model. Avoid generic corporate phrasing.
"""

# -------------------------------
# Subscription Logic
# -------------------------------
PAID_PAGES = {
    "Page 6: Repository": "$9.99/mo"
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

    # Build the prompt inside the function
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

    # Check prompt limit  
    if not usage[user_id]["premium"] and usage[user_id]["count"] >= MAX_PROMPTS:
        st.warning("🚫 You have reached your free limit of 5 prompts this month. Upgrade to premium for unlimited access.")
        if st.button("Upgrade to Premium ($9.99/month)"):
            upgrade_to_premium()
    else:
        # After generating AI response:
        usage[user_id]["count"] += 1
        save_prompt_usage(usage)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a workplace analyst writing realistic job reviews for professionals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            st.session_state.prompt_count += 1
            review_text = response.choices[0].message.content
            st.markdown("### 🧾 Realistic Job Review")
            st.write(review_text)

        except Exception as e:
            st.error(f"❌ Error generating review: {e}")
# -------------------------------
# ✅ Module 1 Wrapper
# -------------------------------
def render_module_1():
    # ✅ Title and Intro
    st.title("The 5 Tool Employee Framework")
    st.markdown("### _Introduction into the 5 Tool Employee Framework_")
    st.markdown("An Interchangeable Model. Finding the Right Fit.")

    # ✅ Framework Section
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
      Just like hitting is fundamental for a baseball player, mastering core skills is crucial for a professional.
    - 🛡 **Fielding → Problem-Solving Ability**  
      A great fielder reacts quickly and prevents errors—just like a skilled problem solver.
    - ⚡ **Speed → Adaptability & Continuous Learning**  
      Speed gives a player a competitive edge; adaptability ensures professionals stay relevant.
    - 💪 **Arm Strength → Communication & Leadership**  
      A powerful arm makes impactful plays—just like effective communication drives team success.
    - 🚀 **Power → Strategic Decision-Making**  
      Power hitters change the game—just like leaders who make high-impact decisions.
    """)

    st.markdown("---")

    # ✅ Chatbox Section
    st.subheader("🤖 Ask AI About the Framework")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("Ask a question (e.g., 'Tell me more about hitting for average', 'Explain adaptability')")

    if st.button("Send Question"):
        if user_question.strip():
            # ✅ Rich descriptive answers based on question keywords
            q_lower = user_question.lower()
            if "hitting" in q_lower or "technical" in q_lower:
                ai_answer = """
                **Hitting for Average → Technical Competence**
                This tool represents a professional’s ability to perform job-specific duties effectively and consistently.
                - **Why It Matters:** Without strong technical fundamentals, everything else suffers.
                - **Behavioral Insight:** High scores indicate rhythm and repeatability under pressure; low scores often signal avoidance of ambiguity or over-reliance on routine.
                - **Development Path:** Build structured training plans, reinforce accountability, and encourage precision under stress.
                """
            elif "fielding" in q_lower or "problem" in q_lower:
                ai_answer = """
                **Fielding → Problem-Solving Ability**
                A great fielder anticipates and adjusts—just like a skilled problem solver who diagnoses inefficiencies early.
                - **Why It Matters:** Prevents chaos and costly errors.
                - **Behavioral Insight:** High scores show foresight and composure; low scores reveal rigidity or blame-shifting.
                - **Development Path:** Scenario planning and root-cause analysis training.
                """
            elif "speed" in q_lower or "adaptability" in q_lower:
                ai_answer = """
                **Speed → Adaptability & Continuous Learning**
                Speed in business means agility and learning under pressure.
                - **Why It Matters:** Keeps employees relevant in fast-changing environments.
                - **Behavioral Insight:** High scores reflect emotional agility and proactive learning; low scores suggest resistance to change.
                - **Development Path:** Micro-learning programs and resilience coaching.
                """
            elif "arm" in q_lower or "communication" in q_lower:
                ai_answer = """
                **Arm Strength → Communication & Leadership**
                Communication drives clarity and influence across teams.
                - **Why It Matters:** Aligns stakeholders and builds trust.
                - **Behavioral Insight:** High scores show authentic leadership; low scores risk optics-driven behavior or dominance.
                - **Development Path:** Coaching on clarity, empathy, and feedback loops.
                """
            elif "power" in q_lower or "strategic" in q_lower:
                ai_answer = """
                **Power → Strategic Decision-Making**
                Power is about foresight and decisive action.
                - **Why It Matters:** Shapes long-term success and prevents costly missteps.
                - **Behavioral Insight:** High scores indicate confidence with humility; low scores reveal impulsiveness or short-term thinking.
                - **Development Path:** Strategic frameworks and risk analysis training.
                """
            else:
                ai_answer = """
                The 5 Tool Employee Framework evaluates five core skills:
                - Technical Competence
                - Problem-Solving Ability
                - Adaptability & Continuous Learning
                - Communication & Leadership
                - Strategic Decision-Making
                Ask about any tool for a detailed explanation.
                """
            st.session_state.chat_history.append((user_question, ai_answer.strip()))
        else:
            st.warning("Please enter a question before sending.")

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
    TOOLS = [
        "Technical Competence",
        "Problem-Solving Ability",
        "Adaptability & Continuous Learning",
        "Communication & Leadership",
        "Strategic Decision-Making"
    ]
    scores = [st.slider(tool, 1, 10, 5) for tool in TOOLS]

    # ✅ Generate Profile Button
    if st.button("Generate 5 Tool Employee"):
        if notes_input.strip():
            st.markdown("### 🧠 Your Custom 5 Tool Employee Profile")

            for tool, score in zip(TOOLS, scores):
                st.markdown(f"**{tool} (Score: {score}/10)**")

                # ✅ Detailed interpretation based on your book
                if score <= 3:
                    st.write("- **Behavioral Reality:** Needs Development.")
                    if tool == "Technical Competence":
                        st.write("  • Misses execution rhythm; avoids ambiguity; may disengage under pressure.")
                        st.write("  • Risk: Reliability gaps erode trust and team cadence.")
                        st.write("  • Development: Structured technical training and accountability systems.")
                    elif tool == "Problem-Solving Ability":
                        st.write("  • Reactive firefighting; freezes or blames others when overwhelmed.")
                        st.write("  • Risk: Creates chaos instead of solutions.")
                        st.write("  • Development: Build analytical discipline and scenario planning.")
                    elif tool == "Adaptability & Continuous Learning":
                        st.write("  • Resistant to change; lacks proactive learning habits.")
                        st.write("  • Risk: Falls behind in dynamic environments.")
                        st.write("  • Development: Micro-learning and resilience coaching.")
                    elif tool == "Communication & Leadership":
                        st.write("  • Communication lacks clarity; influence minimal.")
                        st.write("  • Risk: Team misalignment and low morale.")
                        st.write("  • Development: Authentic leadership coaching and feedback loops.")
                    elif tool == "Strategic Decision-Making":
                        st.write("  • Decisions lack foresight; may chase optics over substance.")
                        st.write("  • Risk: High chance of costly missteps under pressure.")
                        st.write("  • Development: Train in strategic frameworks and risk analysis.")
                elif score <= 6:
                    st.write("- **Behavioral Reality:** Effective but inconsistent.")
                    st.write("  • Strength: Handles routine tasks and moderate complexity.")
                    st.write("  • Growth Area: Needs calibration for high-pressure scenarios.")
                    st.write("  • Development Path: Reinforce rhythm and foresight through structured coaching.")
                else:
                    st.write("- **Behavioral Reality:** Exceptional.")
                    st.write("  • Strength: Demonstrates mastery under pressure; inspires confidence.")
                    st.write("  • Watch Out: Overuse can drift into dysfunction (e.g., dominance, rigidity).")
                    st.write("  • Development Path: Maintain humility and balance; leverage as a leadership strength.")

                st.markdown("---")

            # ✅ Notes Section
            st.markdown("**Notes:**")
            st.write(notes_input)

            # ✅ Radar Chart Visualization
            st.subheader("📊 5-Tool Employee Profile Radar")
            fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="5-Tool Employee Radar Chart")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)
        else:
            st.warning("Please add notes before generating the profile.")

    # ✅ Clear History Button
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.experimental_rerun()
    # ✅ After generating the profile and radar chart
    if st.button("Save to Repository"):
        st.session_state["saved_notes"] = notes_input if "notes_input" in locals() else st.session_state.get("saved_notes", "")
        st.session_state["saved_scores"] = scores if "scores" in locals() else st.session_state.get("saved_scores", "")
        st.session_state["saved_review"] = "Your 5-Tool Employee Profile"
        st.success("✅ Work saved! Go to Page 6 (Repository) to download or organize.")
        
def render_module_2():
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
    Behavioral Insight: Psychoal agility is the governor here—not raw reaction speed. Sustainable performance depends on metabolizing tension, not just masking it.
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
                - Psychoal Capital (Luthans, Avolio, Youssef)
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
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": question}, 
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                st.session_state.prompt_count += 1 
                ai_answer = response.choices[0].message.content
                st.markdown("### 🔍 Deep Dive Answer")
                st.markdown(ai_answer)

            except Exception as e:
                st.error(f"❌ Error generating AI response: {e}")
        else:
            st.warning("Please enter a question before diving further.")
    # ✅ After generating the profile and radar chart
    if st.button("Save to Repository"):
        st.session_state["saved_notes"] = notes_input if "notes_input" in locals() else st.session_state.get("saved_notes", "")
        st.session_state["saved_scores"] = scores if "scores" in locals() else st.session_state.get("saved_scores", "")
        st.session_state["saved_review"] = "Your 5-Tool Employee Profile"
        st.success("✅ Work saved! Go to Page 6 (Repository) to download or organize.")
def render_module_3():
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
    if st.button("Generate Insights"):
        if user_comments.strip():
            st.subheader("🔍 AI Insights Based on Your Comments")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an organizational psychologist analyzing behavior under pressure."},
                {"role": "user", "content": f"Analyze this comment in context of the Behavior Under Pressure Grid: {user_comments}"} 
                ], 
                temperature=0.7,
                max_tokens=400
            )
            st.session_state.prompt_count += 1 
            st.write(response.choices[0].message.content)
        else:
            st.warning("Please add comments before generating insights.")
    # ✅ After generating the profile and radar chart
    if st.button("Save to Repository"):
        st.session_state["saved_notes"] = notes_input if "notes_input" in locals() else st.session_state.get("saved_notes", "")
        st.session_state["saved_scores"] = scores if "scores" in locals() else st.session_state.get("saved_scores", "")
        st.session_state["saved_review"] = "Your 5-Tool Employee Profile"
        st.success("✅ Work saved! Go to Page 6 (Repository) to download or organize.")          
def render_module_4():
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
            ["Low Emotional Calibration", "Talks down, corrects instead of connects", "Erosion of trust, psychoal safety drain"]
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
                model="gpt-4o-mini",
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
            st.session_state.prompt_count += 1  
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
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": (
                            "You are an expert on the 5-Tool Employee Framework. "
                            "Provide detailed, practical, and psychoally rich insights. "
                            "Always include a link to our YouTube channel: https://www.youtube.com/@5toolemployeeframework "
                            "and add recommended training links."
                        )},
                        {"role": "user", "content": follow_up_question} 
                    ],
                    temperature=0.7,
                    max_tokens=700
                )
                st.session_state.prompt_count += 1 
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
    # ✅ After generating the profile and radar chart
    if st.button("Save to Repository"):
        st.session_state["saved_notes"] = notes_input if "notes_input" in locals() else st.session_state.get("saved_notes", "")
        st.session_state["saved_scores"] = scores if "scores" in locals() else st.session_state.get("saved_scores", "")
        st.session_state["saved_review"] = "Your 5-Tool Employee Profile"
        st.success("✅ Work saved! Go to Page 6 (Repository) to download or organize.")        
def render_module_5():
    import streamlit as st
    import plotly.express as px
    from openai import OpenAI
    import os

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # --- Helper: AI response for general questions ---
    def get_ai_response(question):
        system_prompt = """
        You are an expert in organizational psychology and leadership.
        Provide a structured response in this format:
        **Explanation:** Summary of the concept.
        **Detail:** Key insights and why it matters.
        **Practical Tips:** Actionable steps for real-world application.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": contextual_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=700
        )
        st.session_state.prompt_count += 1 
        return response.choices[0].message.content

    # --- Helper: Contextual Insight combining notes and score ---
    def get_contextual_insight(notes, score, risk_level):
        contextual_prompt = f"""
        Analyze this scenario:
        Notes: {notes}
        Numeric Score: {score}
        Risk Level: {risk_level}

        Determine if notes indicate toxic intent or cultural risk even if numeric score suggests low risk.
        Provide:
        **Contextual Insight:** Explain toxicity risk based on notes.
        **Recommendation:** Suggest actions considering both score and notes.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in leadership assessment and organizational culture."},
                {"role": "user", "content": contextual_prompt} # ✅ prompt exists here
            ],
            temperature=0.7,
            max_tokens=500
        )
        st.session_state.prompt_count += 1  
        return response.choices[0].message.content

    # --- UI Layout ---
    st.title("☢️ Toxicity in the Workplace")

    # Educational Expanders
    with st.expander("Padilla’s Toxic Triangle"):
        st.write("Destructive Leaders, Susceptible Followers, and Conducive Environments create toxic conditions.")
    with st.expander("Hogan’s Dark Side Derailers"):
        st.write("Traits like Arrogance, Volatility, and Manipulativeness can derail leadership effectiveness.")
    with st.expander("Machiavellianism & Dark Triad"):
        st.write("Machiavellianism, Narcissism, and Psychopathy are key indicators of toxic tendencies.")
    with st.expander("Behavioral Drift & 360-Degree Feedback"):
        st.write("Behavioral drift occurs when employees gradually deviate from norms; 360-degree feedback helps detect early signs.")

    # Detailed Rubric Table
    st.subheader("Toxicity Rubric")
    st.markdown("""
    <table style='width:100%; border:1px solid black; font-size:14px;'>
    <tr><th>Tool</th><th>Low Risk (3-4)</th><th>Moderate Risk (2)</th><th>High Risk (1)</th><th>Toxicity Triggers</th></tr>
    <tr><td>Speed</td><td>Adapts quickly; integrates feedback without ego.</td><td>Slow to adapt; reacts impulsively.</td><td>Freezes or disengages; ignores feedback.</td><td>Erratic decisions under pressure; volatility derailer.</td></tr>
    <tr><td>Power</td><td>Owns outcomes; decisive and humble.</td><td>Hesitates; deflects blame occasionally.</td><td>Blames others; manipulates responsibility.</td><td>Arrogance derailer; shirking accountability.</td></tr>
    <tr><td>Fielding</td><td>Anticipates risks; builds robust systems.</td><td>Misses risks; rigid under stress.</td><td>Ignores risks; fosters chaos.</td><td>Unchecked risk-taking; overconfidence derailer.</td></tr>
    <tr><td>Hitting for Average</td><td>Delivers consistently; builds trust.</td><td>Inconsistent; skips documentation.</td><td>Silent quitting; erodes trust.</td><td>Detachment derailer; cultural drift.</td></tr>
    <tr><td>Arm Strength</td><td>Communicates clearly; inspires buy-in.</td><td>Dominates or charms without substance.</td><td>Manipulative; dismisses feedback.</td><td>Divisive communication; manipulativeness derailer.</td></tr>
    </table>
    """, unsafe_allow_html=True)

    # AI Chat
    st.subheader("AI Chat: Ask about Toxic Leadership or Feedback")
    ai_question = st.text_area("Ask a question (e.g., Tell me more about 360-degree feedback)")
    if st.button("Get AI Response"):
        st.markdown(get_ai_response(ai_question))

    # Scoring Sliders
    st.subheader("Rate the Employee on Each Dimension")
    speed = st.slider("Speed", 1, 5, 3)
    power = st.slider("Power", 1, 5, 3)
    fielding = st.slider("Fielding", 1, 5, 3)
    hitting = st.slider("Hitting for Average", 1, 5, 3)
    arm_strength = st.slider("Arm Strength", 1, 5, 3)

    notes = st.text_area("Additional Notes")

    # Generate Profile
    if st.button("Generate Profile"):
        total_score = speed + power + fielding + hitting + arm_strength
        if total_score >= 15:
            risk_level = "Low Risk"
            action_plan = "Retain and support; encourage continued engagement."
        elif 10 <= total_score < 15:
            risk_level = "Moderate Risk"
            action_plan = "Provide coaching and monitor closely for improvement."
        else:
            risk_level = "High Risk"
            action_plan = "Immediate intervention required; consider reassignment or exit strategy."

        st.write(f"**Total Score:** {total_score}")
        st.write(f"**Risk Level:** {risk_level}")
        st.write(f"**Action Plan:** {action_plan}")

        # Radar Chart
        categories = ["Speed", "Power", "Fielding", "Hitting", "Arm Strength"]
        scores = [speed, power, fielding, hitting, arm_strength]
        fig = px.line_polar(r=scores, theta=categories, line_close=True)
        fig.update_traces(fill='toself')
        fig.update_layout(title="Toxicity Profile Radar Chart")
        st.plotly_chart(fig)

        # Interpretation Table
        st.markdown("""
        <h4>Total Score Interpretation</h4>
        <table style='width:100%; border:1px solid black;'>
        <tr><th>Score Range</th><th>Risk Level</th><th>Description</th></tr>
        <tr><td>15-20</td><td>Low Risk</td><td>Employee demonstrates strong alignment with organizational values.</td></tr>
        <tr><td>10-14</td><td>Moderate Risk</td><td>Employee shows signs of disengagement or minor toxic behaviors.</td></tr>
        <tr><td>Below 10</td><td>High Risk</td><td>Immediate intervention required; behaviors are harmful to team culture.</td></tr>
        </table>
        """, unsafe_allow_html=True)

        # AI Insights
        st.subheader("AI Insights")
        st.markdown(get_ai_response("toxicity in workplace"))

        # Contextual Insight
        if notes.strip():
            st.subheader("Contextual Insight")
            st.markdown(get_contextual_insight(notes, total_score, risk_level))

import streamlit as st
import random
import pandas as pd

# --- AI + Web Insights Simulation ---
# In real implementation, these would call an AI model and integrate web-scraped insights.
# For now, we'll simulate with blended  from user notes and industry best practices.

def generate_ai_swot(notes, ai_chat):
    """Generate SWOT bullet points based on user notes and web insights."""
    user_strengths = [
        "Strong engineering expertise and leadership",
        "New hire brings extensive industry connections",
        "Ability to deliver complex coding projects quickly"
    ]
    user_weaknesses = [
        "Potential cultural disruption due to salary disparity",
        "Over-reliance on one individual for core coding tasks",
        "Risk of burnout among existing engineers"
    ]
    web_strengths = [
        "High demand for senior engineers positions company competitively",
        "Hybrid team structures reduce burnout and improve delivery"
    ]
    web_weaknesses = [
        "Salary gaps can lead to morale issues and attrition",
        "Limited succession planning increases vulnerability"
    ]
    web_opportunities = [
        "Upskilling programs can boost retention and engagement",
        "Leverage new hire's network for strategic partnerships",
        "Adopt automation tools to reduce workload on engineers"
    ]
    web_threats = [
        "Competitors exploiting instability during transition",
        "Client dissatisfaction if onboarding disrupts service",
        "Industry salary inflation increasing cost pressures"
    ]

    strengths = user_strengths + web_strengths
    weaknesses = user_weaknesses + web_weaknesses
    opportunities = web_opportunities
    threats = web_threats

    return strengths, weaknesses, opportunities, threats

# Weighted scoring logic
weights = {"Impact": 0.4, "Feasibility": 0.3, "Urgency": 0.2, "Confidence": 0.1}

def score_factor():
    return {criterion: random.randint(1, 5) for criterion in weights}

def calculate_weighted_score(scores):
    return sum(scores[c] * weights[c] for c in weights)

# Generate roadmap from top-ranked items
def generate_roadmap(df):
    roadmap = []
    top_items = df.sort_values(by="Total Score", ascending=False).head(5)
    for _, row in top_items.iterrows():
        factor = row["Factor"]
        category = row["Category"]
        roadmap.append({
            "Action": f"Address {category}: {factor}",
            "Milestone": "Complete initial implementation in 90 days",
            "Owner": "Cross-functional team",
            "Review Cycle": "Quarterly reassessment",
            "Best Case": "Improved team stability and client satisfaction",
            "Worst Case": "Attrition increases, delays in delivery",
            "Pivot Strategy": "Reallocate resources and accelerate upskilling"
        })
    return pd.DataFrame(roadmap)

# --- Streamlit UI ---
    # ✅ After generating the profile and radar chart
    if st.button("Save to Repository"):
        st.session_state["saved_notes"] = notes_input if "notes_input" in locals() else st.session_state.get("saved_notes", "")
        st.session_state["saved_scores"] = scores if "scores" in locals() else st.session_state.get("saved_scores", "")
        st.session_state["saved_review"] = "Your 5-Tool Employee Profile"
        st.success("✅ Work saved! Go to Page 6 (Repository) to download or organize.")
def render_module_6():
    st.title("📂 Repository")
    if not usage[user_id]["premium"]:
        st.warning("This feature requires premium ($9.99/month).")
        if st.button("Upgrade to Premium"):
            upgrade_to_premium()
    else:
        st.success("Premium active! Save your work below.")

        # Show captured data
        st.write("### Your Current Work")
        st.write("Notes:", st.session_state.get("saved_notes", "No notes yet"))
        st.write("Scores:", st.session_state.get("saved_scores", "No scores yet"))
        st.write("Review:", st.session_state.get("saved_review", "No review yet"))

        # Save Work Button
        if st.button("Save Work"):
            with open("saved_work.txt", "w") as f:
                f.write("Notes:\n" + str(st.session_state.get("saved_notes", "")) + "\n\n")
                f.write("Scores:\n" + str(st.session_state.get("saved_scores", "")) + "\n\n")
                f.write("Review:\n" + str(st.session_state.get("saved_review", "")))
            st.success("✅ Work saved successfully!")

        # Generate PDF Button
        if st.button("Generate PDF"):
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Your Saved Work", ln=True, align="C")
            pdf.multi_cell(0, 10, txt="Notes:\n" + str(st.session_state.get("saved_notes", "")))
            pdf.multi_cell(0, 10, txt="Scores:\n" + str(st.session_state.get("saved_scores", "")))
            pdf.multi_cell(0, 10, txt="Review:\n" + str(st.session_state.get("saved_review", "")))
            pdf.output("saved_work.pdf")
            with open("saved_work.pdf", "rb") as f:
                st.download_button("Download PDF", f, file_name="saved_work.pdf")
# -------------------------------
# Navigation
# -------------------------------
PAGES = [
    "Page 1: The 5 Tool Employee Framework",
    "Page 2: The 5 Tool Employee Framework: Deep Research Version",
    "Page 3: Behavior Under Pressure Grid",
    "Page 4: Behavioral Calibration Grid",
    "Page 5: Toxicity in the Workplace",
    "Page 6: Repository",
]

selected_page = st.sidebar.selectbox("Choose a page", PAGES)

# ✅ Page rendering logic (unchanged for now)
if selected_page == "Page 1: The 5 Tool Employee Framework":
    render_module_1()
elif selected_page == "Page 2: The 5 Tool Employee Framework: Deep Research Version":
    render_module_2()
elif selected_page == "Page 3: Behavior Under Pressure Grid":
    render_module_3()
elif selected_page == "Page 4: Behavioral Calibration Grid":
    render_module_4()
elif selected_page == "Page 5: Toxicity in the Workplace":
    render_module_5()
elif selected_page == "Page 6: Repository":
    render_module_6()
    
