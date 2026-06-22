# Project Report: Building a Lex + Yacc Front-End

## 1. Project Abstract
This project implements the front-end of a compiler for a custom arithmetic expression language. It covers Lexical Analysis, Syntax Analysis, Semantic Translation via Abstract Syntax Trees (AST), Symbol Table management, and Intermediate Code Generation via Three Address Code (TAC). 

## 2. Introduction
Compilers convert high-level programming language code into machine-executable instructions. The "front-end" focuses on understanding the language structure. By utilizing tools like Flex (for tokenization) and Bison (for grammar rules), we can effectively map mathematical and assignment syntax into structured memory.

## 3. Problem Statement
The goal is to parse custom language statements (like `x := (a + b) * 3`) and correctly evaluate operator precedence, manage identifier lifecycles, and generate logical intermediate outputs suitable for backend optimization.

## 4. Objectives
- Perform Lexical Analysis.
- Develop a Context-Free Grammar (CFG) for Syntax Analysis.
- Construct Abstract Syntax Trees (AST).
- Maintain a Symbol Table for Variable Management.
- Generate Three Address Code (TAC).

## 5. System Design
The system passes character streams into the Flex Scanner, which emits tokens to the Bison Parser. The parser uses an LALR(1) algorithm. As it matches grammar reductions (Syntax Directed Translation), it builds an AST node by node. Finally, the parser recursively navigates the AST to print the tree and generate linear TAC instructions.

## 6. Lexical Analysis Design
**What is a token?** A Token is a classified group of characters (e.g., `ID`, `NUM`). 
**What is a lexeme?** A Lexeme is the actual character sequence (e.g., `a`, `10`).
**Why Flex?** Flex utilizes finite automata (DFA/NFA) to perform regex pattern matching orders of magnitude faster than standard string parsing. We define rules for `+`, `-`, ID (`[a-zA-Z]+`), and NUM (`[0-9]+`).

## 7. Syntax Analysis Design
**CFG & Parse Trees**: A Context-Free Grammar describes the hierarchical syntax of the language. A parse tree traces the exact substitution of non-terminals to terminals.
**Ambiguity**: To prevent ambiguous mathematical expressions (like `a+b*c`), we use `%left` precedence in Bison. `MUL` and `DIV` have higher precedence than `PLUS` and `MINUS`.
**LALR**: Look-Ahead Left-to-Right parsing allows efficient bottom-up construction of the syntax tree.

## 8. AST Design
**Why AST?** A Parse Tree contains useless punctuation and grammar specific nodes (like parentheses). An Abstract Syntax Tree distills the meaning. 
A parent node is the operator (`*`), and children are operands (`a`, `b`). 

## 9. Symbol Table Design
**What is a Symbol Table?** It is a data structure created by the compiler to track variables, their scope, and their data types.
**Scope Management:** Used to track variables within `Global` or `Local` blocks. Here, identifiers are marked `Global`, and generated TAC temporaries (`t1`, `t2`) are marked `Local`.
Implemented as a Hash Table for `O(1)` average lookups.

## 10. TAC Generation Design
**Intermediate Code:** A machine-independent representation of the program.
**Why TAC?** Three Address Code breaks complex expressions into bite-sized instructions with at most one operator and three operands (e.g., `t1 = a + b`). This simplifies register allocation and optimization in the compiler backend.

## 11. Results and Outputs
The compiler successfully parses inputs, handles operator precedence correctly, dynamically constructs and visually prints the AST, emits correct TAC instructions, and caches all seen variables into the Symbol Table.

## 12. Advantages
- Modular and extensible code.
- O(1) identifier retrieval.
- Strict precedence adherence.

## 13. Limitations
- Does not support conditional statements (`if`, `while`).
- Error recovery is basic (stops at first syntax error).
- Data types are hardcoded to `int`.

## 14. Future Enhancements
- Implement Syntax Error Recovery.
- Add code optimization on the TAC (e.g., constant folding).
- Expand to a full Turing-complete language.

## 15. Conclusion
Using Lex and Yacc provides an incredibly robust platform for compiler development. The pipeline of Tokens -> CFG -> AST -> TAC perfectly demonstrates the theoretical concepts of Syntax Directed Translation.
