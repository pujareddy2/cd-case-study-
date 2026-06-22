import plotly.graph_objects as go

def generate_memory_layout_figure(segments: dict):
    """
    Generates a block diagram of the overall memory layout.
    """
    labels = []
    parents = []
    
    # We will use an invisible parent to group them if we use Treemap, 
    # but a simple table or bar chart is easier to understand as a stack.
    
    ordered_segments = [
        "High Address",
        "Stack",
        "Free Space (↓↑)",
        "Heap",
        "BSS (Uninitialized Data)",
        "Data (Initialized)",
        "Text (Code Segment)",
        "Low Address"
    ]
    
    colors = {
        "High Address": "white",
        "Stack": "lightcoral",
        "Free Space (↓↑)": "lightgrey",
        "Heap": "lightgreen",
        "BSS (Uninitialized Data)": "khaki",
        "Data (Initialized)": "gold",
        "Text (Code Segment)": "lightblue",
        "Low Address": "white"
    }

    fig = go.Figure(go.Bar(
        x=[1]*len(ordered_segments),
        y=ordered_segments,
        orientation='h',
        marker=dict(
            color=[colors[seg] for seg in ordered_segments],
            line=dict(color='black', width=1)
        ),
        text=[", ".join(segments.get(seg, [""])) if isinstance(segments.get(seg), list) else "" for seg in ordered_segments],
        textposition='inside'
    ))

    fig.update_layout(
        title="Program Memory Layout",
        barmode='stack',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(autorange="reversed"), # High address at top
        height=600,
        margin=dict(l=200) # Give space for segment names
    )
    
    return fig
