import streamlit as st
from runtime.stack_manager import StackManager
from runtime.activation_tree import ActivationTree
from visualization.stack_visualizer import generate_stack_figure
from visualization.tree_visualizer import generate_activation_tree_graph
import time

def simulate_factorial(n, stack_manager, tree_manager, parent_id=None):
    params = {"n": n}
    ar = stack_manager.push("factorial", params=params)
    node = tree_manager.start_call("factorial", ar.call_id, params, caller_id=parent_id)
    
    st.session_state.simulation_steps.append({
        "action": f"Call factorial({n})",
        "stack_records": [ar_obj for ar_obj in stack_manager.stack],
        "tree_nodes": tree_manager.get_nodes_and_edges()
    })
    
    if n <= 1:
        ret_val = 1
    else:
        ret_val = n * simulate_factorial(n-1, stack_manager, tree_manager, ar.call_id)
        
    stack_manager.pop(return_value=ret_val)
    tree_manager.end_call(ar.call_id, ret_val)
    
    st.session_state.simulation_steps.append({
        "action": f"Return from factorial({n}) -> {ret_val}",
        "stack_records": [ar_obj for ar_obj in stack_manager.stack],
        "tree_nodes": tree_manager.get_nodes_and_edges()
    })
    return ret_val

def render_stack_page():
    st.title("Function Call & Stack Simulator")
    
    if 'sm' not in st.session_state:
        st.session_state.sm = StackManager()
        st.session_state.tree = ActivationTree()
        st.session_state.simulation_steps = []
        st.session_state.current_step = 0

    st.sidebar.header("Simulation Settings")
    n_val = st.sidebar.slider("Factorial N", 1, 5, 3)
    
    if st.sidebar.button("Run Factorial Simulation"):
        st.session_state.sm.reset()
        st.session_state.tree.reset()
        st.session_state.simulation_steps = []
        st.session_state.current_step = 0
        simulate_factorial(n_val, st.session_state.sm, st.session_state.tree)
        
    if not st.session_state.simulation_steps:
        st.info("Run a simulation from the sidebar to see the Stack and Activation Tree in action.")
        return
        
    steps = st.session_state.simulation_steps
    max_steps = len(steps) - 1
    
    st.slider("Step through execution", 0, max_steps, key='current_step')
    
    current = steps[st.session_state.current_step]
    
    st.subheader(f"Action: {current['action']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Stack Snapshots")
        fig = generate_stack_figure(current["stack_records"])
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("### Activation Tree")
        nodes, edges = current["tree_nodes"]
        if nodes:
            dot = generate_activation_tree_graph(nodes, edges)
            st.graphviz_chart(dot.source)
        else:
            st.write("Tree is empty.")
