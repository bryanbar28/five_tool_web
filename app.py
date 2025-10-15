    elif page == "🔄 360 Feedback":
        st.title("🔄 360 Degree Feedback (5-Tool Style)")

        # 📊 Scoring Scale Reference
        st.markdown("### 📊 Scoring Scale Reference")
        st.markdown("""
        | **Total Score** | **Interpretation** | **Action** |
        |----------------|--------------------|------------|
        | **21–25** | Leadership-Ready: A reliable “5-tool player” who adapts, owns outcomes, protects systems, delivers consistently, and inspires teams. Minimal behavioral drift; aligns with team standards. | Retain in leadership or promote. Monitor for minor drift (e.g., stress or burnout). Coach any low scores (1–2). |
        | **15–20** | Stretch-Capable: Solid but shows gaps, like inconsistent reliability or weak forecasting. Risking 90-day employee effectiveness. Behavioral drift may indicate personal or team disruption. | Coach on low scores. Address drift triggers. Retest leadership project. Reassess after 3–6 months. |
        | **Below 15** | High-Risk (90-Day Alert): Likely showing behavioral drift (e.g., blaming others, inconsistency, divisiveness). Risks team disruption. | Do not promote. Address drift directly. Consider role change or exit if drift is chronic. |
        """)

        # 📝 Input Section
        st.markdown("### 📝 Feedback Context")
        role_context = st.text_area("📄 Role or Resume Context", height=200)
        notes_context = st.text_area("📝 Additional Notes or Updates", height=150)

        # 🤖 Strategist Chat
        st.markdown("### 🤖 Ask About Other 360 Models")
        chat_query = st.text_input("Ask your strategist about other feedback models...")
        if chat_query:
            chat_prompt = f"""
            You are a behavioral strategist trained in the 5-Tool Framework. A user asked: "{chat_query}"
            Recommend other 360-degree feedback models (e.g., Bracken, Church, Korn Ferry) and explain how they compare to the 5-Tool approach.
            """
            chat_response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": chat_prompt}],
                temperature=0.7
            )
            st.markdown("#### 🧠 Strategist Response")
            st.markdown(chat_response.choices[0].message.content)

        # 🚀 Generate Button
        st.markdown("### 🚀 Generate 5-Tool Feedback Profile")
        if st.button("Generate Feedback Profile"):
            if not role_context:
                st.warning("Please enter role or resume context.")
            else:
                full_input = f"{role_context}\n\nAdditional Notes:\n{notes_context}"
                scoring_prompt = f"""
                You are a behavioral strategist using the 5-Tool Framework to assess 360-degree feedback.
                Score the individual from 1–5 on each of the following tools:
                - Speed (Cognitive & Behavioral Agility)
                - Ownership, Initiative & Decisiveness
                - Fielding (Strategic Perception & Sensemaking)
                - Hitting for Average (Reliability, Rigor & Execution)
                - Arm Strength (Reach & Influence)

                Then calculate the total score (out of 25) and interpret it using this scale:
                - 21–25: Leadership-Ready
                - 15–20: Stretch-Capable
                - Below 15: High-Risk (90-Day Alert)

                Include behavioral drift triggers if relevant. Use markdown formatting.
                Input context: {full_input}
                """
                feedback = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": scoring_prompt}],
                    temperature=0.7
                )
                result = feedback.choices[0].message.content
                st.session_state.last_feedback = result
                st.markdown("### 🧠 Feedback Profile")
                st.markdown(result)

        # 🗂️ Last Generated Profile
        if 'last_feedback' in st.session_state:
            st.markdown("---")
            st.markdown("### 🗂️ Last Generated Feedback")
            st.markdown(st.session_state.last_feedback)
