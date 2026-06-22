import graphviz

def generate_heap_graph(objects: list, edges: list, roots: list) -> graphviz.Digraph:
    """
    Generates a visual representation of the Heap, showing object references and reachability.
    """
    dot = graphviz.Digraph(comment='Heap Memory Graph')
    dot.attr(rankdir='LR')
    
    dot.attr('node', shape='record', style='filled', fontname='Helvetica')
    
    # Create nodes
    for obj in objects:
        color = 'lightgrey'
        
        # If it's a snapshot dict
        if isinstance(obj, dict):
            obj_id = obj['id']
            val = obj['value']
            marked = obj.get('marked', False)
            if marked:
                color = 'lightgreen'
            elif obj_id in roots:
                color = 'lightblue'
            label = f"{{ ID: {obj_id} | Val: {val} }}"
            dot.node(obj_id, label, fillcolor=color)
        else:
            # It's a HeapObject
            obj_id = obj.obj_id
            if obj.marked:
                color = 'lightgreen'
            elif obj_id in roots:
                color = 'lightblue'
            label = f"{{ ID: {obj_id} | Val: {obj.value} | RefCount: {obj.ref_count} }}"
            dot.node(obj_id, label, fillcolor=color)

    # Roots node to show entry points
    if roots:
        dot.node("ROOTS", "Stack/Global Roots", shape='ellipse', fillcolor='orange', style='filled')
        for r in roots:
            dot.edge("ROOTS", r, color='orange')
            
    # Edges
    for edge in edges:
        dot.edge(edge[0], edge[1])
        
    return dot
