#ifndef OPTIMIZER_H
#define OPTIMIZER_H

#include "basicblock.h"

/* Applies local optimizations (CSE, copy propagation, constant folding, dead code elim) */
void optimize_blocks();

/* Prints the TAC after optimizations have been applied */
void print_optimized_tac();

#endif
