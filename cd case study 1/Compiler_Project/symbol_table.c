#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "symbol_table.h"

#define TABLE_SIZE 100

// Hash table array
SymbolEntry *symbol_table[TABLE_SIZE];

// Simple hash function
unsigned int hash(char *str) {
    unsigned int hash = 5381;
    int c;
    while ((c = *str++))
        hash = ((hash << 5) + hash) + c;
    return hash % TABLE_SIZE;
}

// Inserts a symbol into the hash table if it does not already exist
void insert_symbol(char *lexeme, char *token_type, char *scope, char *data_type) {
    if (lookup_symbol(lexeme) != NULL) return; // Already exists
    
    unsigned int index = hash(lexeme);
    SymbolEntry *new_entry = (SymbolEntry *)malloc(sizeof(SymbolEntry));
    strcpy(new_entry->lexeme, lexeme);
    strcpy(new_entry->token_type, token_type);
    strcpy(new_entry->scope, scope);
    strcpy(new_entry->data_type, data_type);
    
    new_entry->next = symbol_table[index];
    symbol_table[index] = new_entry;
}

// Looks up a symbol by lexeme
SymbolEntry* lookup_symbol(char *lexeme) {
    unsigned int index = hash(lexeme);
    SymbolEntry *entry = symbol_table[index];
    while (entry != NULL) {
        if (strcmp(entry->lexeme, lexeme) == 0) return entry;
        entry = entry->next;
    }
    return NULL;
}

// Displays the formatted symbol table
void display_symbol_table() {
    printf("\n--- Symbol Table ---\n");
    printf("%-15s %-15s %-15s %-15s\n", "Lexeme", "Token Type", "Scope", "Data Type");
    printf("--------------------------------------------------------------\n");
    for (int i = 0; i < TABLE_SIZE; i++) {
        SymbolEntry *entry = symbol_table[i];
        while (entry != NULL) {
            printf("%-15s %-15s %-15s %-15s\n", entry->lexeme, entry->token_type, entry->scope, entry->data_type);
            entry = entry->next;
        }
    }
    printf("--------------------------------------------------------------\n");
}
