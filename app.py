import streamlit as st
import plotly.express as px
import requests
import json
import re
from typing import List

st.set_page_config(page_title="5-Tool Employee Framework", page_icon="⚾", layout="wide")

# ================================
# SESSION STATE INIT
# ================================
if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# ================================
# SIDEBAR
# ================================
st.sidebar.title("⚾ 5-Tool Framework")
st.sidebar.markdown("**Select a module**")
page = st.sidebar.radio(
    "Go to",
    [
        "1. Framework Intro",
        "2. 360° Feedback",
        "3. Toxicity Scale",
        "4. Leadership Eligibility",
        "5. Interview Rubrics",
        "6. Repository"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Powered by Grok-4 • {st.session_state.prompt_count} profiles generated this session")

# ================================
# MAIN PAGE (Intro only for now)
# ================================
if page != "1. Framework Intro":
    st.info("More modules coming soon — this is just the playable prototype for now.")
    st.stop()

st.title("The 5-Tool Employee Framework")
st.markdown("### Finding the rare humans who excel across all five dimensions.")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("""
    #### The 5-Tool Player Analogy
    | Baseball Tool       | Professional Equivalent                        |
    |---------------------|---------------------------------------------------------|
    | Hitting for Average | Reliability, Rhythm & Repeatability                    |
    | Power               | Ownership, Initiative & Decisiveness                   |
    | Speed               | Cognitive & Behavioral Agility, Learning Speed         |
    | Fielding            | Strategic Foresight & System Protection                |
    | Arm Strength        | Communication Reach & Influence                        |
    """)

with col_right:
    st.image("https://i.imgur.com/4Q2e8aM.png", use_column_width=True)

st.markdown("---")

# ================================
# INPUT SECTION
# ================================
st.markdown("#### Build a 5-Tool Profile")
notes = st.text_area(
    "Paste resume, LinkedIn export, performance reviews, or any notes here",
    height=220,
    placeholder="e.g. “John was promoted twice in 18 months, led the billing redesign that saved 40% cost…”"
)

tools = [
    "Speed — Cognitive & Behavioral Agility",
    "Power — Ownership, Initiative & Decisiveness",
    "Fielding — Strategic Foresight & System Protection",
    "Hitting for Average — Reliability, Rhythm & Repeatability",
    "Arm Strength — Communication Reach & Influence"
]

manual_scores = []
for tool in tools:
    key = tool.split(" — ")[0].lower()
    score = st.slider(tool, 1, 10, 6, key=key)
    manual_scores.append(score)

if st.button("🚀 Generate 5-Tool Profile", type="primary", use_container_width=True):
    if not notes.strip():
        st.warning("Paste something first — resume, notes, anything.")
        st.stop()

    with st.spinner("Grok-4 is analyzing the full context…"):
        # Proper system prompt so Grok knows exactly what to do
        system_prompt = """
You are an expert talent evaluator using the 5-Tool Employee Framework.
Assess the person described and return ONLY a JSON array with exactly 5 integers (1–10) in this exact order:

1. Speed — Cognitive & Behavioral Agility
2. Power — Ownership, Initiative & Decisiveness  
3. Fielding — Strategic Foresight & System Protection
4. Hitting for Average — Reliability, Rhythm & Repeatability
5. Arm Strength — Communication Reach & Influence

Then write a short, punchy 3–5 paragraph analysis (max 350 words) that justifies the scores with specific evidence from the input.
Do not add any extra text, explanations, or markdown before the JSON.
Response format must be:
[8,6,9,10,7]
<blank line>
Analysis text here...
"""

        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {st.secrets['XAI_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",        # or "grok-x" if you have access
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": notes}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 800
                },
                timeout=120
            )
            response.raise_for_status()
            raw = response.json()["choices"][0]["message"]["content"]

            # Extract scores reliably
            score_match = re.search(r"\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]", raw)
            if score_match:
                final_scores = [int(x) for x in score_match.groups()]
                analysis = raw.split("]", 1)[1].strip()
                if analysis.startswith("\n"):
                    analysis = analysis[1:].strip()
            else:
                raise ValueError("No score array found")

            st.session_state.prompt_count += 1

        except Exception as e:
            st.error("Grok took a nap. Using your manual sliders only.")
            final_scores = manual_scores
            analysis = "_Temporary fallback — full AI analysis unavailable right now._"

    # ================================
    # RADAR CHART
    # ================================
    fig = px.line_polar(
        r=final_scores,
        theta=tools,
        line_close=True,
        range_r=[0, 10],
        title="5-Tool Employee Radar",
        template="plotly_dark"
    )
    fig.update_traces(fill='toself', fillcolor='rgba(0, 191, 255, 0.4)', line_color='deepskyblue')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])))
    st.plotly_chart(fig, use_container_width=True)

    # ================================
    # ANALYSIS OUTPUT
    # ================================
    st.markdown("### AI Analysis")
    st.markdown(analysis)

    # Show raw scores for transparency
    score_str = " • ".join([f"**{t.split(' — ')[0]}**: {s}/10" for t, s in zip(tools, final_scores)])
    st.caption(score_str)
