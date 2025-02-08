import streamlit as st
import openai
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate

# --- Load environment variables ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --- System Image: Professional Badminton Player ---
PRO_SMASH_IMAGE_PATH = "pro_smash_pose.jpg"  # Replace with actual image path
PRO_SMASH_DESCRIPTION = """
This is a professional badminton player executing a perfect smash. Key points:
1. **Racket Preparation**: The racket is fully behind the head, with the elbow high.
2. **Body Rotation**: The player's body is turned sideways, using the core to generate power.
3. **Jump & Contact Point**: The shuttle is hit at the highest point, ensuring a steep angle.
4. **Follow-Through**: The arm fully extends after contact for maximum power.

A proper smash uses core strength, wrist snap, and fast recovery positioning.
"""

# --- LangChain AI Model (Sonnet 3.5) ---
llm = ChatOpenAI(model="anthropic.claude-3.5-sonnet.v2", base_url="https://api.ai.it.cornell.edu")

# --- Function to Compare User's Smash with Professional Reference ---
def analyze_smash_pose(user_query, user_image):
    """Compares the user's uploaded smash pose with a professional player's pose."""

    # Create a structured system prompt with multimodal support
    system_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="You are an AI badminton coach analyzing player smash techniques."),
        SystemMessage(content="Here is a professional player's perfect smash technique for reference:"),
        SystemMessage(content=PRO_SMASH_DESCRIPTION),
        SystemMessage(content={"type": "image_url", "image_url": PRO_SMASH_IMAGE_PATH}),  # Reference image
        HumanMessage(content="Now analyze this player's smash technique:"),
        HumanMessage(content={"type": "image_url", "image_url": user_image})  # User-uploaded image
    ])

    # Get AI response
    response = llm(system_prompt)

    return response.content

# --- Streamlit Web App ---
st.set_page_config(page_title="🏸 AI Badminton Coach", page_icon="🏆", layout="wide")

st.title("🏸 AI Badminton Coach - Smash Pose Analysis")
st.markdown("### Compare your badminton smash pose with a professional player's pose!")

# --- Display Reference Image (Professional Smash) ---
st.subheader("📸 Professional Smash Pose (Reference)")
st.image(PRO_SMASH_IMAGE_PATH, caption="Professional Badminton Smash Pose")
st.markdown(f"**Why is this a good smash pose?**\n\n{PRO_SMASH_DESCRIPTION}")

# --- User Upload Section ---
st.subheader("📸 Upload Your Smash Pose")
user_uploaded_image = st.file_uploader("Upload an image of you smashing", type=["jpg", "png", "jpeg"])

# --- User Input Question ---
user_query = st.text_area("Ask about your smash technique:", "How is my smash compared to the reference?")

# --- Process and Analyze User's Smash ---
if st.button("⚡ Get AI Analysis"):
    if not openai_api_key:
        st.warning("⚠️ Missing API Key! Please check your `.env` file.", icon="⚠")
    elif not user_uploaded_image:
        st.warning("⚠️ Please upload an image of your smash.", icon="⚠")
    else:
        with st.spinner("🔍 Analyzing your technique..."):
            response = analyze_smash_pose(user_query, user_uploaded_image)
            st.success("✅ AI Analysis Complete!")
            st.markdown("### **📝 AI Feedback:**")
            st.info(response)
