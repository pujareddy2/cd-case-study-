class MemoryLayoutSimulator:
    """
    Simulates the overall structure of program memory.
    Useful for visualizing the whole memory segments.
    """
    def __init__(self):
        self.segments = {
            "High Address": "",
            "Stack": ["(Empty)"],
            "Free Space (↓↑)": ["..."],
            "Heap": ["(Empty)"],
            "BSS (Uninitialized Data)": ["Global variables (0)"],
            "Data (Initialized)": ["Global variables (vals)"],
            "Text (Code Segment)": ["Instructions"],
            "Low Address": ""
        }

    def update_stack(self, stack_records: list):
        if not stack_records:
            self.segments["Stack"] = ["(Empty)"]
        else:
            self.segments["Stack"] = [ar.function_name for ar in reversed(stack_records)]

    def update_heap(self, heap_objects: list):
        if not heap_objects:
            self.segments["Heap"] = ["(Empty)"]
        else:
            self.segments["Heap"] = [f"{obj.obj_id}:{obj.value}" for obj in heap_objects]
            
    def get_layout(self):
        return self.segments
