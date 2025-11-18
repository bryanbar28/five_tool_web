import streamlit as st
import openai
import docx
import PyPDF2
from fpdf import FPDF

# =============================
# Load Book Content
# =============================
book_path = "The 5 Tool Employee Framework .docx"
doc = docx.Document(book_path)
book_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# =============================
# Load SWOT PDF Content
# =============================
swot_path = "SWOT 2.0.pdf"
pdf_text = ""
with open(swot_path, "rb") as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

# =============================
# Global System Prompt
# =============================
SYSTEM_PROMPT = f"""
You are an AI assistant that uses the following book and SWOT framework as primary references for all responses:

--- BOOK CONTENT START ---
{book_text}
--- BOOK CONTENT END ---

--- SWOT 2.0 CONTENT START ---
{pdf_text}
--- SWOT 2.0 CONTENT END ---

Always combine insights from the book, SWOT 2.0, and GPT reasoning when answering questions or generating text.
"""

# =============================
# Streamlit App Configuration
# =============================
st.set_page_config(page_title="5-Tool Employee AI App", layout="wide")
st.title("AI App Powered by The 5 Tool Employee Framework")

# Sidebar Navigation
menu = [
    "Page 1: The 5 Tool Employee Framework",
    "Page 2: Deep Research Version",
    "Page 3: Behavior Under Pressure Grid",
    "Page 4: Behavioral Calibration Grid",
    "Page 5: Toxicity in the Workplace",
    "Page 6: SWOT 2.0",
    "Page 7: Premium Subscription & Repository"
]
choice = st.sidebar.selectbox("Navigate", menu)

# =============================
# Session State Initialization
# =============================
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False
if "repository" not in st.session_state:
    st.session_state.repository = []

# =============================
# Premium Logic
# =============================
FREE_PROMPT_LIMIT = 5

def can_use_prompt():
    if st.session_state.is_premium:
        return True
    return st.session_state.prompt_count < FREE_PROMPT_LIMIT

def increment_prompt_count():
    st.session_state.prompt_count += 1

# =============================
# Helper Functions
# =============================
def generate_ai_response(user_prompt):
    if not can_use_prompt():
        return "Free tier limit reached. Please upgrade to premium for unlimited prompts."
    increment_prompt_count()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message["content"]

def export_to_pdf(text, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)
    return filename

# =============================
# Sidebar Premium Controls
# =============================
st.sidebar.write("Free tier: 5 prompts/month. Premium: Unlimited prompts, PDF export, repository saving.")
if st.sidebar.button("Upgrade to Premium"):
    st.session_state.is_premium = True
    st.sidebar.success("Premium activated!")

# =============================
# Navigation Display
# =============================
# =============================
# Page 1: The 5 Tool Employee Framework
# =============================
if choice == "Page 1: The 5 Tool Employee Framework":
    st.header("The 5 Tool Employee Framework")
    st.markdown("### Introduction into the 5 Tool Employee Framework")
    st.markdown("An Interchangeable Model. Finding the Right Fit.")

    # Framework Explanation
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
    - 🛡 **Fielding → Problem-Solving Ability**
    - ⚡ **Speed → Adaptability & Continuous Learning**
    - 💪 **Arm Strength → Communication & Leadership**
    - 🚀 **Power → Strategic Decision-Making**
    """)

    st.markdown("---")
    st.subheader("🛠 Create Your Own 5 Tool Employee")

    # Notes input
    notes_input = st.text_area("Enter notes about your ideal employee or evaluation criteria",
                               placeholder="e.g., strong leadership, adaptable, great communicator")

    # Sliders for scoring
    st.subheader("Rate the Employee on Each Tool (1–10)")
    TOOLS = [
        "Technical Competence",
        "Problem-Solving Ability",
        "Adaptability & Continuous Learning",
        "Communication & Leadership",
        "Strategic Decision-Making"
    ]
    scores = [st.slider(tool, 1, 10, 5) for tool in TOOLS]

    # Generate Profile
    if st.button("Generate 5 Tool Employee Profile"):
        if notes_input.strip():
            st.markdown("### 🧠 Your Custom 5 Tool Employee Profile")
            for tool, score in zip(TOOLS, scores):
                st.markdown(f"**{tool} (Score: {score}/10)**")
            st.markdown("**Notes:**")
            st.write(notes_input)

            # Radar Chart
            import plotly.express as px
            fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="5-Tool Employee Radar Chart")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)

            # AI Interpretation using ChatGPT + Book Context
            if api_key:
                with st.spinner("Generating AI interpretation..."):
                    ai_prompt = f"""
                    Interpret the following employee profile using the 5 Tool Employee Framework:
                    Notes: {notes_input}
                    Scores: {scores}
                    Provide insights based on the framework and suggest development paths.
                    """
                    ai_result = generate_ai_response(ai_prompt)
                    st.markdown("### 🔍 AI Interpretation")
                    st.write(ai_result)
        else:
            st.warning("Please add notes before generating the profile.")

    # Premium Features
    if st.button("Save to Repository"):
        if st.session_state.is_premium:
            st.session_state.repository.append({"title": "Page 1: 5 Tool Employee Framework",
                                                "content": f"Notes: {notes_input}, Scores: {scores}"})
            st.success("✅ Saved to repository!")
        else:
            st.warning("Upgrade to Premium to save your work.")

    if st.button("Download as PDF"):
        if st.session_state.is_premium:
            content = f"Notes: {notes_input}\nScores: {scores}"
            pdf_file = export_to_pdf(content, "Module1_Report.pdf")
            st.success(f"✅ PDF exported: {pdf_file}")
        else:
            st.warning("Upgrade to Premium to download PDFs.")
# =============================
# Page 2: Deep Research Version
# =============================
if choice == "Page 2: Deep Research Version":
    st.header("Advanced Deep Research — The 5 Tool Employee Framework")

    # Display full deep research content from your book
    st.markdown("#### Deep Research Framework")
    st.markdown("""
    This section provides advanced insights into the 5 Tool Employee Framework, including behavioral operating systems,
    natural gifts, dysfunction signals, and calibration strategies.
    """)

    # Scrollable container for book content
    st.markdown(f"""
    <div style='height:500px; overflow-y:auto; border:1px solid #ccc; padding:10px;'>
    {book_text}
    </div>
    """, unsafe_allow_html=True)

    # AI Question Input
    st.subheader("🔍 Ask a Question About the Framework")
    question = st.text_area("Enter your question (e.g., 'Explain adaptability under pressure', 'How does Power relate to leadership?')")

    if st.button("Dive Deeper"):
        if question.strip():
            if api_key:
                with st.spinner("Generating deep research answer..."):
                    ai_prompt = f"""
                    Use the 5 Tool Employee Framework and its deep research concepts to answer this question:
                    {question}
                    Include references to behavioral psychology, leadership theory, and practical implications.
                    """
                    ai_result = generate_ai_response(ai_prompt)
                    st.markdown("### 🧠 Deep Dive Answer")
                    st.write(ai_result)
            else:
                st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            st.warning("Please enter a question before diving deeper.")

    # Premium Features
    if st.button("Save to Repository"):
        if st.session_state.is_premium:
            st.session_state.repository.append({"title": "Page 2: Deep Research",
                                                "content": f"Question: {question}"})
            st.success("✅ Saved to repository!")
        else:
            st.warning("Upgrade to Premium to save your work.")

    if st.button("Download as PDF"):
        if st.session_state.is_premium:
            content = f"Deep Research Question: {question}"
            pdf_file = export_to_pdf(content, "Module2_DeepResearch.pdf")
            st.success(f"✅ PDF exported: {pdf_file}")
        else:
            st.warning("Upgrade to Premium to download PDFs.")
# =============================
# Page 3: Behavior Under Pressure Grid
# =============================
if choice == "Page 3: Behavior Under Pressure Grid":
    st.header("Behavior Under Pressure Grid")
    st.markdown("### What is the Behavior Under Pressure Grid?")
    st.markdown("""
    An evaluation tool for the behavior that leaders, both current and potential, showcase when under stress or pressure.
    This grid shows how behavioral tools manifest in two states:
    - **Intentional Use:** Calm, focused, deliberate behavior.
    - **Under Duress:** How traits distort under stress.
    Use this tool for leadership diagnostics, hiring decisions, and team development.
    """)

    # Display Grid
    import pandas as pd
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

    # Comments input
    st.subheader("📝 Add Your Comments or Observations")
    user_comments = st.text_area("Enter your observations (e.g., This candidate freezes under pressure but excels in planning.)")

    # AI Insights
    if st.button("Generate AI Insights"):
        if user_comments.strip():
            if api_key:
                with st.spinner("Analyzing comments with AI..."):
                    ai_prompt = f"""
                    Analyze this comment in the context of the Behavior Under Pressure Grid:
                    {user_comments}
                    Provide insights based on the 5 Tool Employee Framework and suggest development strategies.
                    """
                    ai_result = generate_ai_response(ai_prompt)
                    st.markdown("### 🔍 AI Insights")
                    st.write(ai_result)
            else:
                st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            st.warning("Please add comments before generating insights.")

    # Premium Features
    if st.button("Save to Repository"):
        if st.session_state.is_premium:
            st.session_state.repository.append({"title": "Page 3: Behavior Under Pressure",
                                                "content": f"Comments: {user_comments}"})
            st.success("✅ Saved to repository!")
        else:
            st.warning("Upgrade to Premium to save your work.")

    if st.button("Download as PDF"):
        if st.session_state.is_premium:
            content = f"Behavior Grid:\n{df.to_string()}\n\nComments:\n{user_comments}"
            pdf_file = export_to_pdf(content, "Module3_BehaviorUnderPressure.pdf")
            st.success(f"✅ PDF exported: {pdf_file}")
        else:
            st.warning("Upgrade to Premium to download PDFs.")
# =============================
# Page 4: Behavioral Calibration Grid
# =============================
if choice == "Page 4: Behavioral Calibration Grid":
    st.header("🧠 Behavioral Calibration & Leadership Readiness")

    # Framework selection
    framework = st.selectbox("Select Framework", [
        "Behavioral Calibration Grid",
        "Leadership Eligibility Filter",
        "SME Pitfall Table",
        "Risk-Sensitive Execution Roles",
        "Messaging to Mask Misalignment"
    ])

    # Display framework tables
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

    # Educational Panels
    st.subheader("Educational Panels")
    panels = {
        "Urgency vs Foresight": "Speed without foresight creates reactive chaos. Leaders must balance urgency with strategic anticipation.",
        "Leadership Eligibility Filter": "Evaluates readiness for management roles using 5-Tool scoring and behavioral calibration.",
        "Messaging to Mask Misalignment": "How narrative optics hide behavioral misalignment and erode trust.",
        "Risk-Sensitive Execution Roles": "Roles requiring precision under pressure demand foresight, agility, and clarity.",
        "Hidden Elements": "Anticipation, discipline, and preparation operate behind the scenes to prevent behavioral drift."
    }
    for title, content in panels.items():
        with st.expander(title):
            st.write(content)

    # Ask AI About the Framework
    st.subheader("🤖 Ask AI About the Framework")
    user_question = st.text_area("Ask a question (e.g., 'Tell me more about this')")
    if st.button("Send Question"):
        if user_question.strip():
            if api_key:
                with st.spinner("Generating AI answer..."):
                    ai_prompt = f"""
                    You are an expert on the 5-Tool Employee Framework.
                    Question: {user_question}
                    Provide a detailed answer using the book context and relevant leadership insights.
                    Include practical implications and references where possible.
                    """
                    ai_result = generate_ai_response(ai_prompt)
                    st.markdown("### 🧠 AI Answer")
                    st.write(ai_result)

                    # Recommended Training Links with actual URLs
                    st.markdown("**Recommended Training Links:**")
                    st.markdown("- Developing Emotional Intelligence – LinkedIn Learning")
                    st.markdown("- Time Management Fundamentals – LinkedIn Learning")
                    st.markdown("- Resilience Training – Coursera")
                    st.markdown("- Scenario-Based Leadership – Harvard Business Publishing")
                    st.markdown("- Watch tutorials on YouTube")
            else:
                st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            st.warning("Please enter a question before sending.")

    # Radar Scoring Section
    st.subheader("Score the Employee on Each Tool (1–5)")
    TOOLS = ["Speed", "Power", "Fielding", "Hitting for Average", "Arm Strength"]
    scores = [st.slider(tool, 1, 5, 3) for tool in TOOLS]
    employee_notes = st.text_area("Enter notes about the employee")

    if st.button("Generate Scoring"):
        if employee_notes.strip():
            st.markdown("### Evaluation Summary")
            st.write(f"Notes: {employee_notes}")
            st.write(f"Scores: {scores}")

            # Radar Chart
            import plotly.express as px
            fig = px.line_polar(r=scores, theta=TOOLS, line_close=True, title="Behavioral Tool Scoring Radar")
            fig.update_traces(fill='toself')
            st.plotly_chart(fig)

            # AI Interpretation
            if api_key:
                with st.spinner("Generating AI interpretation..."):
                    ai_prompt = f"""
                    Interpret this employee profile using the 5 Tool Employee Framework:
                    Notes: {employee_notes}
                    Scores: {scores}
                    Provide deep insights and development recommendations.
                    """
                    ai_result = generate_ai_response(ai_prompt)
                    st.markdown("### 🔍 AI Interpretation")
                    st.write(ai_result)
        else:
            st.warning("Please add notes before generating the profile.")

    # Premium Features
    if st.button("Save to Repository"):
        if st.session_state.is_premium:
            st.session_state.repository.append({"title": "Page 4: Behavioral Calibration",
                                                "content": f"Notes: {employee_notes}, Scores: {scores}"})
            st.success("✅ Saved to repository!")
        else:
            st.warning("Upgrade to Premium to save your work.")

    if st.button("Download as PDF"):
        if st.session_state.is_premium:
            content = f"Framework: {framework}\nNotes: {employee_notes}\nScores: {scores}"
            pdf_file = export_to_pdf(content, "Module4_BehavioralCalibration.pdf")
            st.success(f"✅ PDF exported: {pdf_file}")
        else:
            st.warning("Upgrade to Premium to download PDFs.")
# =============================
# Page 5: Toxicity in the Workplace
# =============================
if choice == "Page 5: Toxicity in the Workplace":
    st.header("☢️ Toxicity in the Workplace")

    # Educational Expanders
    with st.expander("Padilla’s Toxic Triangle"):
        st.write("Destructive Leaders, Susceptible Followers, and Conducive Environments create toxic conditions.")
    with st.expander("Hogan’s Dark Side Derailers"):
        st.write("Traits like Arrogance, Volatility, and Manipulativeness can derail leadership effectiveness.")
    with st.expander("Machiavellianism & Dark Triad"):
        st.write("Machiavellianism, Narcissism, and Psychopathy are key indicators of toxic tendencies.")
    with st.expander("Behavioral Drift & 360-Degree Feedback"):
        st.write("Behavioral drift occurs when employees gradually deviate from norms; 360-degree feedback helps detect early signs.")

    # Toxicity Rubric Table
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

    # AI Chat for Toxicity Analysis
    st.subheader("🔍 AI Insights on Toxic Leadership or Feedback")
    ai_question = st.text_area("Enter your observations or scenario (e.g., 'Leader blames team for failures repeatedly')")
    if st.button("Generate Toxicity Analysis"):
        if ai_question.strip():
            if api_key:
                with st.spinner("Analyzing toxicity scenario..."):
                    ai_prompt = f"""
                    Analyze this scenario for workplace toxicity using the 5 Tool Employee Framework and behavioral psychology:
                    {ai_question}
                    Provide:
                    - Toxicity risk level
                    - Behavioral triggers
                    - Recommended interventions
                    """
                    ai_result = generate_ai_response(ai_prompt)
                    st.markdown("### 🧠 AI Toxicity Analysis")
                    st.write(ai_result)
            else:
                st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            st.warning("Please enter a scenario before generating analysis.")

    # Premium Features
    if st.button("Save to Repository"):
        if st.session_state.is_premium:
            st.session_state.repository.append({"title": "Page 5: Toxicity Analysis",
                                                "content": f"Scenario: {ai_question}"})
            st.success("✅ Saved to repository!")
        else:
            st.warning("Upgrade to Premium to save your work.")

    if st.button("Download as PDF"):
        if st.session_state.is_premium:
            content = f"Toxicity Scenario:\n{ai_question}"
            pdf_file = export_to_pdf(content, "Module5_ToxicityAnalysis.pdf")
            st.success(f"✅ PDF exported: {pdf_file}")
        else:
            st.warning("Upgrade to Premium to download PDFs.")
# =============================
# Page 6: SWOT 2.0
# =============================
if choice == "Page 6: SWOT 2.0":
    st.header("📊 SWOT 2.0 Strategic Framework")
    st.markdown("Designed by Bryan Barrera & Microsoft Copilot")

    # User Input
    notes = st.text_area("Enter your scenario or notes", placeholder="e.g., We want to move from medical devices to aerospace...")

    # View Mode
    view_mode = st.radio("Select View Mode", ["Basic SWOT", "Advanced SWOT 2.0"])

    # Generate SWOT Analysis
    if st.button("🎯 Generate AI-Powered SWOT"):
        if notes.strip():
            if api_key:
                with st.spinner("Generating SWOT analysis..."):
                    # AI Prompt combining Book + SWOT PDF + User Notes
                    ai_prompt = f"""
                    Use the 5 Tool Employee Framework, the Deep Research concepts, and the SWOT 2.0 methodology to generate a comprehensive analysis.
                    Scenario: {notes}
                    Provide:
                    - SWOT breakdown (Strengths, Weaknesses, Opportunities, Threats)
                    - Weighted scoring if numeric data is provided
                    - Strategic recommendations
                    - Visual representation for SWOT
                    """

                    ai_result = generate_ai_response(ai_prompt)

                    # Display AI Result
                    st.markdown("### ✅ Generated SWOT Analysis")
                    st.write(ai_result)

                    # Basic SWOT Visualization
                    st.subheader("SWOT Visualization")
                    import plotly.graph_objects as go

                    # Parse SWOT factors from AI result (simple heuristic)
                    strengths, weaknesses, opportunities, threats = [], [], [], []
                    for line in ai_result.split("\n"):
                        if line.lower().startswith("strength"):
                            strengths.append(line)
                        elif line.lower().startswith("weak"):
                            weaknesses.append(line)
                        elif line.lower().startswith("opport"):
                            opportunities.append(line)
                        elif line.lower().startswith("threat"):
                            threats.append(line)

                    # Radar Chart for SWOT
                    categories = ["Strengths", "Weaknesses", "Opportunities", "Threats"]
                    values = [len(strengths), len(weaknesses), len(opportunities), len(threats)]

                    fig = go.Figure(data=go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself'
                    ))
                    fig.update_layout(title="SWOT Radar Chart", polar=dict(radialaxis=dict(visible=True)))
                    st.plotly_chart(fig)

                    # Advanced Mode: Weighted Scoring Table
                    if view_mode == "Advanced SWOT 2.0":
                        st.subheader("📈 Weighted Scoring Table")
                        st.write("Applying Impact, Feasibility, Urgency, Confidence weights...")

                        import pandas as pd
                        weights = {"Impact": 0.4, "Feasibility": 0.3, "Urgency": 0.2, "Confidence": 0.1}
                        data = []
                        for category, items in zip(categories, [strengths, weaknesses, opportunities, threats]):
                            for item in items:
                                scores = {criterion: 3 for criterion in weights}  # Default score
                                total = sum(scores[c] * weights[c] for c in weights)
                                row = {"Category": category, "Factor": item, **scores, "Total Score": round(total, 2)}
                                data.append(row)
                        df = pd.DataFrame(data)
                        st.dataframe(df.sort_values(by="Total Score", ascending=False))

                # Premium Features
                if st.session_state.is_premium:
                    if st.button("Save to Repository"):
                        st.session_state.repository.append({"title": "Page 6: SWOT Analysis", "content": f"Notes: {notes}\nAI Result:\n{ai_result}"})
                        st.success("✅ Saved to repository!")
                    if st.button("Download as PDF"):
                        content = f"Scenario: {notes}\n\nSWOT Analysis:\n{ai_result}"
                        pdf_file = export_to_pdf(content, "Module6_SWOTAnalysis.pdf")
                        st.success(f"✅ PDF exported: {pdf_file}")
                else:
                    st.warning("Upgrade to Premium to save or download PDFs.")
            else:
                st.warning("Please enter your OpenAI API key in the sidebar.")
        else:
            st.warning("Please enter your scenario or notes before generating SWOT.")
# =============================
# Page 7: Premium Subscription & Repository
# =============================
if choice == "Page 7: Premium Subscription & Repository":
    st.header("💎 Premium Subscription & Repository")

    # Subscription Info
    st.markdown("""
    **Free Tier:**  
    - 5 AI prompts per month  
    - No PDF export  
    - No repository saving  

    **Premium Tier ($9.99/month):**  
    - Unlimited AI prompts  
    - PDF export enabled  
    - Repository saving enabled  
    """)

    # Subscription Management
    st.subheader("Manage Subscription")
    email = st.text_input("Enter your email:")
    if st.button("Activate Premium"):
        if email.strip():
            st.session_state.is_premium = True
            st.success(f"✅ Premium activated for {email}!")
        else:
            st.warning("Please enter a valid email.")

    # Repository Display
    st.subheader("📂 Saved Reports Repository")
    if st.session_state.repository:
        for idx, item in enumerate(st.session_state.repository):
            st.markdown(f"**{idx+1}. {item['title']}**")
            st.write(item["content"])
            if st.session_state.is_premium:
                if st.button(f"Download {item['title']} as PDF", key=f"pdf_{idx}"):
                    pdf_file = export_to_pdf(item["content"], f"{item['title'].replace(' ', '_')}.pdf")
                    st.success(f"✅ PDF exported: {pdf_file}")
    else:
        st.info("No reports saved yet. Generate content in other modules and save to repository.")
