#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

// Creates an AST node for an Identifier
ASTNode* create_id_node(char *name) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_ID;
    node->name = strdup(name);
    node->left = NULL;
    node->right = NULL;
    return node;
}

// Creates an AST node for a Number
ASTNode* create_num_node(int val) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_NUM;
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
}

// Creates an AST node for an Operator (+, -, *, /)
ASTNode* create_op_node(char op, ASTNode *left, ASTNode *right) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_OP;
    node->op = op;
    node->left = left;
    node->right = right;
    return node;
}

// Creates an AST node for an Assignment (:=)
ASTNode* create_assign_node(ASTNode *left, ASTNode *right) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->type = NODE_ASSIGN;
    node->op = '='; // Internal representation of assignment
    node->left = left;
    node->right = right;
    return node;
}

// Prints the AST in a tree-like structure using indentation
void print_ast(ASTNode *node, int level) {
    if (node == NULL) return;
    
    for (int i = 0; i < level; i++) printf("  ");
    
    if (node->type == NODE_ID) {
        printf("%s\n", node->name);
    } else if (node->type == NODE_NUM) {
        printf("%d\n", node->val);
    } else if (node->type == NODE_OP || node->type == NODE_ASSIGN) {
        if (node->type == NODE_ASSIGN) printf(":=\n");
        else printf("%c\n", node->op);
    }
    
    print_ast(node->left, level + 1);
    print_ast(node->right, level + 1);
}
