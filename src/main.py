import pandas as pd
import lymph_graph as lymph_graph
import train
import visualization

# Launch the whole project
def main():
    trainer = train.ModelTrainer()
    historical_data = pd.read_csv("data/historical_data.csv")
    trainer.train(historical_data)
    graph, top_nodes = lymph_graph.create_lymph_graph("data/nodes_data.csv", trainer=trainer)
    vis = visualization.Visualizer()
    vis.visualize_graph(graph) 
    print("Nodes (node_id, complex_param):")
    for node_id, param in top_nodes:
        print(f"Node {node_id}, Param: {param}")

if __name__ == "__main__":
    main()