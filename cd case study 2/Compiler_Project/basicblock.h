#ifndef BASICBLOCK_H
#define BASICBLOCK_H

#include "tac.h"

/* Structure representing a Basic Block */
typedef struct BasicBlock {
    int block_id;
    TAC* head;
    TAC* tail;
    struct BasicBlock* next;
} BasicBlock;

extern BasicBlock* bb_head;

/* Identifies leader instructions according to BB formation rules */
void identify_leaders();

/* Constructs basic blocks from the identified leaders */
void construct_basic_blocks();

/* Prints all constructed basic blocks and their instructions */
void print_basic_blocks();

#endif
