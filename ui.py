import streamlit as st

def load_page_style():

    st.set_page_config(page_title="Streamlit AI assistant", page_icon=":material/asterisk:")

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:ital,wght@0,400;1,400&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Newsreader', serif;
        }

        /* Reverse the user row: avatar-slot moves to the right of the bubble */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
            flex-direction: row-reverse;
        }

        /* Hide the user avatar icon */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageAvatarUser"] {
            display: none;
        }


    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        width: fit-content !important;
        margin-left: auto;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: rgba(240, 242, 246, 0.5);
    }

    /* hide the face icon since you don't want a logo on user messages */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageAvatarUser"] {
        display: none;
    }
        </style>
    """, unsafe_allow_html=True)