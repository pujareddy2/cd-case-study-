#ifndef AST_H
#define AST_H

typedef enum {
    NODE_ID,
    NODE_NUM,
    NODE_OP,
    NODE_ASSIGN
} NodeType;

typedef struct ASTNode {
    NodeType type;
    char *name;         // For NODE_ID
    int val;            // For NODE_NUM
    char op;            // For NODE_OP
    struct ASTNode *left;
    struct ASTNode *right;
} ASTNode;

ASTNode* create_id_node(char *name);
ASTNode* create_num_node(int val);
ASTNode* create_op_node(char op, ASTNode *left, ASTNode *right);
ASTNode* create_assign_node(ASTNode *left, ASTNode *right);
void print_ast(ASTNode *node, int level);

#endif
