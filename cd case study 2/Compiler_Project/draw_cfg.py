import networkx as nx
import matplotlib.pyplot as plt

def draw_cfg():
    G = nx.DiGraph()
    
    # Add nodes
    G.add_node("B1\nt1 = a > b\nifFalse t1 goto L1")
    G.add_node("B2\nc = a + b\ngoto L2")
    G.add_node("B3\nL1:\nc = a - b")
    G.add_node("B4\nL2:")
    
    # Add edges
    G.add_edge("B1\nt1 = a > b\nifFalse t1 goto L1", "B2\nc = a + b\ngoto L2", label=" True")
    G.add_edge("B1\nt1 = a > b\nifFalse t1 goto L1", "B3\nL1:\nc = a - b", label=" False")
    G.add_edge("B2\nc = a + b\ngoto L2", "B4\nL2:", label=" goto L2")
    G.add_edge("B3\nL1:\nc = a - b", "B4\nL2:", label=" fall-through")
    
    pos = {
        "B1\nt1 = a > b\nifFalse t1 goto L1": (0.5, 1.0),
        "B2\nc = a + b\ngoto L2": (0.2, 0.5),
        "B3\nL1:\nc = a - b": (0.8, 0.5),
        "B4\nL2:": (0.5, 0.0)
    }
    
    plt.figure(figsize=(8, 6))
    
    # Draw nodes with rectangular boxes
    nx.draw_networkx_nodes(G, pos, node_size=6000, node_color='lightblue', node_shape='s', alpha=0.9)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray', width=2)
    nx.draw_networkx_labels(G, pos, font_size=11, font_family='sans-serif', font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='red')
    
    plt.title("Control Flow Graph (CFG) for If-Else Statement", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("cfg_diagram.png", format="PNG", dpi=300, bbox_inches='tight')
    print("CFG Diagram generated successfully.")

if __name__ == "__main__":
    draw_cfg()
