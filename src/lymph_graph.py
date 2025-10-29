import pandas as pd
import networkx as nx
import numpy as np
from avl_tree import AVLTree
import pandas as pd
import numpy as np

# Decode parameter into severity and diagnosis using model
def decode_neural_param(param, trainer):
    return trainer.decode_complex_param(param)

def create_lymph_graph(data_source="data/nodes_data.csv", trainer=None):
    if isinstance(data_source, str):
        df = pd.read_csv(data_source)
        nodes_data = [
            (
                row['node_id'],
                {
                    'density': row['density'],
                    'size': row['size'],
                    'activity': row['activity'],
                    'atypical_cells': row['atypical_cells'],
                    'x': row['x'],
                    'y': row['y']
                }
            )
            for _, row in df.iterrows()
        ]
    else:
        nodes_data = data_source

    # Lymph graph creation
    G = nx.Graph()
    avl = AVLTree()
    
    for node_id, attrs in nodes_data:
        complex_param = trainer.compute_complex_param(attrs) if trainer else attrs['complex_param']
        G.add_node(node_id, complex_param=complex_param, **attrs)
        sev, diag = decode_neural_param(complex_param, trainer)
        G.nodes[node_id]['severity'] = sev
        G.nodes[node_id]['diagnosis'] = diag
        avl.insert(node_id, complex_param)

    for i, (node_i_id, attrs_i) in enumerate(nodes_data):
        node_i_param = G.nodes[node_i_id]['complex_param']
        for j, (node_j_id, attrs_j) in enumerate(nodes_data[i + 1:], start=i + 1):
            node_j_param = G.nodes[node_j_id]['complex_param']
            param_diff = abs(node_i_param - node_j_param)
            if param_diff < 20.0:
                G.add_edge(node_i_id, node_j_id, weight=1.0 / (param_diff + 1e-6))
            if 'x' in attrs_i and 'y' in attrs_i and 'x' in attrs_j and 'y' in attrs_j:
                distance = np.sqrt((attrs_i['x'] - attrs_j['x'])**2 + (attrs_i['y'] - attrs_j['y'])**2)
                if distance < 0.5:
                    G.add_edge(node_i_id, node_j_id, weight=1.0 / (distance + 1e-6))
    
    return G, avl.get_top_n(10)