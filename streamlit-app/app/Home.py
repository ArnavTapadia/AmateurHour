import streamlit as st
import openai
import os
import base64
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate

smash_descriptions = {
    "frontsmashview.png": {
        "title": "Jump Smash Preparation",
        "description": (
            "The player is in mid-air, preparing to execute a jump smash. "
            "The racket arm is drawn back with the elbow positioned high, and the non-racket arm is slightly raised for balance. "
            "The body is rotating, and the player's eyes are likely tracking the shuttle. "
            "The elbow is positioned correctly behind the body, allowing for a full extension during the smash. "
            "The torso rotation generates more power, transferring energy from the core to the racket. "
            "The player has jumped, allowing for a steep downward smash trajectory, which makes the shot harder to return."
        )
    },
    "sidesmashview.png": {
        "title": "Smash Execution",
        "description": (
            "The player is now in the process of striking the shuttle. "
            "His body is fully rotated, and his hitting arm is in motion, about to make contact with the shuttle. "
            "His core and legs are engaged to generate maximum power. "
            "The full-body rotation increases power and speed. "
            "The player’s feet are still off the ground, meaning the smash will have a steep angle, making it harder for the opponent to defend. "
            "His non-racket arm is tucked in, maintaining balance and preventing excess movement."
        )
    },
    "smashexecution.png": {
        "title": "Follow-Through and Power Transfer",
        "description": (
            "The player has completed his swing, and the racket is moving forward with a strong wrist snap. "
            "His eyes are still on the shuttle, ensuring control and accuracy. "
            "His body is slightly leaning forward, indicating good weight transfer. "
            "The wrist snap adds extra speed to the smash, increasing its effectiveness. "
            "The forward body movement ensures momentum is transferred into the shot. "
            "The positioning of his arm and body suggests that he is ready to recover quickly after the shot."
        )
    }
}


# --- Load environment variables ---
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# --- Image Directory and Files ---
SMASH_IMAGE_FOLDER = "streamlit-app/smashhitphotos"
SMASH_IMAGES = [
    {
        "path": os.path.join(SMASH_IMAGE_FOLDER, filename),
        "title": smash_descriptions[filename]["title"],
        "description": smash_descriptions[filename]["description"]
    }
    for filename in smash_descriptions.keys()
]

# --- Function to Convert Local Image to Base64 ---
def encode_image_to_base64(image_path):
    """Encodes an image file to a Base64 string for AI model input."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# --- Convert Images to Base64 ---
for img in SMASH_IMAGES:
    img["base64"] = encode_image_to_base64(img["path"])

# --- System Prompt Introduction (Hidden from User) ---
SYSTEM_PROMPT_INTRO = """
You are an Olympic-level badminton coach specializing in analyzing player smash techniques.
You will compare a user's smash pose to professional smash examples and provide detailed feedback.

Here are three professional smash examples with key descriptions:
"""

# --- LangChain AI Model (Sonnet 3.5) ---
llm = ChatOpenAI(model="anthropic.claude-3.5-sonnet.v2", base_url="https://api.ai.it.cornell.edu")

# --- Function to Analyze User's Smash Pose ---
def analyze_smash_pose(user_query, user_image):
    """Analyzes the user's uploaded smash pose using hidden system context with images."""

    # Create a structured system prompt with multimodal support
    system_messages = [SystemMessage(content=SYSTEM_PROMPT_INTRO)]

    # Add professional smash images and descriptions (Base64 encoded)
    for img in SMASH_IMAGES:
        system_messages.append(SystemMessage(content={"type": "image", "image": img["base64"]}))  # Base64 image
        system_messages.append(SystemMessage(content=f"**{img['title']}**: {img['description']}"))

    # Add user's uploaded image for AI analysis (Convert user image to Base64)
    user_image_base64 = encode_image_to_base64(user_image)

    system_messages.append(HumanMessage(content="Here is the user's smash pose for analysis:"))
    system_messages.append(HumanMessage(content={"type": "image", "image": user_image_base64}))

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
            # Save user-uploaded image temporarily
            user_temp_path = "temp_user_smash.png"
            with open(user_temp_path, "wb") as f:
                f.write(user_uploaded_image.getbuffer())

            # Analyze the image
            response = analyze_smash_pose(user_query, user_temp_path)
            st.success("✅ AI Analysis Complete!")
            st.markdown("### **📝 AI Feedback:**")
            st.info(response)

            # Cleanup temp file
            os.remove(user_temp_path)
