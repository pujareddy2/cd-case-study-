from .activation_record import ActivationRecord
from typing import List

class DisplayTable:
    """
    Simulates the Display Table mechanism for non-local data access in nested scopes.
    """
    def __init__(self):
        # The display array. Index represents the lexical nesting depth.
        # Value is the call_id or a reference to the AR.
        self.table: List[ActivationRecord] = []

    def update_on_call(self, ar: ActivationRecord):
        """Update display when a new AR is pushed."""
        depth = ar.nesting_depth
        
        # Extend table if needed
        while len(self.table) <= depth:
            self.table.append(None)
            
        # The trick: to support popping, we must remember the old value at this depth.
        # But for simulation, we'll just keep the current AR at this depth.
        self.table[depth] = ar

    def get_ar_at_depth(self, depth: int) -> ActivationRecord:
        if depth < len(self.table):
            return self.table[depth]
        return None

def resolve_nonlocal_static_link(current_ar: ActivationRecord, target_depth: int) -> ActivationRecord:
    """
    Resolves a nonlocal variable by traversing the static link chain.
    """
    current = current_ar
    while current is not None and current.nesting_depth > target_depth:
        current = current.access_link
    return current
