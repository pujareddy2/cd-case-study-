from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class ActivationRecord:
    """
    Represents an Activation Record (Stack Frame) created during a function call.
    Contains all the theoretical components required for runtime environment management.
    """
    function_name: str
    call_id: int  # Unique identifier for the call instance
    return_address: str = "main_return"
    control_link: Optional['ActivationRecord'] = None  # Dynamic Link (Caller)
    access_link: Optional['ActivationRecord'] = None   # Static Link (Lexical Parent)
    parameters: Dict[str, Any] = field(default_factory=dict)
    local_variables: Dict[str, Any] = field(default_factory=dict)
    temporaries: Dict[str, Any] = field(default_factory=dict)
    return_value: Any = None
    nesting_depth: int = 0

    def __str__(self):
        return f"AR({self.function_name}_{self.call_id})"

    def to_dict(self):
        return {
            "Function": self.function_name,
            "Call ID": self.call_id,
            "Return Address": self.return_address,
            "Control Link": self.control_link.function_name if self.control_link else "None",
            "Access Link": self.access_link.function_name if self.access_link else "None",
            "Parameters": self.parameters,
            "Locals": self.local_variables,
            "Temporaries": self.temporaries,
            "Return Value": self.return_value,
            "Depth": self.nesting_depth
        }
