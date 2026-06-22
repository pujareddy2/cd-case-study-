@echo off
flex lexer.l
if errorlevel 1 exit /b 1
bison -d parser.y
if errorlevel 1 exit /b 1
gcc -o compiler.exe lex.yy.c parser.tab.c tac.c backpatch.c basicblock.c cfg.c optimizer.c symboltable.c main.c
if errorlevel 1 exit /b 1
echo Build successful!
