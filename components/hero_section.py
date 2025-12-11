import streamlit as st

def render_hero():
    """
    Renders the 'Netflix-style' big banner at the top.
    """
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3em; margin-bottom: 0;">🍿 CineMatch AI</h1>
        <p style="font-size: 1.2em; color: #aaa;">
            The world's first <b>Honest Streaming Service</b>.
        </p>
        <div style="background-color: #262730; padding: 15px; border-radius: 10px; display: inline-block; margin-top: 20px;">
            <span style="color: #FF4B4B; font-weight: bold;">Problem:</span> Standard AIs lie. They recommend random movies just to keep you watching.<br>
            <span style="color: #00C851; font-weight: bold;">Solution:</span> We calculate <b>Uncertainty</b>. If we aren't sure, we tell you.
        </div>
    </div>
    <hr style="border-color: #333;">
    """, unsafe_allow_html=True)




"""
CODE EXPLANATION:
1. render_hero():
   - The "Landing Page" component.
   - Uses centered HTML and custom styling to make the tool look like a SaaS product ("CineMatch AI").
   - The "Problem/Solution" box frames the project context immediately for the user (or interviewer).
   - Why: First impressions matter. A clean header makes the project look complete and professional.
"""