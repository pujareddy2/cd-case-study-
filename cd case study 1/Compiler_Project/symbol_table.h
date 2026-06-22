#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H

typedef struct SymbolEntry {
    char lexeme[50];
    char token_type[20];
    char scope[20];
    char data_type[20];
    struct SymbolEntry *next;
} SymbolEntry;

void insert_symbol(char *lexeme, char *token_type, char *scope, char *data_type);
SymbolEntry* lookup_symbol(char *lexeme);
void display_symbol_table();

#endif
