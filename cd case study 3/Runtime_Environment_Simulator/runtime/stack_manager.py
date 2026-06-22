from .activation_record import ActivationRecord
import copy

class StackManager:
    """
    Manages the push and pop operations of the execution stack.
    Maintains historical snapshots of the stack for visualization.
    """
    def __init__(self):
        self.stack = []
        self.snapshots = []
        self._call_counter = 0

    def push(self, function_name: str, params: dict = None, locals: dict = None, 
             parent_ar: ActivationRecord = None, lexical_parent: ActivationRecord = None,
             depth: int = 0) -> ActivationRecord:
        
        self._call_counter += 1
        
        ar = ActivationRecord(
            function_name=function_name,
            call_id=self._call_counter,
            control_link=parent_ar,
            access_link=lexical_parent,
            parameters=params if params else {},
            local_variables=locals if locals else {},
            nesting_depth=depth
        )
        
        self.stack.append(ar)
        self._take_snapshot(f"Push {ar.function_name}")
        return ar

    def pop(self, return_value=None):
        if not self.stack:
            return None
        
        ar = self.stack.pop()
        ar.return_value = return_value
        self._take_snapshot(f"Pop {ar.function_name} -> returned {return_value}")
        return ar

    def get_current_ar(self):
        if self.stack:
            return self.stack[-1]
        return None

    def _take_snapshot(self, action: str):
        # Create a deep copy of the stack references to freeze the state
        snapshot_stack = []
        for ar in self.stack:
            # We copy just the dict representation to avoid reference mutation issues
            snapshot_stack.append(ar.to_dict())
            
        self.snapshots.append({
            "action": action,
            "stack": snapshot_stack
        })

    def reset(self):
        self.stack = []
        self.snapshots = []
        self._call_counter = 0
