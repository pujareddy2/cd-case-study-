# Test Cases & Sample Executions

## Test Case 1: Simple Function Call
**Input:** `simulate_factorial(1)`
**Expected Output:** 
1. `push` Activation Record for `factorial(1)`.
2. `pop` returning `1`.
3. Stack returns to empty.
**Status:** PASS

## Test Case 2: Recursive Factorial
**Input:** `simulate_factorial(3)`
**Execution Steps:**
1. Call `fac(3)` -> push AR
2. Call `fac(2)` -> push AR
3. Call `fac(1)` -> push AR
4. Return 1 -> pop AR
5. Return 2 -> pop AR
6. Return 6 -> pop AR
**Expected Output:** Activation tree shows a linear branch of depth 3. Stack snapshots show peak depth of 3 Activation Records.
**Status:** PASS

## Test Case 3: Reachability Analysis (Heap)
**Input:** 
- Allocate A, B, C.
- Root = A.
- Link A -> B.
**Expected Output:**
- A is reachable (Blue).
- B is reachable (Green).
- C is unreachable (Grey/Red).
**Status:** PASS

## Test Case 4: Mark-Sweep GC
**Input:** Same as Test Case 3. Run Mark-Sweep.
**Execution Steps:**
- Phase 1 (Mark): A and B get marked.
- Phase 2 (Sweep): C is deleted.
**Expected Output:** Heap graph updates to show only A and B. "Reclaimed 1 objects".
**Status:** PASS

## Test Case 5: Reference Counting Cycles
**Input:** 
- Allocate A, B.
- Root = none.
- Link A -> B and B -> A.
**Expected Output:**
- Running Ref Counting GC reclaims 0 objects because both A and B have a ref count of 1.
- Demonstrates the theoretical flaw of Reference Counting.
**Status:** PASS

## Test Case 6: Display Table Updates
**Input:** Simulate nested procedures `Outer` -> `Inner`.
**Expected Output:** Display Table `[0]` points to `Outer` AR, `[1]` points to `Inner` AR.
**Status:** PASS
