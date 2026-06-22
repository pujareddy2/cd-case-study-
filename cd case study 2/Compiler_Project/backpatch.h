#ifndef BACKPATCH_H
#define BACKPATCH_H

/* Linked list for backpatching lists (truelist, falselist, nextlist) */
typedef struct IntList {
    int instr_no;
    struct IntList* next;
} IntList;

/* Creates a new list containing only the instruction number i */
IntList* makelist(int i);

/* Merges two lists p1 and p2, returning the merged list */
IntList* merge(IntList* p1, IntList* p2);

/* Backpatches instructions in list p to target instruction number target_instr */
void backpatch(IntList* p, int target_instr);

#endif
