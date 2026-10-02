import base64

import streamlit as st
from google import genai

from prompts import (
    SYSTEM_PROMPT,
    IMAGE_ANALYSIS_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
    QUESTION_GENERATION_PROMPT,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📚",
    layout="centered",
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "gemini-3.8-flash"

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_gemini_client():

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


client = get_gemini_client()


# ============================================================
# SESSION STATE
# ============================================================

if "onboarded" not in st.session_state:

    st.session_state.onboarded = False


if "name" not in st.session_state:

    st.session_state.name = ""


if "messages" not in st.session_state:

    st.session_state.messages = []


if "last_interaction_id" not in st.session_state:

    st.session_state.last_interaction_id = None


# ============================================================
# RENDER MESSAGE
# ============================================================

def render_message(message):

    with st.chat_message(message["role"]):

        if message["kind"] == "text":

            st.markdown(
                message["content"]
            )

        elif message["kind"] == "image":

            st.image(
                message["content"],
                use_container_width=True,
            )


# ============================================================
# ADD MESSAGE
# ============================================================

def add_message(
    role,
    kind,
    content,
):

    message = {
        "role": role,
        "kind": kind,
        "content": content,
    }

    st.session_state.messages.append(
        message
    )

    render_message(message)


# ============================================================
# GEMINI REQUEST
# ============================================================

def ask_gemini(input_parts):

    try:

        # ----------------------------------------------------
        # FIRST MESSAGE
        # ----------------------------------------------------

        if (
            st.session_state.last_interaction_id
            is None
        ):

            response = client.interactions.create(

                model=MODEL_NAME,

                input=input_parts,

                system_instruction=SYSTEM_PROMPT,
            )

        # ----------------------------------------------------
        # FOLLOW-UP MESSAGE
        # ----------------------------------------------------

        else:

            response = client.interactions.create(

                model=MODEL_NAME,

                input=input_parts,

                previous_interaction_id=(
                    st.session_state.last_interaction_id
                ),

                system_instruction=SYSTEM_PROMPT,
            )


        # ----------------------------------------------------
        # SAVE CONVERSATION ID
        # ----------------------------------------------------

        st.session_state.last_interaction_id = (
            response.id
        )


        # ----------------------------------------------------
        # RETURN AI RESPONSE
        # ----------------------------------------------------

        if response.output_text:

            return response.output_text


        return (
            "I couldn't generate a response. "
            "Please try again."
        )


    except Exception as error:

        return (
            "### ⚠️ Gemini Error\n\n"
            f"`{error}`\n\n"
            "Please check your API key, model availability, "
            "and internet connection."
        )


# ============================================================
# ONBOARDING
# ============================================================

if not st.session_state.onboarded:

    st.title("📚 Snap & Study")

    st.caption(
        "Snap it. Understand it. Learn it."
    )

    st.markdown(
        """
        ### 🤖 Your AI Study Assistant

        Upload a photo of your study material and ask questions
        about it.

        **Supports:**

        📖 Textbooks  
        📝 Notes  
        ✍️ Handwriting  
        🧮 Mathematics  
        📊 Diagrams  
        💻 Programming  
        📄 Question Papers
        """
    )

    st.divider()

    with st.form("onboarding_form"):

        name = st.text_input(
            "Enter your name"
        )

        submitted = st.form_submit_button(
            "Start Learning 🚀",
            use_container_width=True,
        )

    if submitted:

        if not name.strip():

            st.warning(
                "Please enter your name."
            )

        else:

            st.session_state.name = (
                name.strip()
            )

            st.session_state.onboarded = True

            st.rerun()

    st.stop()


# ============================================================
# HEADER
# ============================================================

col1, col2 = st.columns(
    [6, 1]
)


with col1:

    st.title("📚 Snap & Study")

    st.caption(
        f"Welcome, {st.session_state.name}!"
    )


with col2:

    if st.button(
        "🔄",
        help="Start a new conversation",
    ):

        st.session_state.messages = []

        st.session_state.last_interaction_id = None

        st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧠 Study Tools")

    st.write(
        "Upload an image first, then use these tools."
    )

    st.divider()

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    if st.button(
        "🔍 Analyze Image",
        use_container_width=True,
    ):

        with st.spinner(
            "Analyzing... 🧠"
        ):

            answer = ask_gemini(
                [
                    {
                        "type": "text",
                        "text": IMAGE_ANALYSIS_PROMPT,
                    }
                ]
            )

        add_message(
            "assistant",
            "text",
            answer,
        )


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    if st.button(
        "📝 Summarize",
        use_container_width=True,
    ):

        with st.spinner(
            "Creating summary... 📝"
        ):

            answer = ask_gemini(
                [
                    {
                        "type": "text",
                        "text": SUMMARY_REQUEST_PROMPT,
                    }
                ]
            )

        add_message(
            "assistant",
            "text",
            answer,
        )


    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    if st.button(
        "❓ Generate Questions",
        use_container_width=True,
    ):

        with st.spinner(
            "Generating questions... ❓"
        ):

            answer = ask_gemini(
                [
                    {
                        "type": "text",
                        "text": QUESTION_GENERATION_PROMPT,
                    }
                ]
            )

        add_message(
            "assistant",
            "text",
            answer,
        )


    st.divider()

    st.markdown(
        """
        ### 💡 Try asking

        **Explain this simply.**

        **Solve this step by step.**

        **Summarize this page.**

        **Give me important questions.**

        **Explain this diagram.**

        **Translate this into Telugu.**
        """
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    render_message(message)


# ============================================================
# WELCOME MESSAGE
# ============================================================

if not st.session_state.messages:

    welcome_message = (
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        )
    )

    add_message(
        "assistant",
        "text",
        welcome_message,
    )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask something or upload a study image...",
    accept_file=True,
    file_type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
)


# ============================================================
# PROCESS USER INPUT
# ============================================================

if user_input:

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text.strip()

    input_parts = []


    # ========================================================
    # IMAGE
    # ========================================================

    if photo is not None:

        photo_bytes = photo.getvalue()

        # Show image in chat
        add_message(
            "user",
            "image",
            photo_bytes,
        )

        # Convert image to base64
        image_base64 = base64.b64encode(
            photo_bytes
        ).decode("utf-8")


        # Add image to Gemini input
        input_parts.append(
            {
                "type": "image",
                "data": image_base64,
                "mime_type": photo.type,
            }
        )


    # ========================================================
    # TEXT
    # ========================================================

    if text:

        add_message(
            "user",
            "text",
            text,
        )

        input_parts.insert(
            0,
            {
                "type": "text",
                "text": text,
            },
        )


    # ========================================================
    # IMAGE WITHOUT TEXT
    # ========================================================

    elif photo is not None:

        input_parts.insert(
            0,
            {
                "type": "text",
                "text": IMAGE_ANALYSIS_PROMPT,
            },
        )


    # ========================================================
    # SEND TO GEMINI
    # ========================================================

    if input_parts:

        with st.spinner(
            "Thinking... 🧠"
        ):

            answer = ask_gemini(
                input_parts
            )

        add_message(
            "assistant",
            "text",
            answer,
        )