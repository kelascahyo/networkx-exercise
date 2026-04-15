import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(page_title="NetworkX Explorer", layout="wide")

## --- Functions ---

def generate_graph(nodes, probability):
    # Erdos-Renyi graph: common model for social networks
    return nx.erdos_renyi_graph(n=nodes, p=probability)

## --- Sidebar Controls ---

st.sidebar.header("Network Settings")
node_count = st.sidebar.slider("Number of Nodes", 10, 100, 30)
edge_prob = st.sidebar.slider("Edge Probability", 0.01, 0.20, 0.05)
layout_type = st.sidebar.selectbox("Layout Style", ["Spring", "Circular", "Shell", "Spectral"])

## --- Main UI ---

st.title("🕸️ NetworkX Concept: Social Connectivity")
st.markdown("""
This app demonstrates **Graph Theory** concepts. In this network, 'Nodes' represent people, 
and 'Edges' represent a connection or friendship between them.
""")

# Generate the graph object
G = generate_graph(node_count, edge_prob)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Network Visualization")
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Choose layout
    if layout_type == "Spring":
        pos = nx.spring_layout(G)
    elif layout_type == "Circular":
        pos = nx.circular_layout(G)
    elif layout_type == "Shell":
        pos = nx.shell_layout(G)
    else:
        pos = nx.spectral_layout(G)

    # Draw nodes and edges
    nx.draw(G, pos, ax=ax, with_labels=True, node_color="#4CAF50", 
            edge_color="#CCCCCC", node_size=500, font_size=8)
    
    st.pyplot(fig)

with col2:
    st.subheader("Network Metrics")
    
    # Concept: Degree Centrality (Who is the most "popular"?)
    centrality = nx.degree_centrality(G)
    df_centrality = pd.DataFrame(centrality.items(), columns=["Node", "Centrality Score"])
    df_centrality = df_centrality.sort_values(by="Centrality Score", ascending=False)

    st.write("**Top Influencers (Degree Centrality)**")
    st.dataframe(df_centrality.head(10), use_container_width=True)

    # General Stats
    st.metric("Total Connections", G.number_of_edges())
    st.metric("Average Clustering", round(nx.average_clustering(G), 3))

---

### 2. The Requirements File (`requirements.txt`)

For Streamlit Cloud to run your app, you **must** create a second file in the same GitHub folder named `requirements.txt`. Paste these lines inside:

```text
streamlit
networkx
matplotlib
pandas
