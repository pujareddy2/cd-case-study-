import graphviz

def generate_activation_tree_graph(nodes: list, edges: list) -> graphviz.Digraph:
    """
    Generates a Graphviz Digraph for the Activation Tree.
    """
    dot = graphviz.Digraph(comment='Activation Tree')
    dot.attr(rankdir='TB', size='8,8')
    
    dot.attr('node', shape='rect', style='filled', color='lightblue', fontname='Helvetica')
    
    for node in nodes:
        dot.node(str(node['id']), node['label'])
        
    for edge in edges:
        dot.edge(str(edge[0]), str(edge[1]))
        
    return dot
