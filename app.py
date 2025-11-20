import os
import pandas as pd
import streamlit as st
import plotly.express as px
from docx import Document

# -------------------------------
# Load Book Content for Keyword Logic
# -------------------------------
"book_path = "/mount/src/five_tool_web/The 5 Tool Employee Framework .docx"  # Ensure this file is in the same directory
doc = Document(book_path)
book_text = "
".join([p.text for p in doc.paragraphs if p.text.strip()])

# Keyword mapping for responses
keyword_map = {
    "hitting": "Hitting for Average – Reliability, Rhythm & Repeatability",
    "technical": "Hitting for Average – Reliability, Rhythm & Repeatability",
    "fielding": "Fielding – Strategic Foresight & System Protection",
    "problem": "Fielding – Strategic Foresight & System Protection",
    "speed": "Speed – Adaptability & Continuous Learning",
    "adapt": "Speed – Adaptability & Continuous Learning",
    "arm": "Arm Strength – Communication & Leadership",
    "communication": "Arm Strength – Communication & Leadership",
    "power": "Power – Strategic Decision-Making",
    "strategy": "Power – Strategic Decision-Making"
}

# Extract section from book text
def extract_section(section_title):
    lines = book_text.split("
")
    for i, line in enumerate(lines):
        if section_title.split(" – ")[0] in line:
            return " ".join(lines[i:i+5])
    return "Details not found in book."

# Get response based on keywords
def get_response(user_input):
    for key, section in keyword_map.items():
        if key in user_input.lower():
            return f"### {section}

{extract_section(section)}"
    return "### Overview
The 5 Tool Employee Framework emphasizes:
- Speed (Adaptability & Continuous Learning)
- Power (Strategic Decision-Making)
- Fielding (Problem-Solving & Foresight)
- Hitting for Average (Reliability & Rhythm)
- Arm Strength (Communication & Leadership)"

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Module 1 – 5 Tool Employee Framework", layout="wide")
st.title("Module 1 – The 5 Tool Employee Framework")

# Intro visuals and explanation (Baseball analogy + Professional mapping)
st.markdown("""
## ⚾ Baseball Analogy Meets Business
The original 5-Tool Baseball Player concept evaluates players on:
- **Hitting for Average** – Consistency
- **Hitting for Power** – Big plays
- **Speed** – Quickness
- **Fielding** – Defensive ability
- **Arm Strength** – Throwing power

We’ve adapted this to business:
- **Hitting for Average → Technical Competence & Reliability**
- **Fielding → Problem-Solving & Strategic Foresight**
- **Speed → Adaptability & Continuous Learning**
- **Arm Strength → Communication & Leadership**
- **Power → Strategic Decision-Making**

Every professional needs all five tools to thrive in today’s dynamic environment.
""")

# -------------------------------
# Sliders for scoring
# -------------------------------
st.subheader("Rate Candidate on 5 Tools")
speed = st.slider("Speed (Adaptability)", 1, 10, 5)
power = st.slider("Power (Decision-Making)", 1, 10, 5)
fielding = st.slider("Fielding (Problem-Solving)", 1, 10, 5)
hitting = st.slider("Hitting for Average (Reliability)", 1, 10, 5)
arm = st.slider("Arm Strength (Communication)", 1, 10, 5)

# Radar chart visualization
scores = pd.DataFrame({
    "Tool": ["Speed", "Power", "Fielding", "Hitting", "Arm"],
    "Score": [speed, power, fielding, hitting, arm]
})
fig = px.line_polar(scores, r="Score", theta="Tool", line_close=True,
                    title="Candidate 5 Tool Profile", range_r=[0, 10])
fig.update_traces(fill='toself')
st.plotly_chart(fig)

# -------------------------------
# Notes section
# -------------------------------
notes = st.text_area("Add Notes about Candidate", placeholder="e.g., strong leadership, adaptable, great communicator")

# -------------------------------
# Chat interface for keyword Q&A
# -------------------------------
st.subheader("Ask About a Tool")
user_query = st.text_input("Enter your question (e.g., Tell me about Speed)")
if user_query:
    st.markdown(get_response(user_query))

# -------------------------------
# Premium Features Placeholders
# -------------------------------
st.subheader("Premium Features")
st.button("Convert to PDF (Upgrade for $9.99/month)", disabled=True)
st.button("Save to Repository (Upgrade for $9.99/month)", disabled=True)
st.info("Upgrade in Module 7 to unlock PDF download and repository save.")

# -------------------------------
# Subscription Logic Placeholder
# -------------------------------
st.write("Subscription logic will be integrated in Module 7.")

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
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=700
        )
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in leadership assessment and organizational culture."},
                {"role": "user", "content": contextual_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
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
# For now, we'll simulate with blended logic from user notes and industry best practices.

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

def render_module_6():
    st.title("📊 SWOT 2.0 Strategic Framework")
    st.markdown("Designed by Bryan Barrera & Microsoft Copilot")

    notes = st.text_area("Additional Notes and Input")

    view_mode = st.radio("Select View Mode", ["Basic SWOT", "Advanced SWOT 2.0"])

    if st.button("🎯 Generate AI-Powered SWOT"):
        strengths, weaknesses, opportunities, threats = generate_ai_swot(notes, ai_chat)

        # Quadrant Layout
        st.subheader("✅ Generated SWOT Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### **Strengths**")
            for s in strengths:
                st.markdown(f"- {s}")
            st.markdown("### **Opportunities**")
            for o in opportunities:
                st.markdown(f"- {o}")
        with col2:
            st.markdown("### **Weaknesses**")
            for w in weaknesses:
                st.markdown(f"- {w}")
            st.markdown("### **Threats**")
            for t in threats:
                st.markdown(f"- {t}")

        if view_mode == "Advanced SWOT 2.0":
            st.subheader("📈 Narrative Summary")
            st.write("This analysis blends internal insights with external best practices. "
                     "Key focus: manage cultural risks, leverage new hire's network, and mitigate attrition through upskilling.")

            st.subheader("📊 Weighted Scoring Table")
            st.write("Criteria: Impact (40%), Feasibility (30%), Urgency (20%), Confidence (10%)")

            data = []
            for category, items in zip(["Strength", "Weakness", "Opportunity", "Threat"], [strengths, weaknesses, opportunities, threats]):
                for item in items:
                    scores = score_factor()
                    total = calculate_weighted_score(scores)
                    row = {"Category": category, "Factor": item, **scores, "Total Score": round(total, 2)}
                    data.append(row)

            df = pd.DataFrame(data)
            st.dataframe(df.sort_values(by="Total Score", ascending=False))

            st.subheader("🛠 Dynamic KPIs")
            st.write("Actionable steps with milestones, ownership, and scenario planning.")
            roadmap_df = generate_roadmap(df)
            st.dataframe(roadmap_df)

# Integrate with your app navigation
# Example:
# if selected_page == "Module 6":
#     render_module_6()

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
    

