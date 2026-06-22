#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "basicblock.h"

BasicBlock* bb_head = NULL;

int leaders[1000];
int leader_count = 0;

int is_leader(int instr_no) {
    for (int i = 0; i < leader_count; i++) {
        if (leaders[i] == instr_no) return 1;
    }
    return 0;
}

void add_leader(int instr_no) {
    if (!is_leader(instr_no)) {
        leaders[leader_count++] = instr_no;
    }
}

void identify_leaders() {
    if (tac_head == NULL) return;
    add_leader(tac_head->instruction_number);

    TAC* curr = tac_head;
    while (curr != NULL) {
        if (strcmp(curr->op, "goto") == 0) {
            if (strcmp(curr->arg1, "_") != 0) {
                add_leader(atoi(curr->arg1));
            }
            if (curr->next != NULL) {
                add_leader(curr->next->instruction_number);
            }
        } else if (strncmp(curr->result, "goto", 4) == 0) {
            if (strcmp(curr->result + 5, "_") != 0) {
                add_leader(atoi(curr->result + 5));
            }
            if (curr->next != NULL) {
                add_leader(curr->next->instruction_number);
            }
        }
        curr = curr->next;
    }

    for (int i = 0; i < leader_count - 1; i++) {
        for (int j = i + 1; j < leader_count; j++) {
            if (leaders[i] > leaders[j]) {
                int temp = leaders[i];
                leaders[i] = leaders[j];
                leaders[j] = temp;
            }
        }
    }
}

void construct_basic_blocks() {
    if (leader_count == 0) return;
    BasicBlock* curr_bb = NULL;
    int current_leader_idx = 0;

    TAC* curr_tac = tac_head;
    while (curr_tac != NULL) {
        if (current_leader_idx < leader_count && curr_tac->instruction_number == leaders[current_leader_idx]) {
            BasicBlock* new_bb = (BasicBlock*)malloc(sizeof(BasicBlock));
            new_bb->block_id = current_leader_idx + 1;
            new_bb->head = curr_tac;
            new_bb->tail = curr_tac;
            new_bb->next = NULL;

            if (bb_head == NULL) {
                bb_head = new_bb;
                curr_bb = new_bb;
            } else {
                curr_bb->next = new_bb;
                curr_bb = new_bb;
            }
            current_leader_idx++;
        } else {
            curr_bb->tail = curr_tac;
        }
        curr_tac = curr_tac->next;
    }
}

void print_basic_blocks() {
    printf("--- Leaders ---\n");
    for (int i = 0; i < leader_count; i++) {
        printf("%d ", leaders[i]);
    }
    printf("\n\n--- Basic Blocks ---\n");
    BasicBlock* curr_bb = bb_head;
    while (curr_bb != NULL) {
        printf("Block B%d:\n", curr_bb->block_id);
        TAC* curr_tac = curr_bb->head;
        while (curr_tac != NULL) {
            printf("  %d: ", curr_tac->instruction_number);
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
        printf("\n");
    }
}
