import networkx as nx
import plotly.graph_objects as go

class Visualizer:
    def visualize_graph(self, graph):
        pos = nx.spring_layout(graph, seed=42)

        edge_x = []
        edge_y = []
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='gray'),
            hoverinfo='none',
            mode='lines'
        )

        node_x = []
        node_y = []
        node_colors = []
        node_sizes = []
        node_text = []
        for node, data in graph.nodes(data=True):
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

            sev = data.get('severity', 0.0)
            # Three-step gradient
            if sev <= 0.5:
                # green to yellow
                t = sev / 0.5
                r = int(0 + t * 255)
                g = int(200 + (55 * (1 - t)))
                b = 0
            else:
                # yellow to red
                t = (sev - 0.5) / 0.5
                r = 255
                g = int(200 * (1 - t))
                b = 0
            color = f"rgb({r},{g},{b})"

            node_colors.append(color)
            node_sizes.append(10 + data.get('size', 4) * 4)

            node_text.append(
                f"Node: {node}<br>"
                f"Param: {data.get('complex_param', 'N/A')}<br>"
                f"Severity: {sev:.2f}<br>"
                f"Diagnosis: {data.get('diagnosis', 'unknown')}"
            )

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[str(n) for n in graph.nodes()],
            textposition='top center',
            hoverinfo='text',
            hovertext=node_text,
            marker=dict(
                showscale=False,
                color=node_colors,
                size=node_sizes,
                line_width=2
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Interactive Lymphatic System Graph',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        ))

        fig.write_html('graph.html')
        fig.show()