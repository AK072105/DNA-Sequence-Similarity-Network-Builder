import networkx as nx

from similarity import compare_all_sequences, passes_thresholds


import networkx as nx


def build_network(results_df, sequences):

    graph = nx.Graph()

    # Add all sequences as nodes
    for seq_id in sequences:

        graph.add_node(seq_id)

    # Add edges only for similar sequence pairs
    for _, row in results_df.iterrows():

        if row["status"] == "Similar":

            graph.add_edge(
                row["sequence_a"],
                row["sequence_b"],
                percentage_identity=row["percentage_identity"],
                coverage_a=row["coverage_a"],
                coverage_b=row["coverage_b"]
            )

    return graph


# The below function helps to identify clusters or connected components in the network.
def identify_clusters(graph):

    clusters = list(nx.connected_components(graph))

    return clusters



if __name__ == "__main__":
    
    sequences = {
    "Seq1": "ATGCGTAC",
    "Seq2": "ATGCGTCC",
    "Seq3": "ATGCGTAA",
    "Seq4": "TTGGAACC"}

    graph = build_network(sequences)

    print("Nodes:", graph.nodes())

    print("Edges:", graph.edges())

    print("Number of nodes:", graph.number_of_nodes())

    print("Number of edges:", graph.number_of_edges())

    clusters = identify_clusters(graph)

    print("Clusters:", clusters)


