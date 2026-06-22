class TreeNode:
    def __init__(self, name: str, call_id: int, parameters: dict):
        self.name = name
        self.call_id = call_id
        self.parameters = parameters
        self.return_value = None
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

class ActivationTree:
    """
    Builds the Activation Tree to represent function calls.
    Nodes are activations (functions), edges are calls from caller to callee.
    """
    def __init__(self):
        self.root = None
        self.node_map = {}  # Map call_id -> TreeNode

    def start_call(self, name: str, call_id: int, params: dict, caller_id: int = None):
        node = TreeNode(name, call_id, params)
        self.node_map[call_id] = node

        if caller_id is None or caller_id not in self.node_map:
            if self.root is None:
                self.root = node
        else:
            parent = self.node_map[caller_id]
            parent.add_child(node)
            
        return node

    def end_call(self, call_id: int, return_value: any):
        if call_id in self.node_map:
            self.node_map[call_id].return_value = return_value

    def get_nodes_and_edges(self):
        """Returns lists of nodes and edges for visualization libraries like NetworkX"""
        nodes = []
        edges = []
        
        def traverse(node):
            if not node: return
            
            label = f"{node.name}({','.join([str(v) for v in node.parameters.values()])})"
            if node.return_value is not None:
                label += f" -> {node.return_value}"
                
            nodes.append({
                "id": node.call_id,
                "label": label,
                "name": node.name
            })
            
            for child in node.children:
                edges.append((node.call_id, child.call_id))
                traverse(child)

        traverse(self.root)
        return nodes, edges

    def reset(self):
        self.root = None
        self.node_map = {}
