import streamlit as st
from runtime.memory_layout import MemoryLayoutSimulator
from visualization.memory_visualizer import generate_memory_layout_figure

def render_dashboard():
    st.title("Memory Layout Dashboard")
    st.markdown("This dashboard provides a high-level view of the entire Program Memory model.")
    
    simulator = MemoryLayoutSimulator()
    
    # Try to grab current state
    if 'sm' in st.session_state:
        simulator.update_stack(st.session_state.sm.stack)
    if 'heap' in st.session_state:
        simulator.update_heap(list(st.session_state.heap.get_objects()))
        
    layout = simulator.get_layout()
    fig = generate_memory_layout_figure(layout)
    st.plotly_chart(fig, use_container_width=True)
