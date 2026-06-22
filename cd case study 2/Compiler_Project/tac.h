#ifndef TAC_H
#define TAC_H

/* Structure representing a Three Address Code instruction (Quadruple) */
typedef struct TAC {
    char op[10];
    char arg1[32];
    char arg2[32];
    char result[32];
    int instruction_number;
    struct TAC* next;
} TAC;

extern TAC* tac_head;
extern TAC* tac_tail;
extern int next_instr;

/* Emits a new TAC instruction and adds it to the global list */
void emit(char* op, char* arg1, char* arg2, char* result);

/* Prints the complete generated TAC */
void print_tac();

#endif
