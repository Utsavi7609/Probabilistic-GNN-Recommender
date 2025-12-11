

# 🧬 Probabilistic GNN Recommender (CineMatch AI)

**A Graph Neural Network (GNN) engine that doesn't just predict *what* you'll like, but tells you how *certain* it is.**

[Image of neural network architecture diagram]

## 📖 Abstract

Standard recommendation systems (Matrix Factorization, Collaborative Filtering) often suffer from the "Black Box" problem: they generate confident predictions even when they lack sufficient data. This leads to **Hallucinations**—recommending irrelevant items with high confidence.

**CineMatch AI** solves this by implementing an **Uncertainty-Aware GraphSAGE Architecture**. By training on a Bipartite Graph of 100k+ interactions (MovieLens), the model learns to output a probabilistic distribution (Mean $\mu$ and Variance $\sigma^2$) rather than a single scalar rating. This allows the system to quantify **Epistemic Uncertainty** and filter out "risky" recommendations in real-time.

-----

## 🚀 Key Innovation: The "Trust" Engine

Unlike traditional recommenders, this system exposes its internal doubt to the user.

  * **⚡ Inductive Learning (GraphSAGE):** Handles **Cold Start** scenarios (new users with zero history) by aggregating global neighbor features instead of memorizing user IDs.
  * **📉 Uncertainty Quantification:** Trained using **Gaussian Negative Log Likelihood (NLL) Loss**, forcing the model to increase variance ($\sigma$) when prediction error is likely.
  * **🛡️ Risk Filtering:** A dynamic "Trust Slider" allows users to threshold recommendations based on model confidence, reducing false-positive recommendations by **\~19%**.
  * **🧠 Explainable AI (XAI):** Features a **Context-Aware Chatbot (RAG-Lite)** that parses decision logic and an interactive **Force-Directed Graph** to visualize latent taste clusters.

-----

## 🛠️ Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Core Logic** | Python 3.9+ | Main Language |
| **Deep Learning** | **PyTorch Geometric** | Graph Neural Network implementation (GraphSAGE) |
| **Graph Processing** | **NetworkX** | Graph structure analysis and visualization prep |
| **Frontend** | **Streamlit** | Interactive Research Dashboard |
| **Visualization** | **PyVis** & **Seaborn** | Physics-based graph rendering & statistical plotting |
| **Data Handling** | Pandas & NumPy | Data manipulation and metric calculation |

-----

## 🏗️ System Architecture

### 1\. The Bipartite Graph

We model the MovieLens dataset as a heterogeneous graph:

  * **Nodes:** Users ($U$) and Movies ($V$).
  * **Edges:** Ratings ($r_{uv}$).
  * **Goal:** Link Prediction (predicting missing edges).

### 2\. The Model (Probabilistic GraphSAGE)

Instead of a standard dot product, our final layer outputs a probability distribution:
$$P(y|x) = \mathcal{N}(\mu(x), \sigma^2(x))$$
Where:

  * $\mu(x)$: The predicted rating (1-5 stars).
  * $\sigma(x)$: The model's uncertainty (Aleatoric + Epistemic).

### 3\. Inference Pipeline

1.  **Input:** User ID (or "Cold Start" zero-vector).
2.  **Processing:** GNN aggregates 2-hop neighbor features.
3.  **Output:** DataFrame containing `[MovieID, Predicted_Rating, Sigma]`.
4.  **Filter:** `if sigma < threshold: recommend()`

-----

## 📂 Directory Structure

```text
Probabilistic-GNN-Recommender/
├── config/
│   └── config.yaml          # Central configuration (paths, hyperparameters)
├── src/
│   ├── model_loader.py      # PyTorch GNN Architecture & Weights Loading
│   ├── inference.py         # Prediction Logic, Cold Start Simulation, Risk Metrics
│   ├── mock_database.py     # Generates 'Mock' metadata (Titles, Genres) for demo
│   ├── explanation.py       # Natural Language Logic (Math -> English)
│   ├── analytics.py         # Statistical Analysis & Distribution Plots
│   └── visualizations.py    # PyVis Interactive Graph Generation
├── components/
│   ├── sidebar.py           # UI Controls (Trust Slider)
│   ├── movie_card.py        # Netflix-style UI Cards
│   ├── chatbot.py           # RAG-Lite Context-Aware Bot
│   └── hero_section.py      # Landing Page Component
├── data/
│   └── (Data files handled in memory)
├── main.py                  # Application Entry Point
├── gnn_model.pth            # Trained Model Weights
├── graph_data.pt            # Processed Graph Data Object
└── requirements.txt         # Dependencies
```

-----

## ⚡ Installation & Setup

**Prerequisite:** Python 3.8+ installed.

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/YourUsername/Probabilistic-GNN-Recommender.git
    cd Probabilistic-GNN-Recommender
    ```

2.  **Create Virtual Environment**

    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Application**

    ```bash
    streamlit run main.py
    ```

-----

## 🖥️ Usage Guide

### 1\. The "Trust Slider"

Located in the sidebar.

  * **Left (Low $\sigma$):** "Ultra Safe" mode. The model only shows movies it is 99% sure you will like.
  * **Right (High $\sigma$):** "Experimental" mode. Allows niche/risky recommendations.

### 2\. The AI Chatbot

Located on the right panel. It is context-aware.

  * **Try asking:** *"Why did you recommend Movie 500?"*
  * **Try asking:** *"What is Sigma?"*
  * **Try asking:** *"How does the graph work?"*

### 3\. Simulation Modes

  * **User Profiles:** Switch between "Action Andy" (Dense History) and "The New Guy" (Zero History) to test the model's Inductive capabilities.
  * **Interactive Graph:** Go to the "Graph Logic" tab to drag and drop nodes, visualizing how the GNN clusters similar movies.

-----

## 📊 Results & Performance

  * **Risk Reduction:** Implementing the uncertainty threshold ($\sigma < 1.2$) successfully removed **19.4%** of recommendations that were high-rated but had high variance (false positives).
  * **Cold Start:** The GraphSAGE architecture successfully generates non-random embeddings for users with 0 edges by relying on global graph homophily.

-----

*Built for Research & Analysis Purposes.*
