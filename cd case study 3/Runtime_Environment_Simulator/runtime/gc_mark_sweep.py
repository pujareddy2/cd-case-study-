from .heap_manager import HeapManager

class MarkSweepGC:
    """
    Implements the Mark-Sweep Garbage Collection algorithm.
    Phase 1: Mark (Trace from roots and mark reachable objects).
    Phase 2: Sweep (Iterate over heap and delete unmarked objects).
    """
    def __init__(self, heap_manager: HeapManager):
        self.hm = heap_manager
        self.history = [] # To track phases for GUI

    def run_gc(self):
        self.history = []
        
        # Initial State
        self._record_state("Before GC")
        
        # Phase 1: Mark
        self.mark()
        self._record_state("After Mark Phase")
        
        # Phase 2: Sweep
        reclaimed = self.sweep()
        self._record_state(f"After Sweep Phase (Reclaimed {reclaimed} objects)")
        
        return reclaimed

    def mark(self):
        # Reset all marks
        for obj in self.hm.heap.values():
            obj.marked = False
            
        # Worklist for DFS/BFS
        worklist = list(self.hm.roots)
        
        while worklist:
            curr_id = worklist.pop()
            obj = self.hm.heap.get(curr_id)
            if obj and not obj.marked:
                obj.marked = True
                for ref_id in obj.references:
                    worklist.append(ref_id)

    def sweep(self) -> int:
        unreachable = []
        for obj_id, obj in self.hm.heap.items():
            if not obj.marked:
                unreachable.append(obj_id)
                
        for obj_id in unreachable:
            del self.hm.heap[obj_id]
            
        return len(unreachable)

    def _record_state(self, phase_name: str):
        # Snapshot for GUI visualization
        state = {
            "phase": phase_name,
            "heap": [
                {
                    "id": obj.obj_id, 
                    "value": obj.value, 
                    "marked": obj.marked,
                    "refs": list(obj.references)
                } 
                for obj in self.hm.heap.values()
            ],
            "roots": list(self.hm.roots)
        }
        self.history.append(state)
