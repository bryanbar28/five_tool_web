import streamlit as st
import plotly.express as px
import requests
import re

st.set_page_config(page_title="5-Tool Employee Framework", page_icon="⚾", layout="wide")

st.title("The 5-Tool Employee Framework")
st.markdown("### An Interchangeable Model. Finding the Right Fit.")

st.markdown("""
#### Introduction into the 5-Tool Employee Framework

##### 5-Tool Baseball Player
1. Hitting for Average
2. Hitting for Power
3. Speed
4. Fielding
5. Arm Strength

##### Baseball Tools vs. Professional Skills
1. ⚾ Hitting for Average → Technical Competence & Reliability
2. 🧤 Fielding → Problem-Solving & Strategic Foresight
3. ⚡ Speed → Adaptability & Continuous Learning
4. 💪 Arm Strength → Communication & Leadership
5. 🚀 Power → Strategic Decision-Making & Ownership
""")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("#### Create Your Own 5-Tool Employee")
    notes = st.text_area("Paste resume, job description, or notes here", height=200)

    tools = [
        "Speed — Cognitive & Behavioral Agility",
        "Power — Ownership, Initiative & Decisiveness",
        "Fielding — Strategic Foresight & System Protection",
        "Hitting for Average — Reliability, Rhythm & Repeatability",
        "Arm Strength — Communication Reach & Influence"
    ]

    scores = []
    for t in tools:
        short = t.split(" — ")[0].lower().replace(" ", "_")
        scores.append(st.slider(t, 1, 10, 6, key=short))

with col2:
    st.image("https://i.imgur.com/6ZfZ9kD.png")  # placeholder baseball image

if st.button("Generate Profile", type="primary", use_container_width=True):
    if not notes.strip():
        st.warning("Add some notes or a resume first.")
        st.stop()

    with st.spinner("Grok-4 is reading your full book + deep framework..."):
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {st.secrets['XAI_API_KEY']}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [{"role": "user", "content": notes}],  # simple for now, we'll add the full prompt later
                    "temperature": 0.7
                },
                timeout=90
            )
            response.raise_for_status()
            ai_text = response.json()["choices"][0]["message"]["content"]

            match = re.search(r"\[?\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]?", ai_text)
            final_scores = [int(x) for x in match.groups()] if match else scores

        except Exception:
            st.warning("Grok is taking a quick break — using your sliders only.")
            ai_text = "Full analysis coming soon..."
            final_scores = scores

    fig = px.line_polar(r=final_scores, theta=tools, line_close=True, range_r=[0,10], title="5-Tool Radar")
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(ai_text)
