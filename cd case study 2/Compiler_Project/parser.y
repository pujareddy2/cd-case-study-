%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tac.h"
#include "backpatch.h"
#include "symboltable.h"
#include "basicblock.h"
#include "cfg.h"
#include "optimizer.h"

extern int yylex();
void yyerror(const char* s);
%}

%union {
    char str[32];
    struct {
        char place[32];
    } expr_type;
    struct {
        IntList* truelist;
        IntList* falselist;
    } bool_type;
    struct {
        IntList* nextlist;
    } stmt_type;
    int instr;
}

%token <str> ID NUM
%token IF THEN ELSE WHILE DO
%token AND OR NOT
%token ASSIGN LE GE EQ NE LT GT PLUS MINUS MUL DIV LPAREN RPAREN

%type <expr_type> E T F
%type <bool_type> B
%type <stmt_type> S L S_list
%type <instr> M N

%left OR
%left AND
%right NOT
%left PLUS MINUS
%left MUL DIV

%start program

%%
program:
    S_list {
        backpatch($1.nextlist, next_instr);
    }
    ;

S_list:
    S {
        $$.nextlist = $1.nextlist;
    }
    | S_list M S {
        backpatch($1.nextlist, $2);
        $$.nextlist = $3.nextlist;
    }
    ;

S:
    ID ASSIGN E {
        emit("=", $3.place, "", $1);
        $$.nextlist = NULL;
    }
    | IF LPAREN B RPAREN THEN M S {
        backpatch($3.truelist, $6);
        $$.nextlist = merge($3.falselist, $7.nextlist);
    }
    | IF LPAREN B RPAREN THEN M S N ELSE M S {
        backpatch($3.truelist, $6);
        backpatch($3.falselist, $10);
        IntList* temp = merge($7.nextlist, $8.nextlist);
        $$.nextlist = merge(temp, $11.nextlist);
    }
    | WHILE M LPAREN B RPAREN DO M S {
        backpatch($8.nextlist, $2);
        backpatch($4.truelist, $7);
        $$.nextlist = $4.falselist;
        char buf[16];
        sprintf(buf, "%d", $2);
        emit("goto", buf, "", "");
    }
    ;

M:
    {
        $$ = next_instr;
    }
    ;

N:
    {
        $$ = next_instr;
        $$.nextlist = makelist(next_instr);
        emit("goto", "_", "", "");
    }
    ;

B:
    B OR M B {
        backpatch($1.falselist, $3);
        $$.truelist = merge($1.truelist, $4.truelist);
        $$.falselist = $4.falselist;
    }
    | B AND M B {
        backpatch($1.truelist, $3);
        $$.truelist = $4.truelist;
        $$.falselist = merge($1.falselist, $4.falselist);
    }
    | NOT B {
        $$.truelist = $2.falselist;
        $$.falselist = $2.truelist;
    }
    | LPAREN B RPAREN {
        $$.truelist = $2.truelist;
        $$.falselist = $2.falselist;
    }
    | E LT E {
        $$.truelist = makelist(next_instr);
        $$.falselist = makelist(next_instr + 1);
        emit("<", $1.place, $3.place, "goto _");
        emit("goto", "_", "", "");
    }
    | E GT E {
        $$.truelist = makelist(next_instr);
        $$.falselist = makelist(next_instr + 1);
        emit(">", $1.place, $3.place, "goto _");
        emit("goto", "_", "", "");
    }
    | E LE E {
        $$.truelist = makelist(next_instr);
        $$.falselist = makelist(next_instr + 1);
        emit("<=", $1.place, $3.place, "goto _");
        emit("goto", "_", "", "");
    }
    | E GE E {
        $$.truelist = makelist(next_instr);
        $$.falselist = makelist(next_instr + 1);
        emit(">=", $1.place, $3.place, "goto _");
        emit("goto", "_", "", "");
    }
    | E EQ E {
        $$.truelist = makelist(next_instr);
        $$.falselist = makelist(next_instr + 1);
        emit("==", $1.place, $3.place, "goto _");
        emit("goto", "_", "", "");
    }
    | E NE E {
        $$.truelist = makelist(next_instr);
        $$.falselist = makelist(next_instr + 1);
        emit("!=", $1.place, $3.place, "goto _");
        emit("goto", "_", "", "");
    }
    ;

E:
    E PLUS T {
        strcpy($$.place, new_temp());
        emit("+", $1.place, $3.place, $$.place);
    }
    | E MINUS T {
        strcpy($$.place, new_temp());
        emit("-", $1.place, $3.place, $$.place);
    }
    | T {
        strcpy($$.place, $1.place);
    }
    ;

T:
    T MUL F {
        strcpy($$.place, new_temp());
        emit("*", $1.place, $3.place, $$.place);
    }
    | T DIV F {
        strcpy($$.place, new_temp());
        emit("/", $1.place, $3.place, $$.place);
    }
    | F {
        strcpy($$.place, $1.place);
    }
    ;

F:
    LPAREN E RPAREN {
        strcpy($$.place, $2.place);
    }
    | ID {
        strcpy($$.place, $1);
    }
    | NUM {
        strcpy($$.place, $1);
    }
    ;

%%

void yyerror(const char* s) {
    fprintf(stderr, "Syntax Error: %s\n", s);
}
