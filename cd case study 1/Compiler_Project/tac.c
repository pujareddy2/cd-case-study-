#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tac.h"
#include "symbol_table.h"

TAC *tac_head = NULL;
TAC *tac_tail = NULL;
int temp_count = 1;

// Appends a new TAC instruction to the linked list
void add_tac(const char *op, const char *arg1, const char *arg2, const char *result) {
    TAC *new_tac = (TAC *)malloc(sizeof(TAC));
    strcpy(new_tac->op, op);
    strcpy(new_tac->arg1, arg1);
    strcpy(new_tac->arg2, arg2);
    strcpy(new_tac->result, result);
    new_tac->next = NULL;
    
    if (tac_head == NULL) {
        tac_head = new_tac;
        tac_tail = new_tac;
    } else {
        tac_tail->next = new_tac;
        tac_tail = new_tac;
    }
}

// Generates a new temporary variable (t1, t2, ...) and registers it in the symbol table
char* new_temp() {
    char *temp = (char *)malloc(10);
    sprintf(temp, "t%d", temp_count++);
    insert_symbol(temp, "TEMP", "Local", "int");
    return temp;
}

// Post-order traversal of the AST to generate Three Address Code
void generate_tac(ASTNode *node, char *result) {
    if (node == NULL) return;
    
    if (node->type == NODE_ID) {
        strcpy(result, node->name);
    } else if (node->type == NODE_NUM) {
        sprintf(result, "%d", node->val);
    } else if (node->type == NODE_OP) {
        char left_res[50], right_res[50];
        generate_tac(node->left, left_res);
        generate_tac(node->right, right_res);
        char *temp = new_temp();
        char op_str[2] = {node->op, '\0'};
        add_tac(op_str, left_res, right_res, temp);
        strcpy(result, temp);
    } else if (node->type == NODE_ASSIGN) {
        char right_res[50], left_res[50];
        generate_tac(node->right, right_res);
        generate_tac(node->left, left_res);
        add_tac(":=", right_res, "", left_res);
        strcpy(result, left_res);
    }
}

// Prints out all TAC instructions
void print_tac() {
    TAC *current = tac_head;
    while (current != NULL) {
        if (strcmp(current->op, ":=") == 0) {
            printf("%s := %s\n", current->result, current->arg1);
        } else {
            printf("%s = %s %s %s\n", current->result, current->arg1, current->op, current->arg2);
        }
        current = current->next;
    }
}

// Clears the list for the next statement
void clear_tac() {
    TAC *current = tac_head;
    while (current != NULL) {
        TAC *temp = current;
        current = current->next;
        free(temp);
    }
    tac_head = NULL;
    tac_tail = NULL;
}
