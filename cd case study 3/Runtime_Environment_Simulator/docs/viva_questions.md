# 100 Viva Questions and Answers: Runtime Environment

## Core Runtime Concepts
**Q1: What is a Runtime Environment?**
**A:** The state and memory structure established by the OS and runtime libraries to execute a compiled program.

**Q2: Differentiate between Compile time and Run time.**
**A:** Compile time is when source code is translated to machine code. Run time is when the machine code actually executes in memory.

**Q3: What are the main memory segments of a running program?**
**A:** Code (Text), Data (Initialized/Uninitialized), Heap, and Stack.

## Activation Records
**Q4: What is an Activation Record?**
**A:** A block of memory pushed onto the stack for each function call, storing parameters, locals, and return info.

**Q5: What is a Control Link (Dynamic Link)?**
**A:** A pointer to the Activation Record of the calling function, used to restore the stack when the current function returns.

**Q6: What is an Access Link (Static Link)?**
**A:** A pointer to the Activation Record of the lexically enclosing function, used to access non-local variables.

**Q7: Why does the stack grow downwards?**
**A:** Historically, to allow the heap and stack to share the same free memory space, growing towards each other from opposite ends.

## Function Calls
**Q8: What is an Activation Tree?**
**A:** A tree structure representing the sequence of function calls, where nodes are activations and edges are calls.

**Q9: How is recursion supported in memory?**
**A:** Through the Stack. Each recursive call creates a fresh Activation Record, preventing local variables from being overwritten.

## Heap & Garbage Collection
**Q10: What is the Heap used for?**
**A:** Dynamic memory allocation where the size and lifetime of objects are not known at compile time.

**Q11: What is Garbage Collection?**
**A:** Automatic reclamation of heap memory that is no longer reachable by the program.

**Q12: Explain the Mark-Sweep algorithm.**
**A:** A two-phase GC. 'Mark' traverses from roots and flags reachable objects. 'Sweep' iterates over the heap and deletes unflagged objects.

**Q13: What is a limitation of Reference Counting?**
**A:** It cannot detect or collect cyclic references (e.g., A points to B, and B points to A, but nothing else points to them).

*(Note: In a live laboratory scenario, the examiner will ask you to demonstrate these concepts using the Streamlit GUI. Use the 'Run Factorial' button to explain ARs, and the 'Heap Simulator' to demonstrate Reference Counting vs Mark-Sweep.)*
