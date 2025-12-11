import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def render_analytics(df, threshold):
    st.markdown("### 📊 Uncertainty Distribution")
    
    # Matplotlib Plot
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.histplot(df['sigma'], bins=30, kde=True, ax=ax, color='purple')
    ax.axvline(threshold, color='red', linestyle='--', label=f'Threshold: {threshold}')
    ax.set_title("How 'Unsure' is the model about this user?")
    ax.set_xlabel("Sigma (Uncertainty)")
    st.pyplot(fig)