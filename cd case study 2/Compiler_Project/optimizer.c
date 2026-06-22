#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "optimizer.h"

void optimize_blocks() {
    BasicBlock* curr_bb = bb_head;
    while (curr_bb != NULL) {
        TAC* curr_tac = curr_bb->head;
        while (curr_tac != NULL) {
            // Constant folding
            if (curr_tac->arg1[0] >= '0' && curr_tac->arg1[0] <= '9' &&
                curr_tac->arg2[0] >= '0' && curr_tac->arg2[0] <= '9' &&
                strcmp(curr_tac->op, "=") != 0 && strcmp(curr_tac->op, "goto") != 0 &&
                strncmp(curr_tac->result, "goto", 4) != 0) {
                
                int val1 = atoi(curr_tac->arg1);
                int val2 = atoi(curr_tac->arg2);
                int res = 0;
                int folded = 1;
                
                if (strcmp(curr_tac->op, "+") == 0) res = val1 + val2;
                else if (strcmp(curr_tac->op, "-") == 0) res = val1 - val2;
                else if (strcmp(curr_tac->op, "*") == 0) res = val1 * val2;
                else if (strcmp(curr_tac->op, "/") == 0 && val2 != 0) res = val1 / val2;
                else folded = 0;
                
                if (folded) {
                    strcpy(curr_tac->op, "=");
                    sprintf(curr_tac->arg1, "%d", res);
                    strcpy(curr_tac->arg2, "");
                }
            }
            
            // Common Subexpression Elimination
            TAC* inner_tac = curr_tac->next;
            while (inner_tac != NULL) {
                if (strcmp(curr_tac->op, inner_tac->op) == 0 &&
                    strcmp(curr_tac->arg1, inner_tac->arg1) == 0 &&
                    strcmp(curr_tac->arg2, inner_tac->arg2) == 0 &&
                    strcmp(curr_tac->op, "=") != 0 && strcmp(curr_tac->op, "goto") != 0 &&
                    strncmp(curr_tac->result, "goto", 4) != 0) {
                    
                    strcpy(inner_tac->op, "=");
                    strcpy(inner_tac->arg1, curr_tac->result);
                    strcpy(inner_tac->arg2, "");
                }
                
                if (inner_tac == curr_bb->tail) break;
                inner_tac = inner_tac->next;
            }
            
            if (curr_tac == curr_bb->tail) break;
            curr_tac = curr_tac->next;
        }
        curr_bb = curr_bb->next;
    }
}

void print_optimized_tac() {
    printf("--- Optimized TAC ---\n");
    BasicBlock* curr_bb = bb_head;
    while (curr_bb != NULL) {
        TAC* curr_tac = curr_bb->head;
        while (curr_tac != NULL) {
            printf("%d: ", curr_tac->instruction_number);
            if (strcmp(curr_tac->op, "=") == 0) {
                printf("%s = %s\n", curr_tac->result, curr_tac->arg1);
            } else if (strcmp(curr_tac->op, "goto") == 0) {
                printf("goto %s\n", curr_tac->arg1);
            } else if (strcmp(curr_tac->op, "<") == 0 || strcmp(curr_tac->op, ">") == 0 ||
                       strcmp(curr_tac->op, "<=") == 0 || strcmp(curr_tac->op, ">=") == 0 ||
                       strcmp(curr_tac->op, "==") == 0 || strcmp(curr_tac->op, "!=") == 0) {
                printf("if %s %s %s %s\n", curr_tac->arg1, curr_tac->op, curr_tac->arg2, curr_tac->result);
            } else {
                printf("%s = %s %s %s\n", curr_tac->result, curr_tac->arg1, curr_tac->op, curr_tac->arg2);
            }
            if (curr_tac == curr_bb->tail) break;
            curr_tac = curr_tac->next;
        }
        curr_bb = curr_bb->next;
    }
    printf("---------------------\n");
}
