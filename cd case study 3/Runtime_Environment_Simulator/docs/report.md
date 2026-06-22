# Runtime Environment Simulator - Project Report

## 1. Abstract
This project implements a comprehensive **Runtime Environment Simulator** designed to visually demonstrate the inner workings of memory management during program execution. Built in Python using Streamlit, NetworkX, and Graphviz, the system simulates activation records, recursive function calls, stack manipulation, dynamic heap allocation, and garbage collection algorithms (Mark-Sweep and Reference Counting). It serves as an interactive educational tool for Compiler Design students.

## 2. Introduction
In a compiled language, the compiler translates source code into machine code, but it is the **Runtime System** that manages memory dynamically as the program runs. Understanding how the stack and heap operate is crucial for systems programming and compiler construction. This project visualizes these abstract concepts.

## 3. Problem Statement
Model the execution of procedure calls including recursion, stack allocation, access to nonlocal data, heap allocation, and garbage collection, providing graphical representations of Activation Trees and Memory state.

## 4. Objectives
- Design and simulate Activation Records with proper fields (Return Address, Links, Variables).
- Generate Activation Trees dynamically for recursive calls.
- Track stack snapshots and memory growth.
- Simulate heap memory allocation and inter-object references.
- Implement Mark-Sweep and Reference Counting Garbage Collection.

## 5. System Architecture
The system follows a modular MVC (Model-View-Controller) architecture:
- **Model (Runtime Engine):** `stack_manager.py`, `heap_manager.py`, `gc_mark_sweep.py`.
- **View (GUI & Vis):** Streamlit pages (`gui/`) and Graphviz renderers (`visualization/`).
- **Controller:** Logic bridging Streamlit UI inputs to runtime simulation states.

## 6. Runtime Environment Design
The memory model is split into logical segments:
1. **Code:** Read-only instructions.
2. **Global/Static:** Initialized and BSS data.
3. **Heap:** Dynamic objects, growing upwards.
4. **Stack:** Execution contexts, growing downwards.

## 7. Activation Record Design
The implemented `ActivationRecord` class contains:
- `function_name` & `call_id`
- `return_address`
- `control_link` (Dynamic link to caller)
- `access_link` (Static link to lexical parent)
- `parameters`, `local_variables`, `temporaries`, `return_value`

## 8. Stack Allocation Design
The `StackManager` pushes an Activation Record when a function is called, tracking the nested state. It takes JSON snapshots of the stack at every step for playback in the GUI.

## 9. Heap Management Design
The `HeapManager` simulates dynamic memory. Objects are nodes in a directed graph. References between objects are directed edges.

## 10. Garbage Collection Design
- **Mark-Sweep:** A tracing collector. Phase 1 runs a DFS from roots to mark reachable objects. Phase 2 deletes unmarked objects.
- **Reference Counting:** Each object tracks inbound references. When the count reaches 0, the object is immediately deleted, and its children's counts are decremented recursively.

## 11. Algorithms
### Mark-Sweep Algorithm
```text
1. Initialize all object marks to false.
2. Worklist = [Roots]
3. While Worklist is not empty:
     curr = pop(Worklist)
     if not curr.mark:
         curr.mark = true
         for ref in curr.references:
             push(Worklist, ref)
4. For object in Heap:
     if not object.mark:
         Delete object
```

## 12. Conclusion
The Runtime Environment Simulator successfully demonstrates the core concepts of compiler runtime systems. By translating theoretical textbook concepts into interactive graph visualizations, the project provides a highly effective laboratory demonstration tool.
