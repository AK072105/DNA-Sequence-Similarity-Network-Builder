
import networkx as nx
import plotly.graph_objects as go


def create_network_figure(graph):

    # Calculate positions of all nodes
    positions = nx.spring_layout(graph, seed=42)

    # Create an empty figure
    fig = go.Figure()

    # Draw the edges
    edge_x = []
    edge_y = []

    # Store information for hovering over edges
    edge_hover_x = []
    edge_hover_y = []
    edge_hover_data = []

    for node_a, node_b, edge_data in graph.edges(data=True):

        x0, y0 = positions[node_a]
        x1, y1 = positions[node_b]

        # Store coordinates for drawing the line
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

        # Calculate the midpoint of the edge
        midpoint_x = (x0 + x1) / 2
        midpoint_y = (y0 + y1) / 2

        edge_hover_x.append(midpoint_x)
        edge_hover_y.append(midpoint_y)

        # Store the sequence IDs and similarity metrics
        edge_hover_data.append([
            node_a,
            node_b,
            edge_data["percentage_identity"],
            edge_data["coverage_a"],
            edge_data["coverage_b"]
        ])

    # Draw the actual lines
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=1, color="gray"),
        hoverinfo="skip",
        showlegend=False
    ))

    # Create invisible hover points at the middle of each edge
    fig.add_trace(go.Scatter(
        x=edge_hover_x,
        y=edge_hover_y,
        mode="markers",
        marker=dict(
            size=14,
            color="rgba(0,0,0,0.01)"
        ),
        customdata=edge_hover_data,
        hovertemplate=(
            "<b>%{customdata[0]} ↔ %{customdata[1]}</b><br>"
            "Percentage Identity: %{customdata[2]:.2f}%<br>"
            "Coverage of A: %{customdata[3]:.2f}%<br>"
            "Coverage of B: %{customdata[4]:.2f}%"
            "<extra></extra>"
        ),
        showlegend=False
    ))

    # Identify clusters
    clusters = list(nx.connected_components(graph))

    colors = [
        "#3986D8",
        "#E58A35",
        "#2E9D73",
        "#A16BC1",
        "#D65B65",
        "#8A8A8A"
    ]

    # Draw the nodes, using a different colour for each cluster
    for cluster_number, cluster in enumerate(clusters):

        node_x = []
        node_y = []
        node_labels = []
        node_degrees = []

        for node in cluster:

            x, y = positions[node]

            node_x.append(x)
            node_y.append(y)
            node_labels.append(node)
            node_degrees.append(graph.degree(node))

        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_labels,
            textposition="top center",
            textfont=dict(size=12, color="black"),
            marker=dict(
                size=25,
                color=colors[cluster_number % len(colors)]
            ),
            customdata=node_degrees,
            hovertemplate=(
                "Sequence: %{text}<br>"
                "Connections: %{customdata}"
                "<extra></extra>"
            ),
            name=f"Cluster {cluster_number + 1}"
        ))

    # Configure the appearance
    fig.update_layout(
        title="DNA Sequence Similarity Network",
        showlegend=True,
        hovermode="closest",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="#F5F5DC"
    )

    return fig




