#include <stdio.h>
#include <stdlib.h>
#include "tac.h"
#include "basicblock.h"
#include "cfg.h"
#include "optimizer.h"

extern int yyparse();
extern FILE* yyin;

int main(int argc, char** argv) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            printf("Error opening file: %s\n", argv[1]);
            return 1;
        }
    }
    
    printf("--- Compiling ---\n");
    yyparse();
    
    printf("\n");
    print_tac();
    
    printf("\n");
    identify_leaders();
    construct_basic_blocks();
    print_basic_blocks();
    
    printf("\n");
    construct_cfg();
    print_cfg_text();
    print_cfg_dot();
    
    printf("\n");
    optimize_blocks();
    print_optimized_tac();
    
    return 0;
}
