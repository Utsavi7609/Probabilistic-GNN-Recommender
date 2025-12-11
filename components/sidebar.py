import streamlit as st

def render_sidebar(num_users):
    st.sidebar.header("⚙️ Controls")
    
    # User Selection
    user_id = st.sidebar.number_input("User ID", 0, num_users-1, 42)
    
    # The Research Slider
    threshold = st.sidebar.slider(
        "Uncertainty Threshold (σ)", 
        0.0, 3.0, 1.2,
        help="Filter out recommendations where model variance is high."
    )
    
    st.sidebar.markdown("---")
    
    # Cold Start Toggle
    cold_start = st.sidebar.checkbox(
        "Simulate Cold Start", 
        help="Wipes user history to test robustness."
    )
    
    return user_id, threshold, cold_start


"""
CODE EXPLANATION:
1. render_sidebar():
   - This module isolates the "Control Panel" logic to keep main.py clean.
   - Manual ID Input: A 'Developer Tool' allowing you to test specific Edge Cases (e.g., User 42 for Cold Start).
   - Continuous Slider:
     - Allows float values (e.g., 1.2) for fine-grained control over the Sigma threshold.
     - Dynamic Feedback: As you slide, it updates the text (Safe vs Experimental) to guide the user.
   - State Management: When the user changes, we trigger 'del st.session_state['results']' to force a re-calculation.
"""