import plotly.graph_objects as go

def generate_stack_figure(stack_records: list):
    """
    Generates a Plotly Bar/Table figure or custom shape figure to represent the Stack.
    We will use a table format for clarity of Activation Records.
    """
    if not stack_records:
        return go.Figure().add_annotation(text="Stack is Empty", showarrow=False, font=dict(size=20))

    # Reverse to show top of stack at the top
    reversed_stack = list(reversed(stack_records))
    
    headers = ["Function", "Parameters", "Locals", "Return Value", "Control Link", "Access Link"]
    cells = []
    
    for ar in reversed_stack:
        # Depending on if it's a dict (from snapshot) or object
        if isinstance(ar, dict):
            cells.append([
                ar.get("Function"),
                str(ar.get("Parameters")),
                str(ar.get("Locals")),
                str(ar.get("Return Value")),
                str(ar.get("Control Link")),
                str(ar.get("Access Link"))
            ])
        else:
            cells.append([
                ar.function_name,
                str(ar.parameters),
                str(ar.local_variables),
                str(ar.return_value),
                ar.control_link.function_name if ar.control_link else "None",
                ar.access_link.function_name if ar.access_link else "None"
            ])
            
    # Transpose for plotly table
    cell_values = list(map(list, zip(*cells)))

    fig = go.Figure(data=[go.Table(
        header=dict(values=headers, fill_color='paleturquoise', font=dict(color='black', size=14), align='left'),
        cells=dict(values=cell_values, fill_color='lavender', font=dict(color='black', size=12), align='left', height=40)
    )])
    
    fig.update_layout(title="Current Stack State (Top -> Bottom)", margin=dict(l=0, r=0, t=40, b=0))
    return fig
