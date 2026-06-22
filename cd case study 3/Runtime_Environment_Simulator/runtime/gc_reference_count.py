from .heap_manager import HeapManager

class ReferenceCountGC:
    """
    Implements Reference Counting Garbage Collection.
    When an object's reference count drops to 0, it is immediately collected.
    Cannot collect cyclic references.
    """
    def __init__(self, heap_manager: HeapManager):
        self.hm = heap_manager
        self.history = []

    def process_updates(self):
        """
        In a real system, ref counting is inline.
        Here we process the heap to find and delete 0-ref objects.
        Returns number of reclaimed objects in this sweep.
        """
        self._record_state("Before Ref Count Check")
        reclaimed_count = 0
        
        while True:
            to_delete = []
            for obj_id, obj in self.hm.heap.items():
                if obj.ref_count == 0:
                    to_delete.append(obj_id)
            
            if not to_delete:
                break
                
            for obj_id in to_delete:
                obj = self.hm.heap[obj_id]
                # Before deleting, decrement ref counts of children it points to
                for child_id in obj.references:
                    if child_id in self.hm.heap:
                        self.hm.heap[child_id].ref_count -= 1
                del self.hm.heap[obj_id]
                reclaimed_count += 1
                
            self._record_state(f"Reclaimed {to_delete}")
            
        self._record_state("After Ref Count GC")
        return reclaimed_count

    def _record_state(self, phase_name: str):
        state = {
            "phase": phase_name,
            "heap": [
                {
                    "id": obj.obj_id, 
                    "value": obj.value, 
                    "ref_count": obj.ref_count,
                    "refs": list(obj.references)
                } 
                for obj in self.hm.heap.values()
            ],
            "roots": list(self.hm.roots)
        }
        self.history.append(state)
