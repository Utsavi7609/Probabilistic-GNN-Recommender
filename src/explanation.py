import random

def explain_prediction(rating, sigma, genre, user_history_count):
    """
    Converts metrics into a human-readable string.
    """
    # 1. Analyze Confidence
    if sigma < 0.8:
        confidence_text = "We are **100% sure** you'll love this."
        reason = f"It fits your typical {genre} pattern perfectly."
    elif sigma < 1.5:
        confidence_text = "It's a **Solid Bet**."
        reason = "It's similar to other hits, but a bit different."
    else:
        confidence_text = "This is a **Wildcard**."
        reason = "We don't have much data on you watching this genre."

    # 2. Analyze Rating
    if rating > 4.5:
        hype = "Must Watch!"
    elif rating > 3.5:
        hype = "Recommended."
    else:
        hype = "Passable."

    # 3. Handle Cold Start Context
    if user_history_count == 0:
        reason = "Since you are new, we are guessing based on global trends."

    return f"{confidence_text} {reason}", hype

# """
# CODE EXPLANATION:
# 1. explain_prediction():
#    - This acts as the "Translator" layer between Math and English.
#    - Inputs: Raw numbers (Rating 4.5, Sigma 1.2).
#    - Outputs: Human-readable strings ("Solid Bet", "Wildcard").
#    - Logic: 
#      - If Sigma is low (<0.8), it tells the user "We are sure."
#      - If Sigma is high (>1.5), it warns "We don't have much data."
#    - Cold Start Handling: If the user history count is 0, it explicitly tells the user 
#      "We are guessing based on global trends," managing expectations.
# """