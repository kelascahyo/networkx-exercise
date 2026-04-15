import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="NetworkX Masterclass", layout="wide")

# --- Sidebar: Configuration ---
st.sidebar.header("1. Network Structure")
is_directed = st.sidebar.checkbox("Use Directed Graph (Arrows)", value=False)
node_count = st.sidebar.slider("Nodes", 10, 50, 20)
edge_prob = st.sidebar.slider("Connection Density", 0.05, 0.30, 0.10)

st.sidebar.header("2. Concept Focus")
concept = st.sidebar.selectbox(
    "Choose a Concept to Visualize",
    ["Degree Centrality", "Betweenness Centrality", "Community Detection", "Shortest Path"]
)

# --- Data Generation ---
@st.cache_data
def get_graph(n, p, directed):
    # Erdos-Renyi graph
    G = nx.erdos_renyi_graph(n, p, directed=directed)
    # Ensure the graph is connected for pathfinding
    return G

G = get_graph(node_count, edge_prob, is_directed)

# --- Main UI ---
st.title("🌐 Advanced NetworkX Explorer")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Concept Explanation")
    
    if concept == "Degree Centrality":
        st.info("**Popularity:** Measures how many direct connections a node has. High score = 'The Socialite'.")
        scores = nx.degree_centrality(G)
        
    elif concept == "Betweenness Centrality":
        st.info("**The Bridge:** Measures how often a node sits on the shortest path between others. High score = 'The Gatekeeper'.")
        scores = nx.betweenness_centrality(G)
        
    elif concept == "Community Detection":
        st.info("**Cliques:** Groups nodes that interact more with each other than the rest of the network.")
        # Using Clauset-Newman-Moore greedy modularity maximization
        communities = list(nx.community.greedy_modularity_communities(G))
        scores = {}
        for i, comm in enumerate(communities):
            for node in comm:
                scores[node] = i # Assign community ID as the score
                
    elif concept == "Shortest Path":
        st.info("**Navigation:** The fewest steps needed to get from Node A to Node B.")
        start_node = st.selectbox("Start Node", list(G.nodes()))
        end_node = st.selectbox("End Node", list(G.nodes()), index=len(G.nodes())-1)
        try:
            path = nx.shortest_path(G, source=start_node, target=end_node)
            st.success(f"Path: {' → '.join(map(str, path))}")
        except:
            st.error("No path exists between these nodes!")
            path = []

    # Display Data Table (except for Pathfinding which uses a list)
    if concept != "Shortest Path":
        df = pd.DataFrame(scores.items(), columns=["Node", "Value"]).sort_values(by="Value", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

with col1:
    st.subheader(f"Visualizing: {concept}")
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42) # Seed kept constant for layout stability
    
    # Visual Logic based on Concept
    node_colors = "#1f77b4" # Default blue
    node_sizes = 500
    edge_colors = "#CCCCCC"
    
    if concept == "Degree Centrality" or concept == "Betweenness Centrality":
        # Scale size by the score
        node_sizes = [v * 5000 + 300 for v in scores.values()]
        node_colors = list(scores.values()) # Heatmap based on score
        
    elif concept == "Community Detection":
        # Color nodes by community ID
        node_colors = [scores[node] for node in G.nodes()]
        
    elif concept == "Shortest Path":
        # Highlight path edges in red
        if 'path' in locals() and len(path) > 1:
            path_edges = list(zip(path, path[1:]))
            edge_colors = ['red' if e in path_edges or (not is_directed and e[::-1] in path_edges) else '#CCCCCC' for e in G.edges()]

    # Drawing
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.viridis, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, ax=ax, arrows=is_directed)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="white", ax=ax)
    
    plt.axis("off")
    st.pyplot(fig)
