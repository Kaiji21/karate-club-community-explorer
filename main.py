import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

st.title("Karate Club Graph with Community Hierarchical Agglomeration (CHA)")
st.caption("An interactive Streamlit application for visualizing and analyzing community structures in the Karate Club social network using hierarchical clustering. This tool allows users to explore how the network can be partitioned into different numbers of communities, providing insights into social dynamics and group formation.")

G = nx.karate_club_graph()

st.write(f"**Nodes:** {G.number_of_nodes()} | **Edges:** {G.number_of_edges()}")

adj_matrix = nx.to_numpy_array(G)

def find_communities(adj_matrix, num_groups):
    clustering = AgglomerativeClustering(n_clusters=num_groups, metric='euclidean', linkage='ward')
    clustering.fit(adj_matrix)
    return clustering.labels_

def draw_graph(G, communities, pos, title):
    plt.figure(figsize=(10, 8))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'yellow']
    
    for i in range(max(communities) + 1):
        nodes_in_cluster = [node for node, cluster in enumerate(communities) if cluster == i]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes_in_cluster, node_color=colors[i % len(colors)], label=f"Group {i+1}")
    
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    plt.title(title)
    st.pyplot(plt)

num_groups = st.slider("Select the number of groups to find:", min_value=2, max_value=6, value=2)

communities = find_communities(adj_matrix, num_groups)

pos = nx.spring_layout(G, seed=42)

draw_graph(G, communities, pos, f"Karate Club Graph with {num_groups} Groups")
