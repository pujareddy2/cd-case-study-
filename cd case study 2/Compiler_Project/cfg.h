#ifndef CFG_H
#define CFG_H

#include "basicblock.h"

/* Linked list of edges in CFG */
typedef struct CFGEdge {
    int target_block;
    struct CFGEdge* next;
} CFGEdge;

/* Node in the Control Flow Graph (CFG) */
typedef struct CFGNode {
    BasicBlock* block;
    CFGEdge* successors;
    CFGEdge* predecessors;
    struct CFGNode* next;
} CFGNode;

extern CFGNode* cfg_head;

/* Constructs CFG nodes and edges by analyzing block jumps/fall-throughs */
void construct_cfg();

/* Prints CFG textual representation (Adjacency List, Predecessors, Successors) */
void print_cfg_text();

/* Generates Graphviz DOT output for visual CFG diagram */
void print_cfg_dot();

#endif
