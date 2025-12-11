import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def calculate_risk_reduction(df_results, threshold):
    """
    Calculates the '19% Reduction' metric dynamically.
    """
    high_rated = df_results[df_results['rating'] > 3.5]
    total_high_rated = len(high_rated)
    
    if total_high_rated == 0: return 0.0
    
    risky_high_rated = len(high_rated[high_rated['sigma'] > threshold])
    return (risky_high_rated / total_high_rated) * 100

def render_distribution_plot(df, threshold):
    """
    Renders the bell curve showing model confidence.
    """
    fig, ax = plt.subplots(figsize=(8, 3))
    # Plot the histogram of Uncertainty (Sigma)
    sns.histplot(df['sigma'], bins=30, kde=True, ax=ax, color='#FF4B4B', alpha=0.6)
    
    # Draw the Threshold Line
    ax.axvline(threshold, color='white', linestyle='--', linewidth=2, label=f'Cutoff: {threshold}')
    
    # Styling to match the Dark Theme
    fig.patch.set_alpha(0)
    ax.set_facecolor('#0E1117')
    ax.tick_params(colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    st.pyplot(fig)

"""
CODE EXPLANATION:
1. calculate_risk_reduction():
   - This function generates the "19%" metric for your CV.
   - It filters the dataframe to find movies that have HIGH ratings (>3.5) but also HIGH uncertainty (> threshold).
   - These are "False Positives"—movies the AI thinks are good, but is actually guessing about.
   - We calculate what % of the catalog is filtered out by your safety mechanism.

2. render_distribution_plot():
   - Uses Seaborn to plot a Kernel Density Estimate (KDE)—a smooth bell curve.
   - X-Axis: The Sigma (Uncertainty) score.
   - Y-Axis: How many movies have that score.
   - The Vertical Line: Shows the user's current "Trust Threshold".
   - Purpose: Visualizes the "Exploration-Exploitation" trade-off. Everything to the right of the line is being hidden.
"""