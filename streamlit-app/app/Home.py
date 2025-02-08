import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🏸 AI Badminton Coach",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- THEME & CSS ---
st.markdown(
    """
    <style>
        .css-1d391kg { padding: 10px; }
        .stTextInput, .stTextArea { border-radius: 12px; }
        .stFileUploader { background-color: rgba(255, 255, 255, 0.1); border-radius: 12px; }
        .stButton button { background-color: #f97316; color: white; font-size: 18px; border-radius: 12px; }
        .stButton button:hover { background-color: #ea580c; }
        .stMarkdown h1 { font-size: 36px; font-weight: bold; text-align: center; }
        .stMarkdown h2 { font-size: 28px; font-weight: bold; }
        .stMarkdown h3 { font-size: 24px; font-weight: bold; }
        .stMarkdown p { font-size: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.title("🏆 AI Badminton Coach")
    st.subheader("⚙️ Settings")
    openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")
    st.write("🔹 AI-powered badminton game analysis")
    st.markdown("---")
    st.write("🛠 Developed for **Cornell AI Hackathon 2025**")
    st.write("📍 Challenge: **AI Sports Evolution**")
    st.write("🎯 **Analyze, Improve, Dominate!** 🏸")

# --- MAIN CONTENT ---
st.title("🏸 AI Badminton Coach")
st.markdown("#### **🚀 Train Smarter, Play Better!**")

# --- VIDEO UPLOAD SECTION ---
st.subheader("🎥 Upload Your Badminton Game Footage")
st.write(
    "Upload your **match video** to receive personalized AI insights on your performance. "
    "Our model will analyze **your shots, movement, and decision-making** to offer **actionable feedback!**"
)

uploaded_file = st.file_uploader("Drag and drop a match video", type=["mp4", "mov", "avi", "mkv"])
if uploaded_file:
    st.video(uploaded_file)
    st.success("✅ Video uploaded successfully! AI analysis will begin shortly.")

# --- CHAT FUNCTIONALITY ---
st.subheader("💬 Ask Your AI Coach")
st.write("🎯 **Ask anything about your game:**")
st.markdown(
    """
    - *What mistakes did I make?*  
    - *How can I improve my footwork?*  
    - *What should I do against aggressive smashes?*  
    - *Was my backhand clear effective?*
    """
)

user_query = st.text_area("Type your question below:", "")
if st.button("⚡ Get AI Feedback"):
    if not openai_api_key.startswith("sk-"):
        st.warning("⚠️ Please enter a valid OpenAI API key!", icon="⚠")
    else:
        with st.spinner("🔍 Analyzing your performance..."):
            model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
            response = model.invoke(user_query)
            st.success("✅ AI Analysis Complete!")
            st.markdown("### **📝 AI Feedback:**")
            st.info(response)

# --- FUTURE FEATURE SECTION ---
with st.expander("🚀 Future Feature: Automatic Video Analysis"):
    st.write(
        "We are actively working on **AI-powered video analysis** that will automatically detect: \n"
        "✔️ Shot types (Smash, Drop, Drive, etc.)  \n"
        "✔️ Player positioning & movement efficiency  \n"
        "✔️ Tactical errors & improvement areas  \n"
        "Stay tuned for updates! 🎾"
    )

# --- FOOTER ---
st.markdown("---")
st.markdown("🏆 *Built for the Cornell AI Hackathon 2025 - AI Sports Evolution Challenge*")
