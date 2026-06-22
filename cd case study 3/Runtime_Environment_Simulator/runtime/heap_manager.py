class HeapObject:
    """Represents an object allocated on the heap."""
    def __init__(self, obj_id: str, value: str, size: int = 1):
        self.obj_id = obj_id
        self.value = value
        self.size = size
        self.references = [] # List of obj_ids this object points to
        self.ref_count = 0   # Used for Reference Counting GC
        self.marked = False  # Used for Mark-Sweep GC

    def add_reference(self, target_id: str):
        if target_id not in self.references:
            self.references.append(target_id)

    def remove_reference(self, target_id: str):
        if target_id in self.references:
            self.references.remove(target_id)

class HeapManager:
    """Simulates the Heap Memory and object allocation/references."""
    def __init__(self):
        self.heap = {} # Maps obj_id to HeapObject
        self.roots = [] # List of obj_ids that are directly referenced from stack/globals

    def allocate(self, obj_id: str, value: str) -> HeapObject:
        if obj_id in self.heap:
            raise ValueError(f"Object {obj_id} already exists in heap.")
        obj = HeapObject(obj_id, value)
        self.heap[obj_id] = obj
        return obj

    def add_root(self, obj_id: str):
        if obj_id in self.heap and obj_id not in self.roots:
            self.roots.append(obj_id)
            self.heap[obj_id].ref_count += 1

    def remove_root(self, obj_id: str):
        if obj_id in self.roots:
            self.roots.remove(obj_id)
            self.heap[obj_id].ref_count -= 1

    def add_reference(self, source_id: str, target_id: str):
        if source_id in self.heap and target_id in self.heap:
            self.heap[source_id].add_reference(target_id)
            self.heap[target_id].ref_count += 1

    def remove_reference(self, source_id: str, target_id: str):
        if source_id in self.heap and target_id in self.heap:
            self.heap[source_id].remove_reference(target_id)
            self.heap[target_id].ref_count -= 1

    def get_objects(self):
        return self.heap.values()

    def get_edges(self):
        edges = []
        for obj in self.heap.values():
            for ref in obj.references:
                edges.append((obj.obj_id, ref))
        return edges

    def reset(self):
        self.heap = {}
        self.roots = []
