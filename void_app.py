import streamlit as st
import torch
import pandas as pd
import networkx as nx
from torch_geometric.nn import SAGEConv, to_hetero
import torch.nn.functional as F
from torch_geometric.data import Data
import random

# ==========================================
# 1. MODEL DEFINITION (MUST MATCH KAGGLE)
# ==========================================
class GNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

class UncertaintyRecommender(torch.nn.Module):
    def __init__(self, hidden_channels, data):
        super().__init__()
        self.gnn = GNN(hidden_channels)
        self.gnn = to_hetero(self.gnn, data.metadata(), aggr='sum')
        self.lin = torch.nn.Linear(2 * hidden_channels, 2)

    def forward(self, x_dict, edge_index_dict, edge_label_index):
        z_dict = self.gnn(x_dict, edge_index_dict)
        row, col = edge_label_index
        user_emb = z_dict['user'][row]
        movie_emb = z_dict['movie'][col]
        concat = torch.cat([user_emb, movie_emb], dim=-1)
        out = self.lin(concat)
        mu = out[:, 0]
        sigma = F.softplus(out[:, 1]) + 1e-6
        return mu, sigma

# # ==========================================
# # 2. LOAD ARTIFACTS
# # ==========================================
# @st.cache_resource
# def load_data():
#     # Load Data (Map to CPU)
#     data = torch.load('graph_data.pt', map_location=torch.device('cpu'))
    
#     # Initialize Model
#     model = UncertaintyRecommender(hidden_channels=64, data=data)
    
#     # Load Weights
#     model.load_state_dict(torch.load('gnn_model.pth', map_location=torch.device('cpu')))
#     model.eval()
#     return model, data

# ==========================================
# 2. LOAD ARTIFACTS (FIXED)
# ==========================================
@st.cache_resource
def load_data():
    # Load Data (Map to CPU)
    # Added weights_only=False to fix the PyTorch 2.6 error
    data = torch.load('graph_data.pt', map_location=torch.device('cpu'), weights_only=False)
    
    # Initialize Model
    model = UncertaintyRecommender(hidden_channels=64, data=data)
    
    # Load Weights
    # Added weights_only=False here too
    model.load_state_dict(torch.load('gnn_model.pth', map_location=torch.device('cpu'), weights_only=False))
    model.eval()
    return model, data

# ==========================================
# 3. APP INTERFACE
# ==========================================
st.set_page_config(page_title="GNN Uncertainty Recommender", layout="wide")
st.title("🎬 AI Recommendation Engine with Uncertainty Quantification")
st.markdown("""
**Research Objective:** Unlike standard recommenders that only predict *what* you like, 
this GNN estimates its own **Uncertainty (Sigma)**. 
Use the slider to filter out "Risky" predictions where the model is guessing.
""")

try:
    model, data = load_data()
    st.sidebar.success("✅ System Online")
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("User Control Panel")
user_id = st.sidebar.number_input("Select User ID", 0, data['user'].num_nodes-1, 42)
uncertainty_threshold = st.sidebar.slider("Max Uncertainty Tolerance (Sigma)", 0.0, 3.0, 1.5, help="Lower = Safer Bets. Higher = More Discovery.")

# ==========================================
# 4. PREDICTION LOGIC
# ==========================================
if st.button("Generate Recommendations"):
    with st.spinner("Running GNN Inference..."):
        # 1. Create a batch of (User, All Movies) pairs
        num_movies = data['movie'].num_nodes
        user_indices = torch.full((num_movies,), user_id, dtype=torch.long)
        movie_indices = torch.arange(num_movies, dtype=torch.long)
        edge_label_index = torch.stack([user_indices, movie_indices], dim=0)
        
        # 2. Run Model
        with torch.no_grad():
            mu, sigma = model(data.x_dict, data.edge_index_dict, edge_label_index)
        
        # 3. Convert to Pandas for sorting
        df = pd.DataFrame({
            'movie_id': movie_indices.numpy(),
            'predicted_rating': mu.numpy(),
            'uncertainty': sigma.numpy()
        })
        
        # 4. Filter & Sort
        # Safe Recs: High Rating (>3.5) AND Low Uncertainty (< Threshold)
        safe_recs = df[
            (df['predicted_rating'] > 3.0) & 
            (df['uncertainty'] < uncertainty_threshold)
        ].sort_values(by='predicted_rating', ascending=False).head(10)
        
        # Risky Recs: High Rating BUT High Uncertainty
        risky_recs = df[
            (df['predicted_rating'] > 3.0) & 
            (df['uncertainty'] > uncertainty_threshold)
        ].sort_values(by='predicted_rating', ascending=False).head(5)

    # ==========================================
    # 5. DISPLAY RESULTS
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"✅ Safe Bets (Sigma < {uncertainty_threshold})")
        for _, row in safe_recs.iterrows():
            st.info(f"Movie #{int(row['movie_id'])} | Rating: {row['predicted_rating']:.2f} | Confidence: High (Sigma: {row['uncertainty']:.2f})")
            
    with col2:
        st.subheader("⚠️ High Uncertainty / Experimental")
        for _, row in risky_recs.iterrows():
            st.warning(f"Movie #{int(row['movie_id'])} | Rating: {row['predicted_rating']:.2f} | Confidence: Low (Sigma: {row['uncertainty']:.2f})")

    # ==========================================
    # 6. GRAPH VISUALIZATION (NETWORKX)
    # ==========================================
    st.markdown("---")
    st.subheader("🕸️ Local Graph Connectivity")
    st.caption("Visualizing the User's neighborhood in the graph.")
    
    # Create a small subgraph for the user
    G = nx.Graph()
    G.add_node(f"User {user_id}", color='red', size=20)
    
    # Add top 5 recommended movies as nodes
    for i, row in safe_recs.head(5).iterrows():
        movie_node = f"Movie {int(row['movie_id'])}"
        G.add_node(movie_node, color='blue', size=15)
        G.add_edge(f"User {user_id}", movie_node, weight=row['predicted_rating'])
    
    # Draw simple static graph using Matplotlib inside Streamlit
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=['red'] + ['blue']*5, font_size=8, ax=ax)
    st.pyplot(fig)