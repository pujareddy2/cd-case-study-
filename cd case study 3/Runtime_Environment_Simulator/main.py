import streamlit as st
from gui.home import render_home
from gui.activation_record_page import render_ar_page
from gui.stack_page import render_stack_page
from gui.heap_page import render_heap_page
from gui.gc_page import render_gc_page
from gui.dashboard import render_dashboard

st.set_page_config(page_title="Runtime Environment Simulator", layout="wide", page_icon="⚙️")

def main():
    st.sidebar.title("Navigation")
    pages = {
        "Home": render_home,
        "Program Memory Layout": render_dashboard,
        "Activation Record Viewer": render_ar_page,
        "Function Call Simulator": render_stack_page,
        "Heap Simulator": render_heap_page,
        "Garbage Collection GC": render_gc_page
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
