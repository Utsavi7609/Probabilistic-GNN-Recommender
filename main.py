# # import streamlit as st
# # import streamlit.components.v1 as components

# # # Import our modules
# # from src.model_loader import load_system
# # from src.inference import run_inference, calculate_risk_reduction
# # from src.visualizations import render_interactive_graph, render_confidence_bar
# # from components.sidebar import render_sidebar
# # from components.analytics_dashboard import render_analytics

# # # Page Setup
# # st.set_page_config(page_title="GNN Research Engine", layout="wide", page_icon="🧬")

# # # 1. Load System
# # model, data, cfg = load_system()

# # # 2. Sidebar
# # user_id, threshold, cold_start = render_sidebar(data['user'].num_nodes)

# # # 3. Main Title
# # st.title(f"{cfg['app_name']} v2.0")
# # st.markdown(f"**Target:** User {user_id} | **Mode:** {'🧪 Cold Start' if cold_start else 'Standard'}")

# # # 4. Run Logic
# # if st.button("🚀 Run Analysis", type="primary"):
    
# #     with st.spinner("Running GraphSAGE Inference..."):
# #         # Run the Brain
# #         df = run_inference(model, data, user_id, cold_start)
        
# #         # Calculate Metrics
# #         risk_reduction = calculate_risk_reduction(df, threshold)
        
# #         # Filter Data
# #         safe = df[df['sigma'] < threshold].sort_values('rating', ascending=False)
# #         risky = df[df['sigma'] >= threshold].sort_values('rating', ascending=False)

# #     # 5. Display Tabs
# #     tab1, tab2, tab3 = st.tabs(["📋 Recommendations", "🕸️ Interactive Graph", "📈 Metrics"])
    
# #     with tab1:
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             st.subheader("✅ Safe Bets")
# #             for _, row in safe.head(5).iterrows():
# #                 bar = render_confidence_bar(row['sigma'])
# #                 st.markdown(f"**Movie {int(row['movie_id'])}** | {bar} | Rating: {row['rating']:.1f}", unsafe_allow_html=True)
# #         with c2:
# #             st.subheader("⚠️ Risky / Uncertain")
# #             st.dataframe(risky[['movie_id', 'rating', 'sigma']].head(5), use_container_width=True)

# #     with tab2:
# #         st.info("Drag nodes to rearrange.")
# #         html = render_interactive_graph(data, user_id, df)
# #         components.html(html, height=500, scrolling=True)
        
# #     with tab3:
# #         m1, m2 = st.columns(2)
# #         m1.metric("Risk Reduction", f"{risk_reduction:.1f}%", help="Recommendations blocked by uncertainty filter")
# #         m2.metric("Total Catalog", len(df))
# #         render_analytics(df, threshold)

# # else:
# #     st.info("Click 'Run Analysis' to start.")


# import streamlit as st
# import time

# # Import our modular system
# from src.model_loader import load_system
# from src.inference import run_inference, calculate_risk_reduction
# from src.mock_database import MockDatabase
# from src.explanation import explain_prediction
# from src.visualizations import render_interactive_graph
# from components.movie_card import render_movie_card

# # -----------------------------------------------------------------------------
# # 1. SETUP & CONFIG
# # -----------------------------------------------------------------------------
# st.set_page_config(page_title="CineMatch AI", layout="wide", page_icon="🍿")

# # Load System
# model, data, cfg = load_system()
# num_users = data['user'].num_nodes
# num_movies = data['movie'].num_nodes

# # Initialize Mock DB
# if 'db' not in st.session_state:
#     st.session_state.db = MockDatabase(num_users, num_movies)
# db = st.session_state.db

# # -----------------------------------------------------------------------------
# # 2. HERO SECTION (THE "LAYMAN" WELCOME)
# # -----------------------------------------------------------------------------
# st.title("🍿 CineMatch AI")
# st.markdown("""
# ### The Streaming Service that **Doesn't Lie**.
# Most algorithms pretend they know you perfectly. We don't. 
# We tell you what we're **Sure** about, and what's a **Guess**.
# """)

# # -----------------------------------------------------------------------------
# # 3. PROFILE SELECTOR (GAMIFICATION)
# # -----------------------------------------------------------------------------
# st.markdown("---")
# col1, col2, col3, col4, col5 = st.columns(5)
# personas = [0, 1, 2, 3, 42]

# # Simple state management for selected user
# if 'selected_user' not in st.session_state:
#     st.session_state.selected_user = 42

# def set_user(uid):
#     st.session_state.selected_user = uid

# # Render clickable profile buttons
# for i, col in enumerate([col1, col2, col3, col4, col5]):
#     pid = personas[i]
#     profile = db.get_user_profile(pid)
#     if col.button(f"{profile['avatar']} {profile['name']}", key=f"btn_{pid}"):
#         set_user(pid)

# # Display Current Profile
# curr_profile = db.get_user_profile(st.session_state.selected_user)
# st.success(f"**Viewing as:** {curr_profile['name']} | **Bio:** {curr_profile['bio']}")

# # -----------------------------------------------------------------------------
# # 4. CONTROLS (THE "TRUST" SLIDER)
# # -----------------------------------------------------------------------------
# st.sidebar.header("🎛️ Algorithm Settings")
# st.sidebar.write("How adventurous are you feeling?")

# trust_level = st.sidebar.select_slider(
#     "Trust Level",
#     options=["Only Safe Bets", "Balanced", "I'm Feeling Lucky"],
#     value="Balanced"
# )

# # Map layman terms to scientific Thresholds
# threshold_map = {"Only Safe Bets": 0.5, "Balanced": 1.2, "I'm Feeling Lucky": 3.0}
# threshold = threshold_map[trust_level]

# # -----------------------------------------------------------------------------
# # 5. EXECUTION ENGINE
# # -----------------------------------------------------------------------------
# if st.button("🎬 Find My Movies", type="primary"):
    
#     with st.spinner(f"Analyzing viewing history for {curr_profile['name']}..."):
#         time.sleep(0.5) # Fake loading for UX
        
#         # 1. Cold Start Check
#         is_cold_start = (st.session_state.selected_user == 42)
        
#         # 2. Run GNN Inference
#         raw_df = run_inference(model, data, st.session_state.selected_user, is_cold_start)
        
#         # 3. Enrich with "Fake" Metadata (Titles, Genres)
#         full_df = db.enrich_recommendations(raw_df)
        
#         # 4. Filter Logic
#         safe_movies = full_df[full_df['sigma'] < threshold].sort_values('rating', ascending=False)
#         risky_movies = full_df[full_df['sigma'] >= threshold].sort_values('rating', ascending=False)
        
#         # 5. Metrics
#         reduction = calculate_risk_reduction(full_df, threshold)

#     # -------------------------------------------------------------------------
#     # 6. RESULTS INTERFACE
#     # -------------------------------------------------------------------------
#     tab_home, tab_explain, tab_graph = st.tabs(["📺 Home Feed", "🤖 AI Explanation", "🕸️ Network View"])

#     # --- TAB 1: THE NETFLIX FEED ---
#     with tab_home:
#         c1, c2 = st.columns([2, 1])
        
#         with c1:
#             st.subheader(f"Top Picks for {curr_profile['name']}")
#             if len(safe_movies) == 0:
#                 st.warning("No safe bets found! Try increasing your risk tolerance.")
#             else:
#                 for _, row in safe_movies.head(5).iterrows():
#                     # Generate natural language explanation
#                     exp_text, _ = explain_prediction(row['rating'], row['sigma'], row['genre'], 0 if is_cold_start else 10)
#                     render_movie_card(row, exp_text)
                    
#         with c2:
#             st.subheader("⚠️ Filtered Out")
#             st.caption("We hid these because we aren't sure you'll like them.")
#             for _, row in risky_movies.head(5).iterrows():
#                 st.markdown(f"❌ **{row['title']}** (Uncertainty: {row['sigma']:.2f})")
                
#     # --- TAB 2: EXPLAINABLE AI ---
#     with tab_explain:
#         st.subheader("Why did we make these choices?")
        
#         col_a, col_b = st.columns(2)
#         with col_a:
#             st.metric("Risk Filter Active", f"{reduction:.1f}%", help="Percent of catalog hidden due to uncertainty")
#         with col_b:
#             st.metric("Algorithm Confidence", f"{trust_level}")
            
#         st.markdown(f"""
#         **Analysis for {curr_profile['name']}:**
#         - **History:** We found viewing data for this user.
#         - **Preference:** Strong affinity for **{curr_profile['fav_genre']}**.
#         - **Uncertainty:** The GNN detected high variance in "Comedy" movies for this profile, so we suppressed them.
#         """)

#     # --- TAB 3: GRAPH VIEW ---
#     with tab_graph:
#         st.info("Visualizing your 'Taste Neighborhood'. Nodes = Movies, Center = You.")
#         # We pass the 'full_df' which now has titles!
#         html = render_interactive_graph(data, st.session_state.selected_user, full_df)
#         import streamlit.components.v1 as components
#         components.html(html, height=500)


import streamlit as st
import time
import pandas as pd

# Import Modules
from src.model_loader import load_system
from src.inference import run_inference
from src.mock_database import MockDatabase
from src.explanation import explain_prediction
from src.visualizations import render_interactive_graph
from src.analytics import calculate_risk_reduction, render_distribution_plot

# Import UI Components
from components.movie_card import render_movie_card
from components.hero_section import render_hero
from components.chatbot import render_chatbot
from components.sidebar import render_sidebar  # We will manually build sidebar in main for custom slider

# 1. PAGE CONFIG
st.set_page_config(page_title="CineMatch AI", layout="wide", page_icon="🍿")

# 2. LOAD SYSTEM
model, data, cfg = load_system()
num_users = data['user'].num_nodes
num_movies = data['movie'].num_nodes

# Init Database
if 'db' not in st.session_state:
    st.session_state.db = MockDatabase(num_users, num_movies)
db = st.session_state.db

# Init User State
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = 42  # Default to "New Guy"

# ---------------------------------------------------------
# 3. SIDEBAR (Continuous Slider Fix)
# ---------------------------------------------------------
st.sidebar.header("🎛️ AI Controls")

# A. User Selector (Hidden in sidebar for power users)
st.sidebar.subheader("Debug Profile")
# We allow manual ID entry OR profile selection from main page
manual_id = st.sidebar.number_input("Manual User ID", 0, num_users-1, st.session_state.selected_user)
if manual_id != st.session_state.selected_user:
    st.session_state.selected_user = manual_id

# B. CONTINUOUS SLIDER (Your Request)
st.sidebar.markdown("---")
st.sidebar.subheader("Uncertainty Tolerance")
threshold = st.sidebar.slider(
    "Sigma Cutoff (σ)", 
    min_value=0.0, 
    max_value=3.0, 
    value=1.2, 
    step=0.1,
    help="Lower = Safer Bets. Higher = More Discovery."
)

# Dynamic Label based on Slider
if threshold < 0.8:
    st.sidebar.success("Mode: Ultra Safe 🛡️")
elif threshold < 1.8:
    st.sidebar.info("Mode: Balanced ⚖️")
else:
    st.sidebar.warning("Mode: Experimental 🧪")

# ---------------------------------------------------------
# 4. MAIN PAGE LAYOUT
# ---------------------------------------------------------
render_hero()  # The Big Welcome Banner

# A. PROFILE SELECTOR
st.subheader("👤 Who is watching?")
cols = st.columns(5)
personas = [0, 1, 2, 3, 42]

for i, col in enumerate(cols):
    pid = personas[i]
    profile = db.get_user_profile(pid)
    # Highlight the selected button
    is_selected = (pid == st.session_state.selected_user)
    type = "primary" if is_selected else "secondary"
    
    if col.button(f"{profile['avatar']} {profile['name']}", key=f"btn_{pid}", type=type, use_container_width=True):
        st.session_state.selected_user = pid
        st.rerun()

# Show current bio
curr_profile = db.get_user_profile(st.session_state.selected_user)
st.info(f"**Current Context:** {curr_profile['bio']} (ID: {st.session_state.selected_user})")

# ---------------------------------------------------------
# 5. EXECUTION (FIXED: SAVES STATE)
# ---------------------------------------------------------
# We run if the button is clicked OR if we already have data in memory
if st.button("🚀 Generate Personalization", type="primary", use_container_width=True) or 'results' in st.session_state:
    
    # STEP A: CALCULATE (Only if we don't have data yet, or if button was just clicked)
    # We check if 'results' is missing to avoid re-running GNN on every slider move/chat interaction
    if 'results' not in st.session_state or st.session_state.get('trigger_rerun', False):
        with st.spinner("Running GraphSAGE Inference..."):
            time.sleep(0.5) # UX pause
            
            # Cold Start Logic
            is_cold_start = (st.session_state.selected_user == 42)
            
            # Run Inference (The Heavy Math)
            raw_df = run_inference(model, data, st.session_state.selected_user, is_cold_start)
            full_df = db.enrich_recommendations(raw_df)
            
            # Save to Memory
            st.session_state['results'] = {
                'full_df': full_df,
                'is_cold_start': is_cold_start
            }
            # Reset trigger
            st.session_state['trigger_rerun'] = False

    # STEP B: RETRIEVE FROM MEMORY
    results = st.session_state['results']
    full_df = results['full_df']
    is_cold_start = results['is_cold_start']

    # STEP C: FILTERING (Runs fast every time you move the slider)
    # We re-filter the saved dataframe based on the NEW threshold from sidebar
    safe_movies = full_df[full_df['sigma'] < threshold].sort_values('rating', ascending=False)
    risky_movies = full_df[full_df['sigma'] >= threshold].sort_values('rating', ascending=False)
    reduction = calculate_risk_reduction(full_df, threshold)
# ---------------------------------------------------------
    # 6. DASHBOARD INTERFACE (Split Layout)
    # ---------------------------------------------------------
    # Create two columns: 70% for Data, 30% for Chatbot
    col_data, col_chat = st.columns([7, 3])
    
    # --- LEFT COLUMN: DATA TABS ---
    with col_data:
        t1, t2, t3 = st.tabs(["📺 Recommendations", "🕸️ Graph Logic", "📊 Analytics"])
        
        # TAB 1: CARDS
        with t1:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("✅ Top Picks")
                if safe_movies.empty:
                    st.error("No movies met your Safety Standard. Increase the slider!")
                for _, row in safe_movies.head(5).iterrows():
                    exp, _ = explain_prediction(row['rating'], row['sigma'], row['genre'], 0 if is_cold_start else 10)
                    render_movie_card(row, exp)
            with c2:
                st.subheader("⚠️ Filtered")
                for _, row in risky_movies.head(5).iterrows():
                    st.markdown(f"**{row['title']}**\n\nUncertainty: `{row['sigma']:.2f}`")
                    st.progress(min(1.0, row['sigma']/3.0))

        # TAB 2: PYVIS GRAPH
        with t2:
            st.markdown("#### Your Taste Cluster")
            html = render_interactive_graph(data, st.session_state.selected_user, full_df)
            import streamlit.components.v1 as components
            components.html(html, height=600)

        # TAB 3: ANALYTICS
        with t3:
            m1, m2 = st.columns(2)
            m1.metric("Risk Reduction", f"{reduction:.1f}%", delta="Bad recs avoided")
            m2.metric("Catalog Scanned", f"{len(full_df)}")
            render_distribution_plot(full_df, threshold)

    # --- RIGHT COLUMN: PERMANENT AI COPILOT ---
    with col_chat:
        st.markdown("### 🤖 AI Copilot")
        st.caption("I analyze the data on the left in real-time.")
        
        # Render the chatbot here (Always visible!)
        render_chatbot(full_df)


"""
CODE EXPLANATION:
1. Page Layout: Sets up the 'Split Screen' (Data on Left, Chat on Right).
2. State Management ('results'):
   - We store the GNN results in 'st.session_state'.
   - This prevents the app from re-calculating the math every time you type in the chat box.
   - The 'if button or results' logic ensures the data persists.
3. Sidebar Logic:
   - The 'Threshold Slider' controls the variable 'threshold'.
   - The filtering logic (df[df.sigma < threshold]) runs in real-time.
   - As you move the slider, the 'safe_movies' list updates instantly.
4. Integration:
   - This file ties everything together: loading the model, getting user input, running inference, and rendering the components (Cards, Graph, Chat).
"""