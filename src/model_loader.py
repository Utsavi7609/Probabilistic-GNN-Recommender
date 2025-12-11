import torch
import streamlit as st
from torch_geometric.nn import SAGEConv, to_hetero
import torch.nn.functional as F
import yaml
import os

# 1. Load Config
def load_config():
    # Fix for path issues: use absolute path based on this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# 2. Define Architecture (Must match your Kaggle Training exactly)
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
        
        # Manual Prediction Head for User->Movie
        row, col = edge_label_index
        user_emb = z_dict['user'][row]
        movie_emb = z_dict['movie'][col]
        
        concat = torch.cat([user_emb, movie_emb], dim=-1)
        out = self.lin(concat)
        
        # Return Mean (Rating) and Variance (Sigma)
        return out[:, 0], F.softplus(out[:, 1]) + 1e-6

# 3. Loader Function
@st.cache_resource
def load_system():
    cfg = load_config()
    try:
        # Load Data
        data = torch.load(cfg['paths']['data'], map_location='cpu', weights_only=False)
        
        # Initialize & Load Model
        model = UncertaintyRecommender(cfg['model']['hidden_channels'], data)
        model.load_state_dict(torch.load(cfg['paths']['model'], map_location='cpu', weights_only=False))
        model.eval()
        
        return model, data, cfg
    except FileNotFoundError as e:
        st.error(f"🚨 Critical Error: {e}. Please ensure gnn_model.pth and graph_data.pt are in the root folder.")
        st.stop()


# """
# CODE EXPLANATION:
# 1. load_config(): Reads the YAML file to get paths (like 'gnn_model.pth') so we don't hardcode them.
# 2. GNN Class: Defines the 'Encoder'.
#    - Uses SAGEConv layers (GraphSAGE) instead of GCNConv.
#    - SAGEConv allows 'Inductive' learning (handling new users not seen during training).
# 3. UncertaintyRecommender Class: The main model.
#    - 'to_hetero': Converts the simple GNN to handle Bipartite graphs (User nodes AND Movie nodes).
#    - The 'lin' layer: The final output layer.
#    - Crucially, it outputs 2 values: Mean (Rating) and Sigma (Variance).
#    - F.softplus: A math function that ensures Sigma is always positive (you can't have negative uncertainty).
# 4. load_system(): A robust function to load the saved model weights.
#    - It uses 'map_location=cpu' to ensure it runs on your laptop even if trained on a GPU.
# """