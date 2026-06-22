#include <stdio.h>
#include <stdlib.h>
#include "symbol_table.h"

extern FILE *yyin;
extern int yyparse();

int main(int argc, char **argv) {
    // Open the provided input file
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            perror("Failed to open file");
            return 1;
        }
    } else {
        printf("Please provide an input file.\nUsage: ./compiler input.txt\n");
        return 1;
    }
    
    printf("Starting Compilation...\n\n");
    printf("--- Lexical Analysis (Tokens) ---\n");
    
    // Parse the file. yyparse will implicitly call yylex which prints tokens
    yyparse();
    
    // Final Output of Symbol Table
    display_symbol_table();
    
    fclose(yyin);
    printf("\nCompilation Completed Successfully.\n");
    return 0;
}
