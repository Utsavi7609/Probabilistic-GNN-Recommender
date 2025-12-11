# # # import streamlit as st
# # # import random

# # # def render_chatbot():
# # #     st.subheader("💬 Ask the AI")
# # #     st.caption("I can explain how I make decisions.")

# # #     # Simple simulated chat interface
# # #     if "messages" not in st.session_state:
# # #         st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me why I recommended a movie, or how my Uncertainty Engine works."}]

# # #     # Display chat history
# # #     for msg in st.session_state.messages:
# # #         with st.chat_message(msg["role"]):
# # #             st.write(msg["content"])

# # #     # User Input
# # #     if prompt := st.chat_input("Ask a question..."):
# # #         st.session_state.messages.append({"role": "user", "content": prompt})
# # #         with st.chat_message("user"):
# # #             st.write(prompt)

# # #         # LOGIC: Simple Keyword Matching (Rule-Based)
# # #         prompt_lower = prompt.lower()
# # #         if "why" in prompt_lower and "recommend" in prompt_lower:
# # #             response = "I look at the graph connections. If you watched 'Inception', and 'Inception' is connected to 'Interstellar' in my database, I recommend it!"
# # #         elif "uncertainty" in prompt_lower or "sigma" in prompt_lower:
# # #             response = "Uncertainty (Sigma) is my 'Doubt Score'. If I haven't seen enough data about a specific genre for you, my Sigma goes up."
# # #         elif "cold start" in prompt_lower:
# # #             response = "Cold Start happens when a new user joins. I have no history for them, so I rely on average global trends until they rate a movie."
# # #         else:
# # #             response = "That's a great question! Basically, I use a Graph Neural Network (GNN) to find patterns in 100,000+ ratings."

# # #         st.session_state.messages.append({"role": "assistant", "content": response})
# # #         with st.chat_message("assistant"):
# # #             st.write(response)

# # import streamlit as st
# # import pandas as pd

# # def render_chatbot(current_recommendations_df):
# #     """
# #     A 'Context-Aware' Chatbot.
# #     It can read the current recommendations table to answer specific questions.
# #     """
# #     st.subheader("💬 AI Analyst")
# #     st.caption("Ask me about specific movies or my decision logic.")

# #     # Initialize Chat History
# #     if "messages" not in st.session_state:
# #         st.session_state.messages = [
# #             {"role": "assistant", "content": "I've analyzed the graph. Ask me 'Why did you pick Movie 100?' or 'How sure are you?'"}
# #         ]

# #     # Display Chat History
# #     for msg in st.session_state.messages:
# #         with st.chat_message(msg["role"]):
# #             st.write(msg["content"])

# #     # User Input
# #     if prompt := st.chat_input("Ask a question..."):
# #         # 1. User Message
# #         st.session_state.messages.append({"role": "user", "content": prompt})
# #         with st.chat_message("user"):
# #             st.write(prompt)

# #         # 2. AI Logic (The "Smart" Part)
# #         response = generate_smart_response(prompt, current_recommendations_df)

# #         # 3. AI Response
# #         st.session_state.messages.append({"role": "assistant", "content": response})
# #         with st.chat_message("assistant"):
# #             st.write(response)

# # def generate_smart_response(prompt, df):
# #     """
# #     Parses the user prompt and looks up data in the DataFrame.
# #     """
# #     prompt = prompt.lower()
    
# #     # CASE A: Asking about a specific movie ID (e.g., "Why 500?")
# #     # We look for numbers in the prompt
# #     import re
# #     movie_id_match = re.search(r'\d+', prompt)
    
# #     if movie_id_match:
# #         mid = int(movie_id_match.group())
# #         # Check if this movie is in our current recommendation list
# #         movie_row = df[df['movie_id'] == mid]
        
# #         if not movie_row.empty:
# #             row = movie_row.iloc[0]
# #             sigma = row['sigma']
# #             rating = row['rating']
            
# #             # Dynamic Explanation
# #             if sigma < 0.8:
# #                 confidence = "extremely high confidence"
# #                 reason = "it is tightly clustered with your viewing history"
# #             else:
# #                 confidence = "low confidence (Experimental)"
# #                 reason = "it is a bit outside your usual genres, but trending"
                
# #             return (f"**Analysis for Movie {mid}:**\n"
# #                     f"- I predicted a rating of **{rating:.2f}/5.0**.\n"
# #                     f"- My uncertainty is **{sigma:.2f}**, which means I have {confidence}.\n"
# #                     f"- I picked this because {reason}.")
# #         else:
# #             return f"Movie {mid} isn't in the current top list, so I can't give you specific details right now."

# #     # CASE B: General Questions
# #     if "why" in prompt and "recommend" in prompt:
# #         return "I use a Graph Neural Network (GNN). I look at the movies you liked (Green Nodes) and find other movies (Blue Nodes) that are mathematically close to them in the embedding space."
    
# #     if "uncertainty" in prompt or "sigma" in prompt:
# #         return ("Sigma (σ) represents my standard deviation.\n"
# #                 "- **Low Sigma (<0.8):** I have lots of data confirming this match.\n"
# #                 "- **High Sigma (>1.5):** I am guessing based on weak connections.")
        
# #     if "cold start" in prompt:
# #         return "Cold Start is when a user has no history. In that case, I rely on the 'Bias' term of my model—essentially recommending universally popular items until you rate something."

# #     # Fallback
# #     return "I can explain my logic! Try asking 'Why did you recommend Movie [ID]?' or 'What is Sigma?'"


# import streamlit as st
# import pandas as pd
# import re

# def render_chatbot(current_recommendations_df):
#     """
#     A 'Context-Aware' Chatbot.
#     It can read the current recommendations table to answer specific questions.
#     """
#     # Initialize Chat History
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             {"role": "assistant", "content": "I'm your Copilot. Ask me 'How does the graph work?' or 'Why Movie 45?'"}
#         ]

#     # Display Chat History
#     for msg in st.session_state.messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # User Input
#     if prompt := st.chat_input("Ask a question..."):
#         # 1. User Message
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         # 2. AI Logic
#         response = generate_smart_response(prompt, current_recommendations_df)

#         # 3. AI Response
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         with st.chat_message("assistant"):
#             st.write(response)

# def generate_smart_response(prompt, df):
#     """
#     Parses the user prompt and looks up data in the DataFrame.
#     """
#     prompt_lower = prompt.lower()
    
#     # CASE A: Asking about a specific movie ID (e.g., "Why 500?")
#     movie_id_match = re.search(r'\d+', prompt_lower)
    
#     if movie_id_match:
#         mid = int(movie_id_match.group())
#         movie_row = df[df['movie_id'] == mid]
        
#         if not movie_row.empty:
#             row = movie_row.iloc[0]
#             sigma = row['sigma']
#             rating = row['rating']
            
#             if sigma < 0.8:
#                 confidence = "extremely high confidence"
#                 reason = "it is tightly clustered with your viewing history"
#             else:
#                 confidence = "low confidence (Experimental)"
#                 reason = "it is a bit outside your usual genres, but trending"
                
#             return (f"**Analysis for Movie {mid}:**\n"
#                     f"- Predicted Rating: **{rating:.2f}/5.0**\n"
#                     f"- Uncertainty (Sigma): **{sigma:.2f}** ({confidence})\n"
#                     f"- Reason: {reason}.")
#         else:
#             return f"Movie {mid} isn't in the current top list. I only analyze the active recommendations."

#     # CASE B: Graph / Network Logic
#     if any(word in prompt_lower for word in ["graph", "network", "nodes", "edges", "how does it work"]):
#         return ("**How the Graph Works:**\n"
#                 "- **Nodes:** Every user and movie is a dot (Node).\n"
#                 "- **Edges:** If you rate a movie, we draw a line (Edge).\n"
#                 "- **The Math:** I look at your neighbors. If you are connected to 'Action Andy', and he liked 'John Wick', I assume you might like it too!")

#     # CASE C: General Concepts
#     if "sigma" in prompt_lower or "uncertainty" in prompt_lower:
#         return ("**Sigma (σ)** is my 'Doubt Score'.\n"
#                 "- **Low (<0.8):** I have lots of data confirming this match.\n"
#                 "- **High (>1.5):** I am guessing based on weak connections.")
        
#     if "cold start" in prompt_lower:
#         return "Cold Start is when a new user joins with zero history. I rely on global popularity trends until they rate their first movie."

#     # CASE D: Smart Fallback (Echoes the user's topic)
#     # This extract common stop words to guess the "topic"
#     ignored_words = ["what", "is", "the", "how", "why", "are", "you", "tell", "me", "about", "a", "an"]
#     keywords = [w for w in prompt.split() if w.lower() not in ignored_words]
    
#     topic = keywords[0] if keywords else "that"
    
#     return (f"I understand you are asking about **'{topic}'**, but my database is strictly limited to Movie Ratings and Graph Uncertainty metrics.\n\n"
#             f"I cannot provide outside information about **{topic}**. Try asking me about 'Sigma' or specific Movie IDs!")


import streamlit as st
import pandas as pd
import re

def render_chatbot(current_recommendations_df):
    """
    A 'Context-Aware' Chatbot.
    It can read the current recommendations table to answer specific questions.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "I'm your Copilot. Try asking: 'What is Sigma and how does Cold Start work?'"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # AI Logic
        response = generate_smart_response(prompt, current_recommendations_df)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

def generate_smart_response(prompt, df):
    """
    Parses the user prompt and looks up data in the DataFrame.
    """
    prompt_lower = prompt.lower()
    responses = [] # We will collect multiple answers here
    
    # ------------------------------------------------------------------
    # PART 1: Look for Movie IDs (Handles multiple IDs like "Why 500 and 600?")
    # ------------------------------------------------------------------
    movie_ids = re.findall(r'\d+', prompt_lower) # Finds ALL numbers
    
    if movie_ids:
        for mid_str in movie_ids:
            mid = int(mid_str)
            movie_row = df[df['movie_id'] == mid]
            
            if not movie_row.empty:
                row = movie_row.iloc[0]
                sigma = row['sigma']
                rating = row['rating']
                
                if sigma < 0.8:
                    conf_str = "High Confidence"
                else:
                    conf_str = "Experimental/Low Confidence"
                    
                responses.append(f"**Analysis for Movie {mid}:** I predicted a rating of {rating:.1f}/5.0 with {conf_str} (σ={sigma:.2f}).")
            else:
                responses.append(f"**Movie {mid}:** Not in the current top list, so I can't analyze it.")

    # ------------------------------------------------------------------
    # PART 2: Check for Concepts (Independent Checks)
    # ------------------------------------------------------------------
    
    # Check for Graph Logic
    if any(word in prompt_lower for word in ["graph", "network", "nodes", "edges", "how does it work"]):
        responses.append("**Graph Logic:** I view users and movies as Nodes. If you are connected to 'Action Andy', and he liked 'John Wick', I pass that 'signal' through the Edge to recommend it to you.")

    # Check for Sigma/Uncertainty
    if "sigma" in prompt_lower or "uncertainty" in prompt_lower:
        responses.append("**Sigma (σ):** This is my internal 'Doubt Score'.\n- Low (<0.8) = I have lots of data.\n- High (>1.5) = I am guessing based on weak connections.")
        
    # Check for Cold Start
    if "cold start" in prompt_lower:
        responses.append("**Cold Start:** This happens when a new user joins with zero history. Since I have no 'Edges' for them, I rely on global popularity trends until they rate their first movie.")

    # ------------------------------------------------------------------
    # PART 3: Final Assembly or Fallback
    # ------------------------------------------------------------------
    
    # If we found at least one answer, join them together
    if responses:
        return "\n\n---\n\n".join(responses)

    # Fallback only if NO keywords were matched
    ignored_words = ["what", "is", "the", "how", "why", "are", "you", "tell", "me", "about", "a", "an", "and"]
    keywords = [w for w in prompt.split() if w.lower() not in ignored_words]
    topic = keywords[0] if keywords else "that"
    
    return (f"I understand you are asking about **'{topic}'**, but my database is strictly limited to Movie Ratings and Graph Uncertainty metrics.\n\n"
            f"I cannot provide outside information about **{topic}**. Try asking me about 'Sigma' or specific Movie IDs!")

"""
CODE EXPLANATION:
1. Session State ('messages'):
   - Streamlit reruns the script on every click. We use 'st.session_state' to remember chat history so it doesn't disappear.
2. generate_smart_response():
   - This is a Rule-Based (Regex) system, not an LLM.
   - Part 1 (Regex): It looks for numbers (e.g., "500") in your question.
     - If found, it queries the DataFrame: df[df['movie_id'] == 500].
     - It returns the EXACT rating and sigma from the model.
   - Part 2 (Keywords): It checks for words like "Graph", "Sigma", "Cold Start".
     - It returns pre-written educational definitions.
   - Part 3 (Fallback): If it doesn't understand, it echoes your topic ("I don't know about X") to sound natural.
"""