import networkx as nx
from pyvis.network import Network
import tempfile
import os

def render_confidence_bar(sigma, max_sigma=3.0):
    """
    Draws the visual bar: ████░░ (High Confidence)
    """
    # Normalize: 0 sigma = 100% conf, 3.0 sigma = 0% conf
    pct = max(0, min(100, (1 - (sigma / max_sigma)) * 100))
    filled = int(pct / 10)
    empty = 10 - filled
    bar = "█" * filled + "░" * empty
    
    # Color coding for the text
    color = "green" if pct > 70 else "orange" if pct > 40 else "red"
    return f"<code style='color:{color}'>{bar} {int(pct)}%</code>"

def render_interactive_graph(data, user_id, df_results):
    """
    Backs up CV Claim: 'Visualized graph embeddings... identifying patterns'
    """
    # 1. Setup PyVis
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
    
    # 2. Add Center User Node
    net.add_node(f"User_{user_id}", label=f"User {user_id}", color="#FF4B4B", size=25)
    
    # 3. Add Top 15 Recommendations as Nodes
    top_recs = df_results.sort_values('rating', ascending=False).head(15)
    
    for _, row in top_recs.iterrows():
        mid = int(row['movie_id'])
        sigma = row['sigma']
        rating = row['rating']
        
        # Node Color: Blue (Safe) vs Orange (Risky)
        color = "#00C851" if sigma < 1.0 else "#ffbb33"
        label = f"Mov {mid}"
        
        # Tooltip content
        title = f"Genre: {row['genre']}\nRating: {rating:.1f}\nUncertainty: {sigma:.2f}"
        
        net.add_node(f"Mov_{mid}", label=label, title=title, color=color, size=15 + rating)
        net.add_edge(f"User_{user_id}", f"Mov_{mid}", value=rating, color="#555555")
        
    # 4. Physics Options
    net.force_atlas_2based(gravity=-50)
    
    # 5. Export to HTML
    try:
        # Use a standard temp file approach
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        net.save_graph(tmpfile.name)
        with open(tmpfile.name, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<div>Error generating graph: {e}</div>"
    
"""
CODE EXPLANATION:
1. render_confidence_bar():
   - Converts the raw Sigma value (e.g., 1.2) into a visual HTML progress bar.
   - If Sigma is low, the bar is Green (Safe). If high, it's Orange (Risky).
2. render_interactive_graph():
   - Uses the 'PyVis' library to generate a physics simulation.
   - Nodes: It creates a central 'User Node' and connects 'Movie Nodes' to it.
   - Force Atlas 2: The physics algorithm that makes connected nodes pull together.
   - It exports the graph as an HTML snippet, which Streamlit renders in an iframe.
"""