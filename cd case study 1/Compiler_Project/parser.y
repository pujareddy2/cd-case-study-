%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"
#include "symbol_table.h"
#include "tac.h"

int yylex(void);
void yyerror(const char *s);

extern FILE *yyin;
%}

%union {
    int val;
    char *str;
    struct ASTNode *node;
}

/* Tokens mapping to scanner */
%token <str> ID
%token <val> NUM
%token ASSIGN PLUS MINUS MUL DIV LPAREN RPAREN

/* AST Node types for non-terminals */
%type <node> statement expr term factor

/* Operator Precedence and Associativity */
%left PLUS MINUS
%left MUL DIV

%%

program:
    statement_list
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    ID ASSIGN expr {
        ASTNode *id_node = create_id_node($1);
        insert_symbol($1, "ID", "Global", "int");
        $$ = create_assign_node(id_node, $3);
        
        printf("\n--- AST for Assignment to '%s' ---\n", $1);
        print_ast($$, 0);
        
        printf("\n--- TAC for Assignment to '%s' ---\n", $1);
        char result_var[50];
        generate_tac($$, result_var);
        print_tac();
        clear_tac();
    }
    ;

expr:
    expr PLUS term { $$ = create_op_node('+', $1, $3); }
    | expr MINUS term { $$ = create_op_node('-', $1, $3); }
    | term { $$ = $1; }
    ;

term:
    term MUL factor { $$ = create_op_node('*', $1, $3); }
    | term DIV factor { $$ = create_op_node('/', $1, $3); }
    | factor { $$ = $1; }
    ;

factor:
    LPAREN expr RPAREN { $$ = $2; }
    | ID { 
        $$ = create_id_node($1); 
        insert_symbol($1, "ID", "Global", "int");
    }
    | NUM { $$ = create_num_node($1); }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax Error: %s\n", s);
}
