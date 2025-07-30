import streamlit as st
import time
import json
from difficulty_texts import get_text_by_difficulty
from utils import calculate_accuracy, count_mistakes, calculate_wpm, highlight_mistakes
from streamlit_lottie import st_lottie

st.set_page_config(page_title="TypeRush", layout="wide")

# Load and apply custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to load Lottie animation from a local JSON file
def load_lottiefile(filepath: str):
    
    with open(filepath, "r") as f:
        return json.load(f)

# --- Top Header Section (Centered) ---
st.markdown("<h1 class='main-title'>TypeRush</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline centered'>Test your skills, boost your speed, and conquer the keyboard.</p>", unsafe_allow_html=True)

# Lottie animation and edgy text below the title, also centered
col_empty1, col_lottie_text, col_empty2 = st.columns([1, 2, 1])
with col_lottie_text:
    dance_lottie_json = load_lottiefile("assets/lotties/dance.json")
    if dance_lottie_json:
        st_lottie(dance_lottie_json, height=150, key="dance_top_left")
    st.markdown("<p class='edgy-text-centered'>Ready to test your typing skills?</p>", unsafe_allow_html=True)

# Initialize session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "test_finished" not in st.session_state:
    st.session_state.test_finished = False
if "original_text" not in st.session_state:
    st.session_state.original_text = ""
if "typed_text" not in st.session_state:
    st.session_state.typed_text = ""
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "easy"
if "is_starting" not in st.session_state:
    st.session_state.is_starting = False

# --- Main App Logic ---

# Display "Restart Test" button only after a test has started
if st.session_state.original_text:
    col_empty_res1, col_res_btn, col_empty_res2 = st.columns([1, 2, 1])
    with col_res_btn:
        if st.button("Restart Test", key="main_restart_button"):
            st.session_state.start_time = None
            st.session_state.test_finished = False
            st.session_state.original_text = ""
            st.session_state.typed_text = ""
            st.session_state.last_input = ""
            st.rerun()

# Handle Countdown
if st.session_state.is_starting:
    countdown_placeholder = st.empty()
    for i in range(3, 0, -1):
        countdown_placeholder.markdown(f"<h1 style='text-align: center;'>{i}</h1>", unsafe_allow_html=True)
        time.sleep(1)
    countdown_placeholder.empty()
    st.session_state.start_time = time.time()
    st.session_state.is_starting = False
    st.rerun()

# Display the challenge level selection if no test is active and not starting
if not st.session_state.original_text and not st.session_state.test_finished and not st.session_state.is_starting:
    # Removed the purple cat animation to clean up the layout.
    st.markdown("""
        <div class='cool-statement'>
            
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Choose a challenge level")
    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")
    st.markdown("  ")
    # Adjusted the column layout for more reliable centering of the buttons.
    col_empty_buttons1, col1, col2, col3, col_empty_buttons2 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button("Easy", key="easy_button"):
            st.session_state.difficulty = "easy"
            st.session_state.original_text = get_text_by_difficulty("easy")
            st.session_state.is_starting = True
            st.rerun()
    with col2:
        if st.button("Medium", key="medium_button"):
            st.session_state.difficulty = "medium"
            st.session_state.original_text = get_text_by_difficulty("medium")
            st.session_state.is_starting = True
            st.rerun()
    with col3:
        if st.button("Hard", key="hard_button"):
            st.session_state.difficulty = "hard"
            st.session_state.original_text = get_text_by_difficulty("hard")
            st.session_state.is_starting = True
            st.rerun()

# If test is in progress
if st.session_state.original_text and not st.session_state.test_finished and not st.session_state.is_starting:
    st.markdown("### Start Typing Below ")
    st.markdown(f"**Text to type:** {st.session_state.original_text}")

    typed = st.text_input("start typing here ...", value=st.session_state.typed_text, key="typing_box")
    submitted = False
    
    if typed != st.session_state.last_input:
        st.session_state.typed_text = typed
        st.session_state.last_input = typed
        if st.session_state.start_time is not None:
            submitted = True

    if st.button("Submit"):
        st.session_state.typed_text = typed
        if st.session_state.start_time is not None:
            submitted = True

    if submitted:
        st.session_state.test_finished = True
        end_time = time.time()
        
        acc = calculate_accuracy(st.session_state.original_text, typed)
        mistakes = count_mistakes(st.session_state.original_text, typed)
        wpm = calculate_wpm(typed, st.session_state.start_time, end_time)
        highlighted_text = highlight_mistakes(st.session_state.original_text, typed)

        st.success("Test Finished!")
        
        col_empty_res_metrics1, col1_res, col2_res, col_empty_res_metrics2 = st.columns([1, 1, 2, 1])
        with col1_res:
            st.metric("Time Taken", f"{round(end_time - st.session_state.start_time, 2)}s")
            st.metric("Accuracy", f"{acc}%")
            st.metric("WPM", f"{wpm}")
            st.metric("Mistake", f"{mistakes}")
        
        with col2_res:
            lottie_json = load_lottiefile("assets/lotties/no-inte.json")
            if lottie_json:
                st_lottie(lottie_json, height=300, key="loading")
                
        st.markdown("### Mistake Highlighting:")
        st.markdown("<p style='font-size: 16px; color: grey;'>Red text indicates a mistake.</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px;'>{highlighted_text}</p>", unsafe_allow_html=True)

st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("  ")
st.markdown("### Usage Information")
st.markdown("""
Since this application is built with Streamlit, which doesn't support real-time updates, you need to trigger a server rerun to submit your text.

- To submit your finished typing test, please **press `Enter`** or **click the `Submit` button.**
- If you wish to start over, you can use the **`Restart Test`** button.
""")
st.markdown("  ")

st.markdown("  ")
st.markdown("  ")

st.markdown("  ")
st.markdown("  ")
st.markdown("  ")

st.markdown("  ")
st.markdown("  ")

st.markdown("  ")
st.markdown("  ")        
st.markdown("<p class='footer'>Designed and developed by Zain</p>", unsafe_allow_html=True)