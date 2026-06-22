#ifndef TAC_H
#define TAC_H

#include "ast.h"

// Structure to hold a single Three Address Code instruction
typedef struct TAC {
    char op[5];
    char arg1[50];
    char arg2[50];
    char result[50];
    struct TAC *next;
} TAC;

void generate_tac(ASTNode *node, char *result);
void print_tac();
void clear_tac();

#endif
