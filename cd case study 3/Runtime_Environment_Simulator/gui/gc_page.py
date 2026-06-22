import streamlit as st
from runtime.gc_mark_sweep import MarkSweepGC
from runtime.gc_reference_count import ReferenceCountGC
from visualization.heap_visualizer import generate_heap_graph
import time

def render_gc_page():
    st.title("Garbage Collection Simulator")
    
    if 'heap' not in st.session_state or not st.session_state.heap.get_objects():
        st.warning("Please allocate objects in the 'Heap Simulator' tab first.")
        return

    hm = st.session_state.heap
    
    gc_type = st.radio("Select GC Algorithm", ["Mark-Sweep", "Reference Counting"])
    
    if st.button(f"Run {gc_type} GC"):
        if gc_type == "Mark-Sweep":
            gc = MarkSweepGC(hm)
            reclaimed = gc.run_gc()
            st.session_state.gc_history = gc.history
            st.session_state.gc_msg = f"Mark-Sweep reclaimed {reclaimed} objects."
        else:
            gc = ReferenceCountGC(hm)
            reclaimed = gc.process_updates()
            st.session_state.gc_history = gc.history
            st.session_state.gc_msg = f"Reference Counting reclaimed {reclaimed} objects."
            
    if 'gc_history' in st.session_state:
        st.success(st.session_state.gc_msg)
        
        history = st.session_state.gc_history
        step = st.slider("Step through GC phases", 0, len(history)-1, 0)
        
        state = history[step]
        st.subheader(f"Phase: {state['phase']}")
        
        # Prepare data for visualizer
        objects = state['heap']
        edges = []
        for obj in objects:
            for ref in obj['refs']:
                edges.append((obj['id'], ref))
                
        dot = generate_heap_graph(objects, edges, state['roots'])
        st.graphviz_chart(dot.source)
        
        if gc_type == "Mark-Sweep":
            st.markdown("""
            **Mark-Sweep Legend:**
            - 🟢 **Green:** Marked (Reachable)
            - ⚪ **Grey:** Unmarked (Garbage)
            """)
