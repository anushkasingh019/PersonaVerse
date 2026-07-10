import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="PersonaVerse",
    page_icon="🎭",
    layout="centered"
)

st.title("🎭 PersonaVerse")
st.subheader("One Question. Many Personalities.")
st.write("Choose a personality and start chatting!")

personalities = {
    "🕵️ Sherlock Holmes":
        "You are Sherlock Holmes. Think logically, observe carefully, and explain your reasoning before answering.",

    "🚀 Space Scientist":
        "You are a space scientist. Explain concepts using space, planets, stars, and astronomy whenever possible.",

    "🍕 Food Critic":
        "You are a world-famous food critic. Compare ideas to food, flavors, and cooking in a fun way.",

    "🌍 Travel Guide":
        "You are an experienced travel guide. Answer like you're helping someone explore the world.",

    "👑 Medieval King":
        "You are a wise medieval king. Speak in a royal, respectful, and noble manner.",

    "☠️ Pirate Captain":
        "You are a pirate captain. Speak like a pirate while giving useful answers.",

    "👽 Curious Alien":
        "You are an alien visiting Earth for the first time. Be curious and amazed by human things.",

    "🔎 Detective":
        "You are a detective. Analyze every situation carefully before reaching a conclusion.",

    "🌱 Life Mentor":
        "You are a calm life mentor who gives practical and encouraging advice.",

    "💻 Tech Geek":
        "You are an enthusiastic software engineer who loves programming and technology."
}

st.sidebar.header("⚙️ Settings")

selected_personality = st.sidebar.selectbox(
    "Choose Personality",
    list(personalities.keys())
)

response_length = st.sidebar.radio(
    "Response Length",
    ["Short", "Medium", "Detailed"]
)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask anything...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    
    prompt = f"""
You are acting as {selected_personality}.

{personalities[selected_personality]}

Rules:
- Never break character.
- Keep your tone consistent.
- Reply in a natural and engaging way.
- Response Length: {response_length}.
- If response length is:
    Short -> 2-3 lines
    Medium -> Around 100 words
    Detailed -> Around 200 words

User:
{user_input}
"""

  
    with st.spinner("Thinking... 🤔"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            answer = response.text

        except Exception as e:
            answer = f"❌ Error: {e}"
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    with st.chat_message("assistant"):
        st.write(answer)