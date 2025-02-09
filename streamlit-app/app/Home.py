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

# --- Image Directory and Files ---
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
        ),
        "url": "https://github.com/ArnavTapadia/AmateurHour/blob/a2fd8c92af4ddfff4b2b2172ac0231c95992dd69/streamlit-app/smashhitphotos/frontsmashview.png"  # Replace with your actual image URL
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
        ),
        "url": "https://github.com/ArnavTapadia/AmateurHour/blob/a2fd8c92af4ddfff4b2b2172ac0231c95992dd69/streamlit-app/smashhitphotos/sidesmashview.png"  # Replace with your actual image URL
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
        ),
        "url": "https://github.com/ArnavTapadia/AmateurHour/blob/a2fd8c92af4ddfff4b2b2172ac0231c95992dd69/streamlit-app/smashhitphotos/smashexecution.png"  # Replace with your actual image URL
    }
}

# --- System Prompt Introduction (Hidden from User) ---
SYSTEM_PROMPT_INTRO = """
You are an Olympic-level badminton coach specializing in analyzing player smash techniques.
You will compare a user's smash pose to professional smash examples and provide detailed feedback.

Here are three professional smash examples with key descriptions:
"""

# --- LangChain AI Model (Sonnet 3.5) ---
llm = ChatOpenAI(model="anthropic.claude-3.5-sonnet.v2", base_url="https://api.ai.it.cornell.edu")

# --- Function to Analyze User's Smash Pose ---
def analyze_smash_pose(user_query, user_image_url):
    """Analyzes the user's uploaded smash pose using hidden system context with image descriptions."""
    # Prepare the system messages
    system_messages = [SystemMessage(content=SYSTEM_PROMPT_INTRO)]
    
    # Add professional smash descriptions and image URLs
    for filename, details in smash_descriptions.items():
        system_messages.append(SystemMessage(content=f"**{details['title']}**: {details['description']}"))
        system_messages.append(SystemMessage(content=f"Image URL: {details['url']}"))

    # Add user's uploaded image for AI analysis
    system_messages.append(HumanMessage(content="Here is the user's smash pose for analysis:"))
    system_messages.append(HumanMessage(content=f"Image URL: {user_image_url}"))

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
            # Simulate hosting the user-uploaded image by saving it temporarily
            user_temp_path = "temp_user_smash.png"
            with open(user_temp_path, "wb") as f:
                f.write(user_uploaded_image.getbuffer())

            # Simulate an image URL for user-uploaded image (replace this with an actual hosting service)
            user_image_url = "https://example.com/uploaded_user_image.png"  # Replace with hosted URL

            # Analyze the image
            response = analyze_smash_pose(user_query, user_image_url)
            st.success("✅ AI Analysis Complete!")
            st.markdown("### **📝 AI Feedback:**")
            st.info(response)

            # Cleanup temp file
            os.remove(user_temp_path)
