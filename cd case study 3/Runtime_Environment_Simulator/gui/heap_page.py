import streamlit as st
from runtime.heap_manager import HeapManager
from visualization.heap_visualizer import generate_heap_graph

def render_heap_page():
    st.title("Heap Memory Simulator")
    
    if 'heap' not in st.session_state:
        st.session_state.heap = HeapManager()

    hm = st.session_state.heap
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Controls")
        
        with st.expander("Allocate Object"):
            obj_id = st.text_input("Object ID (e.g., A)")
            obj_val = st.text_input("Value")
            if st.button("Allocate"):
                if obj_id:
                    try:
                        hm.allocate(obj_id, obj_val)
                        st.success(f"Allocated {obj_id}")
                    except ValueError as e:
                        st.error(str(e))
                        
        with st.expander("Set Root Reference"):
            root_id = st.text_input("Root Object ID")
            if st.button("Add Root"):
                hm.add_root(root_id)
            if st.button("Remove Root"):
                hm.remove_root(root_id)
                
        with st.expander("Create Reference (Pointer)"):
            src_id = st.text_input("Source ID")
            dst_id = st.text_input("Target ID")
            if st.button("Link"):
                hm.add_reference(src_id, dst_id)
            if st.button("Unlink"):
                hm.remove_reference(src_id, dst_id)

        if st.button("Reset Heap", type="primary"):
            st.session_state.heap.reset()
            st.rerun()

    with col2:
        st.subheader("Heap Reachability Graph")
        objects = list(hm.get_objects())
        edges = hm.get_edges()
        roots = hm.roots
        
        if not objects:
            st.info("Heap is empty.")
        else:
            dot = generate_heap_graph(objects, edges, roots)
            st.graphviz_chart(dot.source)
            
        st.markdown("""
        **Legend:**
        - 🟠 **Orange:** Stack/Global Roots (Entry points to the heap)
        - 🔵 **Blue:** Objects directly referenced by roots
        - ⚪ **Grey:** Dynamically allocated objects
        """)
