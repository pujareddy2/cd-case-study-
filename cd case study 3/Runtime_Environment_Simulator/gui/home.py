import streamlit as st

def render_home():
    st.title("Runtime Environment Simulator")
    st.markdown("""
    ### Welcome to the Compiler Design Case Study 3 Simulator!

    This interactive educational tool demonstrates what happens under the hood when a program executes. 

    **Core Concepts Visualized:**
    - **Activation Records:** See how functions are packaged with arguments, local variables, and return addresses.
    - **Stack Simulator:** Watch the stack grow and shrink as functions are called and return.
    - **Activation Trees:** Trace recursive calls (like Factorial and Fibonacci).
    - **Heap Management:** See how objects are dynamically allocated and referenced.
    - **Garbage Collection:** Step through Mark-Sweep and Reference Counting algorithms.

    **Use the sidebar to navigate between different simulations.**
    
    *Developed for Compiler Design Laboratory.*
    """)
