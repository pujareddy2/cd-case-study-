%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_token(const char* token_name, const char* lexeme) {
    if(lexeme)
        printf("%s(%s)\n", token_name, lexeme);
    else
        printf("%s\n", token_name);
}
%}

%%
[ \t\r\n]+              { /* Ignore whitespace */ }
"//".*                  { /* Ignore single-line comments */ }
":="                    { print_token("ASSIGN", NULL); return ASSIGN; }
"+"                     { print_token("PLUS", NULL); return PLUS; }
"-"                     { print_token("MINUS", NULL); return MINUS; }
"*"                     { print_token("MUL", NULL); return MUL; }
"/"                     { print_token("DIV", NULL); return DIV; }
"("                     { print_token("LPAREN", NULL); return LPAREN; }
")"                     { print_token("RPAREN", NULL); return RPAREN; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); print_token("ID", yytext); return ID; }
[0-9]+                  { yylval.val = atoi(yytext); print_token("NUM", yytext); return NUM; }
.                       { printf("UNKNOWN_TOKEN(%s)\n", yytext); }
%%

int yywrap() {
    return 1;
}
