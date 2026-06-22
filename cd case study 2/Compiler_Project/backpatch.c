#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "backpatch.h"
#include "tac.h"

IntList* makelist(int i) {
    IntList* list = (IntList*)malloc(sizeof(IntList));
    list->instr_no = i;
    list->next = NULL;
    return list;
}

IntList* merge(IntList* p1, IntList* p2) {
    if (p1 == NULL) return p2;
    if (p2 == NULL) return p1;
    IntList* curr = p1;
    while (curr->next != NULL) {
        curr = curr->next;
    }
    curr->next = p2;
    return p1;
}

void backpatch(IntList* p, int target_instr) {
    IntList* curr_list = p;
    while (curr_list != NULL) {
        int instr_no = curr_list->instr_no;
        TAC* curr_tac = tac_head;
        while (curr_tac != NULL) {
            if (curr_tac->instruction_number == instr_no) {
                char buf[16];
                sprintf(buf, "%d", target_instr);
                if (strcmp(curr_tac->op, "goto") == 0) {
                    strcpy(curr_tac->arg1, buf);
                } else {
                    sprintf(curr_tac->result, "goto %s", buf);
                }
                break;
            }
            curr_tac = curr_tac->next;
        }
        curr_list = curr_list->next;
    }
}
