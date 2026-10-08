import requests
import streamlit as st
from prompts import SYSTEM_PROMPT

st.set_page_config(
    page_title="WalkQuest AI",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 WalkQuest AI")
st.subheader("Turn a walk into an adventure.")

st.write(
    "Generate a fun outdoor quest and get away from the screen."
)

location = st.text_input(
    "📍 Where do you want to walk?",
    "My neighborhood"
)

duration = st.selectbox(
    "⏱ Available time",
    ["15 minutes", "30 minutes", "45 minutes", "60 minutes"]
)

difficulty = st.selectbox(
    "🥾 Difficulty",
    ["Easy", "Medium", "Hard"]
)

if "answer" not in st.session_state:
    st.session_state.answer = None

if st.button("🚀 Generate My Quest"):

    prompt = f"""
{SYSTEM_PROMPT}

Create a SHORT outdoor walking quest.

Location: {location}
Duration: {duration}
Difficulty: {difficulty}

Return ONLY this format:

🌱 YOUR WALK QUEST

🌿 Quest Title:
[short creative title]

⏱️ Duration:
{duration}

🥾 Difficulty:
{difficulty}

🎯 MISSIONS

1. [mission 1]

2. [mission 2]

3. [mission 3]

4. [mission 4]

🦺 SAFETY
[one short safety tip]

🌱 TOUCH GRASS SCORE
[score]/100

📵 QUEST RULE
[one short sentence]

Rules:
- Do NOT write a story.
- Keep the response short.
- Create exactly 4 missions.
- Put every mission on a separate line.
- Missions must be safe and realistic.
- Encourage walking and outdoor observation.
- Do not suggest dangerous activities.
- Do not suggest trespassing.
- Do NOT mention AI.
- Do NOT mention the model.
- Do NOT write "Generated with".
"""

    with st.spinner("🌱 Creating your quest..."):

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "gemma3:1b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            st.session_state.answer = response.json()["response"]

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Ollama is not running. Start Ollama and try again."
            )

        except Exception as e:
            st.error("❌ Gemma generation failed.")
            st.code(str(e))


if st.session_state.answer:

    st.success("Quest Ready! 🌱")

    st.markdown(st.session_state.answer)

    st.divider()

    st.subheader("🏆 Complete Your Quest")

    st.write("Complete all 4 missions to finish your adventure.")

    mission1 = st.checkbox("🌿 Mission 1 completed")
    mission2 = st.checkbox("🌳 Mission 2 completed")
    mission3 = st.checkbox("👀 Mission 3 completed")
    mission4 = st.checkbox("🥾 Mission 4 completed")

    completed = sum([
        mission1,
        mission2,
        mission3,
        mission4
    ])

    st.progress(completed / 4)

    st.write(f"Progress: **{completed}/4 missions completed**")

    if completed == 4:

        st.balloons()

        st.success("🎉 Quest Completed!")

        st.metric(
            "🌱 Touch Grass Achievement",
            "100 XP"
        )

        st.info(
            "🔥 Amazing! You successfully completed your outdoor quest."
        )

    else:

        st.info(
            f"🌱 Complete {4 - completed} more mission(s) to finish your quest."
        )