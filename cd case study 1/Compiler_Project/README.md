# Compiler Design: Lex + Yacc Front-End

Welcome to the end-to-end implementation of a Compiler Front-End for a simple arithmetic expression language.

## Project Structure
* `scanner.l`: Lex/Flex source code for Lexical Analysis. Matches tokens.
* `parser.y`: Yacc/Bison source code for Syntax Analysis. Creates CFG and calls semantic actions.
* `ast.c` / `ast.h`: Manages the Abstract Syntax Tree (AST).
* `symbol_table.c` / `symbol_table.h`: Hash table storing IDs and Temporary Variables.
* `tac.c` / `tac.h`: Generates Three Address Code (TAC) representing intermediate code.
* `main.c`: Entry point of the program.

## Installation on Windows

To run the actual C compiler on Windows, you must install MSYS2 to get GCC, Flex, and Bison.
1. Download **MSYS2** from https://www.msys2.org/ and install it.
2. Open the **MSYS2 UCRT64** terminal from your Start Menu.
3. Update package database: `pacman -Syu`
4. Install GCC, Flex, and Bison by running:
   `pacman -S gcc flex bison`
5. Navigate to the project directory in the MSYS2 terminal (e.g., `cd "/c/Desktop/case study/cd case study 1/Compiler_Project"`).

## Option 1: The Quick Way (Python Simulator)

If you do not have MSYS2 (GCC, Flex, Bison) installed, you can use the provided Python script. It simulates the entire compiler (Lexer/Parser) and generates the AST and TAC instantly! No C compilation required.

1. Open your terminal in the `Compiler_Project` folder.
2. Run the following command:
   ```sh
   python simulate_compiler.py input.txt
   ```
*(This will read your `input.txt` file and output the parsed results directly!)*

---

## Option 2: The Full Way (Building the C Compiler)

If you want to compile and run the actual C code using Flex and Bison, make sure you have installed **MSYS2** (from the instructions above) and added GCC, Flex, and Bison to your system PATH.

1. **Open your terminal** in the `Compiler_Project` directory.

2. **Generate the Lexer (Scanner):**
   ```sh
   flex scanner.l
   ```
   *(This reads your Lex rules and generates a C file called `lex.yy.c`)*

3. **Generate the Parser:**
   ```sh
   bison -d parser.y
   ```
   *(This reads your Yacc grammar rules and generates `parser.tab.c` and `parser.tab.h`)*

4. **Compile all the C files together:**
   ```sh
   gcc lex.yy.c parser.tab.c ast.c symbol_table.c tac.c main.c -o compiler
   ```
   *(This links everything and produces the `compiler.exe` executable program)*

5. **Run the Compiler!**
   ```sh
   ./compiler input.txt
   ```

## Run the Java GUI
We have also included a fully functional Java Swing GUI that simulates the parsing logic!
1. Open your standard Windows Command Prompt or PowerShell in the project directory.
2. Compile the Java file:
   ```sh
   javac CompilerFrontEnd.java
   ```
3. Run the GUI:
   ```sh
   java CompilerFrontEnd
   ```

## Test Cases
Here are 15 Test Cases, showcasing how the compiler works.

### Test Case 1: Simple Assignment
**Input**: `val := 10`
**Expected Tokens**: ID(val) ASSIGN NUM(10)
**Expected AST**:
```
:=
  val
  10
```
**Expected TAC**: `val := 10`

### Test Case 2: Precedence
**Input**: `prec1 := a + b * c`
**Expected AST**: `+` evaluates after `*`.
```
:=
  prec1
  +
    a
    *
      b
      c
```

### Test Case 3: Forced Precedence via Parentheses
**Input**: `prec2 := (a + b) * c`
**Expected AST**: `+` is grouped.
```
:=
  prec2
  *
    +
      a
      b
    c
```

### Test Case 4: Associativity
**Input**: `assoc := a - b - c`
Left-associative grammar evaluates `a-b` first.

### Test Case 5: Nested Parentheses
**Input**: `nested := ((a + b) * c) - d`

### Test Case 6: Multiple Operators
**Input**: `multiop := a + b - c * d / e`

### Test Case 7: Invalid Syntax
**Input**: `bad1 := (a + b`
**Result**: `Syntax Error: syntax error` (Unmatched parenthesis).

### Test Case 8: Missing Identifiers
**Input**: `bad2 := a + * b`
**Result**: `Syntax Error: syntax error`

### Test Case 9: Complex Expression
**Input**: `complex := (a * b) + (c * d) / (e - f)`
**AST & TAC**: Fully breaks down into multiple `t1, t2, t3` temporaries.

*(Check out `input.txt` to run most of these test cases dynamically.)*
