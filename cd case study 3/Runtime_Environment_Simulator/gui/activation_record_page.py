import streamlit as st
import pandas as pd
from runtime.activation_record import ActivationRecord

def render_ar_page():
    st.title("Activation Record (Stack Frame) Viewer")
    st.markdown("An Activation Record is pushed onto the stack every time a function is called.")
    
    with st.sidebar:
        st.header("Create Custom AR")
        func_name = st.text_input("Function Name", "my_func")
        call_id = st.number_input("Call ID", 1)
        ret_addr = st.text_input("Return Address", "main_loop_end")
        params = st.text_input("Parameters (comma separated)", "x=10, y=20")
        locals_str = st.text_input("Locals (comma separated)", "sum=30")
        
        if st.button("Generate Visualization"):
            p_dict = {k.strip(): v.strip() for k, v in [p.split('=') for p in params.split(',') if '=' in p]}
            l_dict = {k.strip(): v.strip() for k, v in [l.split('=') for l in locals_str.split(',') if '=' in l]}
            
            ar = ActivationRecord(
                function_name=func_name,
                call_id=call_id,
                return_address=ret_addr,
                parameters=p_dict,
                local_variables=l_dict
            )
            st.session_state.current_ar = ar

    if 'current_ar' in st.session_state:
        ar = st.session_state.current_ar
        st.subheader(f"Logical Layout of AR({ar.function_name})")
        
        data = {
            "Field": ["Return Value", "Parameters", "Control Link", "Access Link", "Saved Machine Status", "Local Variables", "Temporaries"],
            "Value": [
                str(ar.return_value),
                str(ar.parameters),
                "-> Caller AR" if not ar.control_link else ar.control_link.function_name,
                "-> Lexical Parent AR" if not ar.access_link else ar.access_link.function_name,
                f"RetAddr: {ar.return_address}",
                str(ar.local_variables),
                str(ar.temporaries)
            ],
            "Purpose": [
                "Space reserved for the function's result",
                "Arguments passed to the function",
                "Dynamic Link to restore caller's frame",
                "Static Link to access non-local variables",
                "Instruction pointer to resume execution",
                "Memory for variables local to this function",
                "Space for evaluating complex expressions"
            ]
        }
        
        df = pd.DataFrame(data)
        st.table(df)
        
        st.info("The stack grows downwards, so this block of memory is pushed as a single contiguous unit.")
