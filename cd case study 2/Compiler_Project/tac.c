#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tac.h"

TAC* tac_head = NULL;
TAC* tac_tail = NULL;
int next_instr = 1;

void emit(char* op, char* arg1, char* arg2, char* result) {
    TAC* new_tac = (TAC*)malloc(sizeof(TAC));
    strcpy(new_tac->op, op);
    strcpy(new_tac->arg1, arg1);
    strcpy(new_tac->arg2, arg2);
    strcpy(new_tac->result, result);
    new_tac->instruction_number = next_instr++;
    new_tac->next = NULL;

    if (tac_head == NULL) {
        tac_head = new_tac;
        tac_tail = new_tac;
    } else {
        tac_tail->next = new_tac;
        tac_tail = new_tac;
    }
}

void print_tac() {
    TAC* curr = tac_head;
    printf("--- Original Three Address Code ---\n");
    while (curr != NULL) {
        printf("%d: ", curr->instruction_number);
        if (strcmp(curr->op, "=") == 0) {
            printf("%s = %s\n", curr->result, curr->arg1);
        } else if (strcmp(curr->op, "goto") == 0) {
            printf("goto %s\n", curr->arg1);
        } else if (strcmp(curr->op, "<") == 0 || strcmp(curr->op, ">") == 0 ||
                   strcmp(curr->op, "<=") == 0 || strcmp(curr->op, ">=") == 0 ||
                   strcmp(curr->op, "==") == 0 || strcmp(curr->op, "!=") == 0) {
            printf("if %s %s %s %s\n", curr->arg1, curr->op, curr->arg2, curr->result);
        } else {
            printf("%s = %s %s %s\n", curr->result, curr->arg1, curr->op, curr->arg2);
        }
        curr = curr->next;
    }
    printf("-----------------------------------\n");
}
