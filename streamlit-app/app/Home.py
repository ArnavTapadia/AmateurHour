import streamlit as st
import openai
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from smashdescriptions import smash_descriptions
# --- Load environment variables ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --- System Prompt: Hidden Professional Smash Images with Context ---
SMASH_IMAGES = [
    {"path": "smash_pose_1.jpg", "description": ""},
    {"path": "smash_pose_2.jpg", "description": ""},
    {"path": "smash_pose_3.jpg", "description": ""}
]

SYSTEM_PROMPT_INTRO = """
You are an Olympic-level badminton coach specializing in analyzing player smash techniques.
You will compare a user's smash pose to professional smash examples and provide detailed feedback.

Here are **three professional smash poses** along with descriptions of each phase:
"""

# --- LangChain AI Model (Sonnet 3.5) ---
llm = ChatOpenAI(model="anthropic.claude-3.5-sonnet.v2", base_url="https://api.ai.it.cornell.edu")

# --- Function to Analyze User's Smash Pose ---
def analyze_smash_pose(user_query, user_image):
    """Analyzes the user's uploaded smash pose using hidden system context with images."""

    # Create a structured system prompt with multimodal support
    system_messages = [
        SystemMessage(content=SYSTEM_PROMPT_INTRO)
    ]

    # Add professional smash images and descriptions (hidden from user)
    for img in SMASH_IMAGES:
        system_messages.append(SystemMessage(content={"type": "image_url", "image_url": img["path"]}))
        system_messages.append(SystemMessage(content=img["description"]))

    # Add user's uploaded image for AI analysis
    system_messages.append(HumanMessage(content="Here is the user's smash pose for analysis:"))
    system_messages.append(HumanMessage(content={"type": "image_url", "image_url": user_image}))

    # Create the prompt template
    system_prompt = ChatPromptTemplate.from_messages(system_messages)

    # Get AI response
    response = llm(system_prompt)

    return response.content

# --- Streamlit Web App ---
st.set_page_config(page_title="🏸 AI Badminton Coach", page_icon="🏆", layout="wide")

st.title("🏸 AI Badminton Coach - Smash Pose Analysis")
st.markdown("### Upload your badminton smash pose and get expert AI feedback!")

# --- User Upload Section ---
st.subheader("📸 Upload Your Smash Pose")
user_uploaded_image = st.file_uploader("Upload an image of your smash", type=["jpg", "png", "jpeg"])

# --- User Input Question ---
user_query = st.text_area("Ask about your smash technique:", "How can I improve my smash?")

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
