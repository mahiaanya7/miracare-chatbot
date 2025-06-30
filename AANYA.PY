# MiraCare: AI Mental Health + Career Assistant (Web UI + Mood Tracker)

import openai
import os
import streamlit as st
import datetime

# Set your OpenAI API key
oai_key = os.getenv("OPENAI_API_KEY")  # or manually: oai_key = "your-api-key"
openai.api_key = oai_key

# ---- Core Function: Chat with GPT-4 ----
def chat_with_user(prompt, user_mood=None, resume_content=None):
    system_prompt = """
    You are MiraCare, a warm, supportive, and smart AI assistant that helps users with mental wellness and career guidance. 
    Respond kindly, use simple and motivating language. If user sounds stressed or sad, offer positive reinforcement or journaling prompts.
    If resume is provided, analyze it and give 3 career improvement tips.
    """

    if resume_content:
        prompt = f"User needs resume help. Here's the resume:\n{resume_content}\nPlease review it and give feedback."
    elif user_mood:
        prompt = f"User seems {user_mood}. Suggest a calming tip and ask a reflective question.\n{prompt}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.8
    )
    return response.choices[0].message.content

# ---- Mood History Tracker ----
def load_mood_history():
    if "mood_history" not in st.session_state:
        st.session_state.mood_history = []
    return st.session_state.mood_history

def update_mood_history(mood):
    st.session_state.mood_history.append({
        "date": str(datetime.date.today()),
        "mood": mood
    })

# ---- Streamlit Web UI ----
st.set_page_config(page_title="MiraCare AI Assistant", layout="centered")
st.title("🧠 MiraCare: Mental Health & Career Assistant")
st.write("Choose your need and get kind, smart support from AI.")

mode = st.radio("Choose Mode", ["Mental Health Support", "Resume Feedback"])

if mode == "Mental Health Support":
    mood = st.text_input("How are you feeling today? (e.g., anxious, happy, sad)")
    thoughts = st.text_area("What’s on your mind today?")
    if st.button("Talk to MiraCare"):
        if thoughts.strip():
            update_mood_history(mood)
            reply = chat_with_user(thoughts, user_mood=mood)
            st.success("MiraCare says:")
            st.write(reply)
        else:
            st.warning("Please share your thoughts first.")

    # Mood Tracker Display
    mood_history = load_mood_history()
    if mood_history:
        st.subheader("📈 Your Mood History")
        for entry in mood_history[-5:]:  # Show last 5 entries
            st.write(f"{entry['date']}: *{entry['mood']}*")

elif mode == "Resume Feedback":
    resume = st.text_area("Paste your resume content (plain text)")
    if st.button("Analyze Resume"):
        if resume.strip():
            reply = chat_with_user("", resume_content=resume)
            st.success("MiraCare Feedback:")
            st.write(reply)
        else:
            st.warning("Please paste your resume to continue.")
