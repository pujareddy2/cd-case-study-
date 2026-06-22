#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cfg.h"

CFGNode* cfg_head = NULL;

void add_edge(CFGNode* from, BasicBlock* to_block) {
    if(from == NULL || to_block == NULL) return;
    CFGEdge* new_edge = (CFGEdge*)malloc(sizeof(CFGEdge));
    new_edge->target_block = to_block->block_id;
    new_edge->next = from->successors;
    from->successors = new_edge;

    CFGNode* to_node = cfg_head;
    while (to_node != NULL && to_node->block->block_id != to_block->block_id) {
        to_node = to_node->next;
    }
    if (to_node != NULL) {
        CFGEdge* pred_edge = (CFGEdge*)malloc(sizeof(CFGEdge));
        pred_edge->target_block = from->block->block_id;
        pred_edge->next = to_node->predecessors;
        to_node->predecessors = pred_edge;
    }
}

BasicBlock* find_block_by_instr(int instr_no) {
    BasicBlock* curr = bb_head;
    while (curr != NULL) {
        if (curr->head->instruction_number == instr_no) return curr;
        curr = curr->next;
    }
    return NULL;
}

void construct_cfg() {
    BasicBlock* curr_bb = bb_head;
    CFGNode* last_node = NULL;

    while (curr_bb != NULL) {
        CFGNode* new_node = (CFGNode*)malloc(sizeof(CFGNode));
        new_node->block = curr_bb;
        new_node->successors = NULL;
        new_node->predecessors = NULL;
        new_node->next = NULL;

        if (cfg_head == NULL) {
            cfg_head = new_node;
            last_node = new_node;
        } else {
            last_node->next = new_node;
            last_node = new_node;
        }
        curr_bb = curr_bb->next;
    }

    CFGNode* curr_node = cfg_head;
    while (curr_node != NULL) {
        TAC* tail_tac = curr_node->block->tail;
        if (strcmp(tail_tac->op, "goto") == 0 && strcmp(tail_tac->arg1, "_") != 0) {
            int target = atoi(tail_tac->arg1);
            BasicBlock* target_bb = find_block_by_instr(target);
            if (target_bb) add_edge(curr_node, target_bb);
        } else if (strncmp(tail_tac->result, "goto", 4) == 0 && strcmp(tail_tac->result + 5, "_") != 0) {
            int target = atoi(tail_tac->result + 5);
            BasicBlock* target_bb = find_block_by_instr(target);
            if (target_bb) add_edge(curr_node, target_bb);
            if (curr_node->block->next != NULL) {
                add_edge(curr_node, curr_node->block->next);
            }
        } else {
            if (curr_node->block->next != NULL) {
                add_edge(curr_node, curr_node->block->next);
            }
        }
        curr_node = curr_node->next;
    }
}

void print_cfg_text() {
    printf("--- Control Flow Graph ---\n");
    CFGNode* curr = cfg_head;
    while (curr != NULL) {
        printf("Node B%d:\n", curr->block->block_id);
        printf("  Predecessors: ");
        CFGEdge* pred = curr->predecessors;
        while (pred != NULL) {
            printf("B%d ", pred->target_block);
            pred = pred->next;
        }
        printf("\n  Successors: ");
        CFGEdge* succ = curr->successors;
        while (succ != NULL) {
            printf("B%d ", succ->target_block);
            succ = succ->next;
        }
        printf("\n\n");
        curr = curr->next;
    }
}

void print_cfg_dot() {
    printf("--- CFG DOT Format ---\ndigraph CFG {\n");
    CFGNode* curr = cfg_head;
    while (curr != NULL) {
        CFGEdge* succ = curr->successors;
        while (succ != NULL) {
            printf("  B%d -> B%d;\n", curr->block->block_id, succ->target_block);
            succ = succ->next;
        }
        curr = curr->next;
    }
    printf("}\n----------------------\n");
}
