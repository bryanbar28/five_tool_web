import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Five-Tool App", layout="wide")

# -------------------------------
# Session State Setup
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "initial_review" not in st.session_state:
    st.session_state.initial_review = ""
if "show_repository" not in st.session_state:
    st.session_state.show_repository = False
if "last_parse" not in st.session_state:
    st.session_state.last_parse = None

# -------------------------------
# OpenAI Client
# -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# SINGLE AI FUNCTION — ALL CHAT BOXES USE THIS
# -------------------------------
def ask_5tool(question: str, temperature=0.3):
    context = """
You are an expert consultant using Bryan Barrera’s 5-Tool Employee Framework from the book "Finding the Right Fit".
The five tools:
• Speed — Cognitive & Behavioral Agility
• Power — Ownership, Initiative & Decisiveness
• Fielding — Strategic Foresight & System Protection
• Hitting for Average — Reliability, Rhythm & Repeatability
• Arm Strength — Communication Reach & Influence

Always reference behavior under pressure, dysfunction signals, toxicity, leadership eligibility, behavioral drift, and systems thinking. Use baseball analogies when helpful.
Never give generic advice — stay grounded in the framework and the user’s input.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temperature,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ],
        max_tokens=900
    )
    return response.choices[0].message.content.strip()

# -------------------------------
# Business Description Parser
# -------------------------------
def parse_business_description(description: str):
    prompt = f"""
Extract ONLY valid JSON (no markdown):

{{
  "industry_primary": "e.g. Food & Beverage",
  "industry_subcategory": "e.g. Coffee Roasting",
  "company_size_employees": "1"|"2-10"|"11-50"|"51-200"|"201-1000"|"1000+",
  "company_size_revenue": "<1M"|"1-5M"|"5-20M"|"20-100M"|"100M+"|"Unknown",
  "location_city": string or null,
  "location_state": string or null,
  "business_model": "B2B"|"B2C"|"Marketplace"|"Subscription"|"Retail"|"Wholesale"|"Service"|"Other",
  "confidence_score": 1-10
}}

User description: "{description}"
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = resp.choices[0].message.content.strip()
        return json.loads(raw)
    except Exception as e:
        st.error(f"Parsing failed: {e}")
        return None

# -------------------------------
# API Keys – Replace with your actual values
# -------------------------------
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")  # Replace with your key if not in env
CHANNEL_ID = "YOUR_CHANNEL_ID"  # Replace with your actual channel ID

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
# Subscription Logic (Placeholder)
# -------------------------------
PAID_PAGES = {
    "Page 7: Repository": "$9.99/mo"
}
def is_unlocked(page):
    return True  # Set to False for real subscription; currently always unlocked for testing

def unlock_page(page, price):
    st.warning(f"This page requires a subscription: {price}")
    if st.button("Unlock Now"):
        st.success("Unlocked! (Demo)")

# -------------------------------
# Job Review Generator
# -------------------------------
def generate_job_review(role, notes=None):
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
        prompt += f"\nIncorporate these notes: {notes}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# -------------------------------
# Template Discovery
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

# -------------------------------
# Pages
# -------------------------------
def page_parser():
    st.title("Smart Business Parser")
    desc = st.text_area("Describe your business", height=120,
                        placeholder="e.g. my company is a small coffee roasting business in Portland")
    if st.button("Parse", type="primary"):
        if desc.strip():
            with st.spinner("Analyzing..."):
                result = parse_business_description(desc)
                if result:
                    st.session_state.last_parse = result
                    st.success("Done!")
    if "last_parse" in st.session_state:
        st.json(st.session_state.last_parse, expanded=True)

def page_1():
    render_template_discovery()
    st.title("The 5 Tool Employee Framework")
    st.markdown("### Introduction into the 5 Tool Employee Framework")
    st.markdown("An Interchangeable Model. Finding the Right Fit.")
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
- 🧤 **Fielding → Problem-Solving Ability**  
  A great fielder reacts quickly and prevents errors—just like a skilled problem solver.
- ⚡ **Speed → Adaptability & Continuous Learning**  
  Speed gives a player a competitive edge; adaptability ensures professionals stay relevant.
- 💪 **Arm Strength → Communication & Leadership**  
  A powerful arm makes impactful plays—just like effective communication drives team success.
- 🚀 **Power → Strategic Decision-Making**  
  Power hitters change the game—just like leaders who make high-impact decisions.
    """)
    st.markdown("---")
    st.subheader("Ask AI About the Framework")
    q = st.text_input("Ask anything (e.g., 'Tell me more about hitting for average')")
    if st.button("Send"):
        if q.strip():
            with st.spinner("Thinking..."):
                answer = ask_5tool(q)
            st.markdown(answer)
    st.subheader("Create Your Own 5 Tool Employee")
    notes_input = st.text_area("Enter notes about your ideal employee", placeholder="e.g., strong leadership, adaptable")
    st.subheader("Rate the Employee on Each Tool (1–10)")
    TOOLS = [
        "Technical Competence",
        "Problem-Solving Ability",
        "Adaptability & Continuous Learning",
        "Communication & Leadership",
        "Strategic Decision-Making"
    ]
    scores = [st.slider(tool, 1, 10, 5) for tool in TOOLS]
    if st.button("Generate 5 Tool Employee"):
        if notes_input.strip():
            st.markdown("### Custom 5 Tool Employee Profile")
            for tool, score in zip(TOOLS, scores):
                st.markdown(f"**{tool} (Score: {score}/10)**")
                # Interpretation (your original logic)
                if score <= 3:
                    st.write("- Needs Development")
                elif score <= 6:
                    st.write("- Effective but inconsistent")
                else:
                    st.write("- Exceptional")
                st.markdown("---")
            st.markdown("**Notes:**")
            st.write(notes_input)
            fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="5-Tool Radar")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)
        else:
            st.warning("Add notes first.")
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()

def render_module_2():
    import streamlit as st
    st.title("Advanced Deep Research — The 5 Tool Employee Framework")
    
    # ✅ SAME scrollable PDF content as before
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
    st.markdown(
        f"<div style='height:500px; overflow-y:auto; border:1px solid #ccc; padding:10px;'>{pdf_content}</div>",
        unsafe_allow_html=True
    )

    # ✅ SAME input box and button
    question = st.text_input("Ask a question about the framework:")
    
    if st.button("Dive Further"):
        if question.strip():
            q_lower = question.lower()

            # Intelligent keyword matching — same logic you loved from Module 1
            if any(word in q_lower for word in ["speed", "agility", "adapt", "learning"]):
                answer = """
**Speed — Cognitive & Behavioral Agility**  
**Natural Gift:** Pattern recognition, emotional agility, perceptual timing  
**High-Functioning:** Adjusts mid-motion with grace; communicates with precise cadence; integrates feedback without spiraling; creates momentum without overcomplication  
**Dysfunction Signals:** Impulsive reactions, mistakes urgency for depth, defaults to charisma, performs instead of processes  
**Behavioral Insight:** Sustainable performance depends on metabolizing tension, not masking it.  
**Where It Shows Up:** Change management, customer-facing roles, volatile executive communication, high-ambiguity individual contributors
                """
            elif any(word in q_lower for word in ["power", "ownership", "decis", "initiative"]):
                answer = """
**Power — Ownership, Initiative & Decisiveness**  
**Natural Gift:** Inner drive, conviction, will to close  
**High-Functioning:** Owns mission end-to-end, pushes progress without consensus, makes high-impact decisions others align behind, brings heat without burning bridges  
**Dysfunction Signals:** Bulldozes collaboration, hides behind motion, overuses authority, equates charisma with clarity  
**Behavioral Insight:** Unchecked Power erodes trust — humility is the limiter.  
**Where It Shows Up:** Founders, team leads, closers, high-pressure final-call roles
                """
            elif any(word in q_lower for word in ["fielding", "foresight", "risk", "system", "protect"]):
                answer = """
**Fielding — Strategic Foresight & System Protection**  
**Natural Gift:** Systems awareness, anticipatory thinking, stability  
**High-Functioning:** Spots second/third-order consequences early, builds guardrails, operates upstream of risk, stays composed in uncertainty  
**Dysfunction Signals:** Risk-averse/defensive, resists new data, rigid safeguards, blames others  
**Behavioral Insight:** Emotional maturity shows through discipline — people, not pressure, break systems.  
**Where It Shows Up:** Compliance, audit, legal, ops, strategic planning, QA, culture protectors
                """
            elif any(word in q_lower for word in ["hitting", "average", "reliab", "rhythm", "consistency"]):
                answer = """
**Hitting for Average — Reliability, Rhythm & Repeatability**  
**Natural Gift:** Execution discipline, operational precision, resilience  
**High-Functioning:** Delivers quietly and predictably under pressure, builds trust through consistency, anchors workflows, focuses on base hits  
**Dysfunction Signals:** Hides in routine, resents lack of recognition, over-indexes habit, mechanical task performance  
**Behavioral Insight:** Culture underrates the glue — rhythm beats reaction, trust beats tension. Recognition must find the quiet storm.  
**Where It Shows Up:** Ops, customer success, fulfillment, risk-sensitive execution, chaos-preventers
                """
            elif any(word in q_lower for word in ["arm", "strength", "communicat", "influence", "leadership"]):
                answer = """
**Arm Strength — Communication Reach & Influence**  
**Natural Gift:** Expressive clarity, emotional connection, presence  
**High-Functioning:** Distills vision into moving language, connects across hierarchies effortlessly, builds buy-in without overreaching  
**Dysfunction Signals:** Charms without substance, dominates conversation, masks misalignment, prioritizes performance over truth  
**Behavioral Insight:** Influence without clarity becomes theater — real communication reaches identity and belonging.  
**Where It Shows Up:** Sales, enablement, leadership, cross-functional translators, cultural brokers
                """
            else:
                answer = "Ask about one of the five tools (Speed, Power, Fielding, Hitting for Average, Arm Strength) for a full deep-research breakdown."

            st.markdown("### 🔍 Deep Dive Answer")
            st.markdown(answer)
        else:
            st.warning("Please enter a question before diving further.")
def render_module_3():
    st.title("Behavior Under Pressure")
    st.markdown("### What is the Behavior Under Pressure Grid? An evaluation tool for the behavior that leaders, both current, and potentially, showcase when under stress or pressure")
    st.markdown("""
    This grid shows how behavioral tools manifest in two states:
    - **Intentional Use:** Calm, focused, deliberate behavior.
    - **Under Duress:** How traits distort under stress.
   
    Use this tool for leadership diagnostics, hiring decisions, and team development.
    """)
    
    # ✅ SAME table
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
    st.dataframe(df, hide_index=True)

    # ✅ SAME input box
    comments = st.text_area("Add your comments or observations", placeholder="e.g., This candidate freezes under pressure but excels in planning.")

    if st.button("Generate Insights"):
        if comments.strip():
            c_lower = comments.lower()

            if any(word in c_lower for word in ["power", "own", "decis", "feedback", "overreach"]):
                insight = """
**Power Under Duress Analysis**  
When Power distorts under pressure:  
- Overreaches authority  
- Avoids feedback, deflects blame  
- Bulldozes collaboration  
- Hides behind motion instead of reflection  

**Diagnostic Insight:** This is ego-driven control. The individual equates volume with leadership.  
**Calibration Path:** Reinforce humility as the limiter. Practice structured feedback loops and ownership rituals (e.g., "What did I own today?").
                """
            elif any(word in c_lower for word in ["speed", "react", "perform", "deflect", "show"]):
                insight = """
**Speed Under Duress Analysis**  
When Speed distorts:  
- Reacts impulsively or performs for optics  
- Mistakes urgency for depth  
- Deflects instead of integrates feedback  

**Diagnostic Insight:** This is motion masquerading as progress — charisma over processing.  
**Calibration Path:** Train psychological agility: pause protocols, reflection rituals, and feedback integration drills.
                """
            elif any(word in c_lower for word in ["fielding", "freeze", "rigid", "block", "blame"]):
                insight = """
**Fielding Under Duress Analysis**  
When Fielding distorts:  
- Freezes or becomes defensive  
- Rigidifies safeguards, blocks learning  
- Blames others when overwhelmed  

**Diagnostic Insight:** Lack of emotional maturity under uncertainty — foresight fails when ego is threatened.  
**Calibration Path:** Build anticipatory thinking through scenario planning and upstream risk exercises.
                """
            elif any(word in c_lower for word in ["hitting", "average", "check out", "avoid", "change", "routine"]):
                insight = """
**Hitting for Average Under Duress Analysis**  
When Hitting distorts:  
- Checks out or hides in routine  
- Avoids stretch assignments  
- Resents lack of recognition  

**Diagnostic Insight:** Reliability breaks when ambiguity rises — the quiet storm goes silent.  
**Calibration Path:** Reinforce rhythm through consistency rituals and recognition of base hits.
                """
            elif any(word in c_lower for word in ["arm", "charm", "dominate", "mask", "clarity"]):
                insight = """
**Arm Strength Under Duress Analysis**  
When Arm Strength distorts:  
- Charms without substance  
- Dominates conversation  
- Uses messaging to mask misalignment  

**Diagnostic Insight:** Influence becomes theater — performance over truth.  
**Calibration Path:** Anchor communication in clarity and belonging, not optics.
                """
            else:
                insight = "Comment detected. Match found across multiple tools — consider full 5-Tool evaluation under pressure."

            st.markdown("### 🔍 Behavior Under Pressure Insights")
            st.markdown(insight)
        else:
            st.warning("Please add comments before generating insights.")         
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

    # SAME UI — 100% untouched
    st.title("Behavioral Calibration & Leadership Readiness")
    
    framework = st.selectbox("Select Framework", [
        "Behavioral Calibration Grid",
        "Leadership Eligibility Filter",
        "SME Pitfall Table",
        "Risk-Sensitive Execution Roles",
        "Messaging to Mask Misalignment"
    ])

    # SAME tables — unchanged
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
            ["Fielding", "Responds with situational precision under ambiguity", "Can manage tension without emotional leakage"],
            ["Arm Strength", "Communicates clearly across hierarchy and function", "Delivers signal—not noise—to any audience"],
            ["Speed", "Adapts quickly without skipping strategic foresight", "Demonstrates urgency with calibration"],
            ["Power", "Holds conviction without overpowering or rigid framing", "Anchored, not authoritarian"],
            ["Hitting for Average", "Maintains team rhythm, trust, and consistency", "Cultural glue; reduces friction organically"]
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

    st.subheader("Educational Panels")
    for title, content in educational_panels.items():
        with st.expander(title):
            st.write(content)

    # SAME Q&A — now AI-free, instant, smart
    st.subheader("Ask About the Framework")
    follow = st.text_area("Ask a follow-up")
    if st.button("Get Answer"):
        if follow.strip():
            q = follow.lower()
            if "eligibility" in q or "promot" in q or "ready" in q:
                answer = """
**Leadership Eligibility Filter**  
Only promote when:  
- Fielding ≥ 4 (foresight under ambiguity)  
- Arm Strength ≥ 4 (clear cross-hierarchy communication)  
- Speed ≥ 4 (calibrated urgency)  
- Power ≥ 4 (anchored conviction)  
- Hitting for Average ≥ 4 (cultural glue)  

Missing any = Stretch-Capable at best.  
Missing two or more = SME-Only path.
                """
            elif "sme" in q or "pitfall" in q or "promot" in q and "expert" in q:
                answer = """
**Common SME Promotion Pitfalls**  
- Execution Excellence → Micromanagement  
- Deep Knowledge → Weaponizes expertise  
- Busy Bee Mentality → Activity ≠ strategy  
- Low Emotional Calibration → Talks down, erodes safety  

Never promote technical brilliance without behavioral calibration.
                """
            elif "messaging" in q or "mask" in q or "misalign" in q:
                answer = """
**Messaging to Mask Misalignment**  
Tactics:  
- Framing over function  
- Abstract value spam  
- Narrative smoothing  
- Visual optics  
- Intentional ambiguity  

Result: Temporary illusion, long-term erosion of trust and performance.
                """
            elif "risk" in q or "execution" in q or "precision" in q:
                answer = """
**Risk-Sensitive Execution Roles Demand**  
- High decision load  
- Zero emotional leakage under pressure  
- Cost-aware speed  
- Crystal target clarity  
- Real-time behavioral calibration  

One weak link = system failure.
                """
            else:
                answer = "Ask about Eligibility Filter, SME Pitfalls, Messaging to Mask Misalignment, or Risk-Sensitive Roles for deep insights."
            st.markdown("### Answer")
            st.markdown(answer)
        else:
            st.warning("Please enter a question")

    # SAME scoring & radar — unchanged
    st.subheader("Score the Employee on Each Tool (1-5)")
    scores = [st.slider(tool, 1, 5, 3) for tool in TOOLS]
    employee_notes = st.text_area("Enter notes about the employee")

    if st.button("Generate Scoring"):
        total_score = sum(scores)
        category, action = interpret_score(total_score)
        analysis = f"### Evaluation Summary\n\n**Total Score:** {total_score}/25\n**Leadership Category:** {category}\n**Recommended Action:** {action}\n\n#### Tool-by-Tool\n"
        for tool, score in zip(TOOLS, scores):
            status = "Needs Development" if score <= 2 else "Effective" if score <= 4 else "Exceptional"
            analysis += f"- **{tool}:** {score} ({status})\n"
        analysis += f"\n**Notes:** {employee_notes or 'None'}"
        st.markdown(analysis)

        fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="Behavioral Tool Scoring Radar")
        fig.update_traces(fill='toself')
        st.plotly_chart(fig)

        # Follow-up under radar — now AI-free
        st.subheader("Ask a follow-up question about the radar:")
        radar_q = st.text_area("Enter your question", placeholder="e.g., Training recommendations for low Power?")
        if st.button("Get Answer", key="radar_answer"):
            if radar_q.strip():
                rq = radar_q.lower()
                if "power" in rq:
                    ans = "Low Power: Practice ownership rituals, structured feedback loops, and humility training."
                elif "speed" in rq:
                    ans = "Low Speed: Pause protocols, reflection drills, feedback integration exercises."
                elif "fielding" in rq            
        
def render_module_5():
    import streamlit as st
    import plotly.express as px

    st.title("☢️ Toxicity in the Workplace")

    # SAME Educational Expanders
    with st.expander("Padilla’s Toxic Triangle"):
        st.write("Destructive Leaders, Susceptible Followers, and Conducive Environments create toxic conditions.")
    with st.expander("Hogan’s Dark Side Derailers"):
        st.write("Traits like Arrogance, Volatility, and Manipulativeness can derail leadership effectiveness.")
    with st.expander("Machiavellianism & Dark Triad"):
        st.write("Machiavellianism, Narcissism, and Psychopathy are key indicators of toxic tendencies.")
    with st.expander("Behavioral Drift & 360-Degree Feedback"):
        st.write("Behavioral drift occurs when employees gradually deviate from norms; 360-degree feedback helps detect early signs.")

    # SAME Rubric Table
    st.subheader("Toxicity Rubric")
    st.markdown("""
    <table style='width:100%; border:1px solid black; font-size:14px"}}>
    <tr><th>Tool</th><th>Low Risk (3-4)</th><th>Moderate Risk (2)</th><th>High Risk (1)</th><th>Toxicity Triggers</th></tr>
    <tr><td>Speed</td><td>Adapts quickly; integrates feedback without ego.</td><td>Slow to adapt; reacts impulsively.</td><td>Freezes or disengages; ignores feedback.</td><td>Erratic decisions under pressure; volatility derailer.</td></tr>
    <tr><td>Power</td><td>Owns outcomes; decisive and humble.</td><td>Hesitates; deflects blame occasionally.</td><td>Blames others; manipulates responsibility.</td><td>Arrogance derailer; shirking accountability.</td></tr>
    <tr><td>Fielding</td><td>Anticipates risks; builds robust systems.</td><td>Misses risks; rigid under stress.</td><td>Ignores risks; fosters chaos.</td><td>Unchecked risk-taking; overconfidence derailer.</td></tr>
    <tr><td>Hitting for Average</td><td>Delivers consistently; builds trust.</td><td>Inconsistent; skips documentation.</td><td>Silent quitting; erodes trust.</td><td>Detachment derailer; cultural drift.</td></tr>
    <tr><td>Arm Strength</td><td>Communicates clearly; inspires buy-in.</td><td>Dominates or charms without substance.</td><td>Manipulative; dismisses feedback.</td><td>Divisive communication; manipulativeness derailer.</td></tr>
    </table>
    """, unsafe_allow_html=True)

    # SAME Q&A — keyword logic
    q = st.text_area("Ask about toxic leadership")
    if st.button("Get Response"):
        if q.strip():
            ql = q.lower()
            if "padilla" in ql or "triangle" in ql:
                ans = "**Padilla’s Toxic Triangle**\nDestructive Leaders + Susceptible Followers + Conducive Environment = Toxicity.\nBreak any one leg and toxicity collapses."
            elif "hogan" in ql or "derailer" in ql:
                ans = "**Hogan’s Dark-Side Derailers**\n- Volatility (Speed)\n- Arrogance (Power)\n- Overconfidence (Fielding)\n- Detachment (Hitting)\n- Manipulativeness (Arm Strength)"
            elif "machiavell" in ql or "dark triad" in ql:
                ans = "**Dark Triad Traits**\n- Machiavellianism → Manipulative Arm Strength\n- Narcissism → Inflated Power\n- Psychopathy → Detached Hitting + Volatile Speed"
            elif "drift" in ql or "360" in ql:
                ans = "**Behavioral Drift Detection**\n360-degree feedback catches gradual deviation before it becomes cultural cancer.\nEarly signals: dropping Hitting for Average, rising Power dysfunction."
            else:
                ans = "Ask about Padilla’s Triangle, Hogan’s Derailers, Dark Triad, or Behavioral Drift for deep insights."
            st.markdown("### Response")
            st.markdown(ans)
        else:
            st.warning("Enter a question first")

    # SAME Scoring Sliders
    st.subheader("Rate the Employee on Each Dimension")
    speed = st.slider("Speed", 1, 5, 3)
    power = st.slider("Power", 1, 5, 3)
    fielding = st.slider("Fielding", 1, 5, 3)
    hitting = st.slider("Hitting for Average", 1, 5, 3)
    arm_strength = st.slider("Arm Strength", 1, 5, 3)
    notes = st.text_area("Additional Notes")

    # SAME Generate Profile + Radar + Table
    if st.button("Generate Profile"):
        total_score = speed + power + fielding + hitting + arm_strength
        if total_score >= 15:
            risk_level = "Low Risk"
            action_plan = "Retain and support; encourage continued engagement."
        elif total_score >= 10:
            risk_level = "Moderate Risk"
            action_plan = "Provide coaching and monitor closely for improvement."
        else:
            risk_level = "High Risk"
            action_plan = "Immediate intervention required; consider reassignment or exit strategy."

        st.write(f"**Total Score:** {total_score}/25")
        st.write(f"**Risk Level:** {risk_level}")
        st.write(f"**Action Plan:** {action_plan}")

        categories = ["Speed", "Power", "Fielding", "Hitting", "Arm Strength"]
        scores_list = [speed, power, fielding, hitting, arm_strength]
        fig = px.line_polar(r=scores_list, theta=categories, line_close=True)
        fig.update_traces(fill='toself')
        fig.update_layout(title="Toxicity Profile Radar Chart")
        st.plotly_chart(fig)

        st.markdown("""
        <h4>Total Score Interpretation</h4>
        <table style='width:100%; border:1px solid black;'>
        <tr><th>Score Range</th><th>Risk Level</th><th>Description</th></tr>
        <tr><td>15-20</td><td>Low Risk</td><td>Employee demonstrates strong alignment with organizational values.</td></tr>
        <tr><td>10-14</td><td>Moderate Risk</td><td>Employee shows signs of disengagement or minor toxic behaviors.</td></tr>
        <tr><td>Below 10</td><td>High Risk</td><td>Immediate intervention required; behaviors are harmful to team culture.</td></tr>
        </table>
        """, unsafe_allow_html=True)

        # Contextual Insight — keyword-based (fixed multi-line strings)
        if notes.strip():
            n = notes.lower()
            insight = "No strong toxic signals detected from notes."
            if any(w in n for w in ["blame", "fault", "not me", "they", "others"]):
                insight = """**High Power Toxicity Risk**  
Blame-shifting detected — classic arrogance derailer.  
Immediate coaching on ownership required."""
            elif any(w in n for w in ["charm", "everyone loves", "optics", "image", "perform"]):
                insight = """**High Arm Strength Toxicity Risk**  
Manipulative charm without substance — theater over truth."""
            elif any(w in n for w in ["quiet", "disengage", "silent", "checked out", "quit"]):
                insight = """**High Hitting Toxicity Risk**  
Silent quitting / detachment derailer — reliability collapsing."""
            elif any(w in n for w in ["rigid", "my way", "resist", "defensive", "block"]):
                insight = """**High Fielding Toxicity Risk**  
Rigid under stress — blocks learning and innovation."""
            st.subheader("Contextual Insight")
            st.markdown(insight)
            
def render_module_6():
    st.title("SWOT 2.0 Strategic Framework")
    st.markdown("Designed by Bryan Barrera – Bias-Resistant, Systems-Driven")

    notes = st.text_area("Raw notes / challenges", height=180)

    if st.button("Generate Bias-Resistant SWOT 2.0", type="primary"):
        if not notes.strip():
            st.warning("Please enter notes first")
            return

        n = notes.lower()

        # === Extract key themes using keyword logic (your book + SWOT 2.0) ===
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []

        # Strengths
        if any(w in n for w in ["strong", "great", "leader", "team", "skill", "expert", "reliable", "consistent", "culture", "process", "system", "tool"]):
            strengths.append("Strong leadership and/or team cohesion")
        if any(w in n for w in ["data", "tech", "tool", "system", "process", "efficient", "lean"]):
            strengths.append("Robust systems or technical capability")
        if any(w in n for w in ["loyal", "long-term", "tenured", "experienced"]):
            strengths.append("Experienced, loyal workforce")

        # Weaknesses
        if any(w in n for w in ["toxic", "blame", "ego", "arrogant", "disengage", "quiet quit", "drift", "burnout", "turnover"]):
            weaknesses.append("Toxic behavior or behavioral drift")
        if any(w in n for w in ["rigid", "slow", "resist", "change", "old", "outdated"]):
            weaknesses.append("Resistance to change / outdated processes")
        if any(w in n for w in ["firefight", "reactive", "chaos", "miss", "risk"]):
            weaknesses.append("Reactive culture / lack of foresight")
        if any(w in n for w in ["silo", "misalign", "communication", "dominate", "charm"]):
            weaknesses.append("Poor cross-functional communication or misalignment")

        # Opportunities
        if any(w in n for w in ["train", "coach", "develop", "grow", "upskill"]):
            opportunities.append("Leadership development & coaching programs")
        if any(w in n for w in ["system", "process", "lean", "5-tool", "framework"]):
            opportunities.append("Implement 5-Tool Framework for calibration")
        if any(w in n for w in ["360", "feedback", "drift", "toxicity"]):
            opportunities.append("Introduce 360-degree feedback to catch drift early")
        if any(w in n for w in ["culture", "value", "trust"]):
            opportunities.append("Rebuild trust through consistency and recognition")

        # Threats
        if any(w in n for w in ["competitor", "market", "economy", "lose", "talent"]):
            threats.append("Talent flight to competitors")
        if any(w in n for w in ["toxic", "lawsuit", "reputation"]):
            threats.append("Reputational damage from unresolved toxicity")
        if any(w in n for w in ["burnout", "turnover", "drift"]):
            threats.append("Cultural collapse from unchecked behavioral drift")

        # Default fallback if no keywords
        if not (strengths or weaknesses or opportunities or threats):
            st.info("No strong signals detected — try adding more detail about people, processes, or culture.")
            return

        # === Display Quadrants (your exact layout) ===
        st.subheader("✅ Generated SWOT Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### **Strengths**")
            for s in strengths or ["(None detected)"]:
                st.markdown(f

def render_module_7():
    st.title("🚧 Page 8: Under Construction")
    st.markdown("This page is not yet implemented.")
    
# -------------------------------
# Navigation
# -------------------------------
PAGES = [
    "Page 1: The 5 Tool Employee Framework",
    "Page 2: The 5 Tool Employee Framework: Deep Research Version",
    "Page 3: Behavior Under Pressure Grid",
    "Page 4: Behavioral Calibration Grid",
    "Page 5: Toxicity in the Workplace",
    "Page 6: SWOT 2.0",
    "Page 7: Repository",
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
elif selected_page == "Page 6: SWOT 2.0":
    render_module_6()
elif selected_page == "Page 7: Repository":
    render_module_7()
    

