%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"

void yyerror(const char* s);
%}

%option noyywrap

%%

"if"        { return IF; }
"then"      { return THEN; }
"else"      { return ELSE; }
"while"     { return WHILE; }
"do"        { return DO; }
"and"       { return AND; }
"or"        { return OR; }
"not"       { return NOT; }

[0-9]+      { strcpy(yylval.str, yytext); return NUM; }
[a-zA-Z_][a-zA-Z0-9_]* { strcpy(yylval.str, yytext); return ID; }

":="        { return ASSIGN; }
"<="        { return LE; }
">="        { return GE; }
"=="        { return EQ; }
"!="        { return NE; }
"<"         { return LT; }
">"         { return GT; }
"+"         { return PLUS; }
"-"         { return MINUS; }
"*"         { return MUL; }
"/"         { return DIV; }
"("         { return LPAREN; }
")"         { return RPAREN; }

[ \t\n\r]+  { /* ignore whitespace */ }
.           { printf("Unknown character: %s\n", yytext); }

%%
