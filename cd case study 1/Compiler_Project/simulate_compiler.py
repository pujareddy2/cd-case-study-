import sys
import re

# Token Types
class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

def lexer(text):
    tokens = []
    # Token regexes
    rules = [
        ('ASSIGN', r':='),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MUL', r'\*'),
        ('DIV', r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NUM', r'\d+'),
        ('SKIP', r'[ \t\r\n]+'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in rules)
    for mo in re.finditer(tok_regex, text):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'ID':
            print(f"ID({value})")
        elif kind == 'NUM':
            print(f"NUM({value})")
        else:
            print(f"{kind}")
        tokens.append(Token(kind, value))
    return tokens

# AST Node
class ASTNode:
    def __init__(self, type, val=None, left=None, right=None):
        self.type = type
        self.val = val
        self.left = left
        self.right = right

temp_count = 1
tac_list = []
symbol_table = {}

def insert_symbol(lexeme, token_type, scope, data_type):
    if lexeme not in symbol_table:
        symbol_table[lexeme] = (token_type, scope, data_type)

def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    insert_symbol(t, "TEMP", "Local", "int")
    return t

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == expected_type:
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        return None

    def parse_statement(self):
        id_tok = self.match('ID')
        if id_tok and self.match('ASSIGN'):
            expr_node = self.parse_expr()
            if expr_node:
                insert_symbol(id_tok.lexeme, "ID", "Global", "int")
                return ASTNode('ASSIGN', ':=', ASTNode('ID', id_tok.lexeme), expr_node)
        return None

    def parse_expr(self):
        node = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ('PLUS', 'MINUS'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_term()
            node = ASTNode('OP', op.lexeme, node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type in ('MUL', 'DIV'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_factor()
            node = ASTNode('OP', op.lexeme, node, right)
        return node

    def parse_factor(self):
        if self.match('LPAREN'):
            node = self.parse_expr()
            self.match('RPAREN')
            return node
        id_tok = self.match('ID')
        if id_tok:
            insert_symbol(id_tok.lexeme, "ID", "Global", "int")
            return ASTNode('ID', id_tok.lexeme)
        num_tok = self.match('NUM')
        if num_tok:
            return ASTNode('NUM', num_tok.lexeme)
        return None

def print_ast(node, level=0):
    if not node: return
    indent = "  " * level
    if node.type in ('ID', 'NUM'):
        print(f"{indent}{node.val}")
    else:
        print(f"{indent}{node.val}")
    print_ast(node.left, level + 1)
    print_ast(node.right, level + 1)

def generate_tac(node):
    if node.type in ('ID', 'NUM'):
        return node.val
    elif node.type == 'OP':
        left_res = generate_tac(node.left)
        right_res = generate_tac(node.right)
        t = new_temp()
        tac_list.append(f"{t} = {left_res} {node.val} {right_res}")
        return t
    elif node.type == 'ASSIGN':
        right_res = generate_tac(node.right)
        left_res = generate_tac(node.left)
        tac_list.append(f"{left_res} := {right_res}")
        return left_res

def display_symbol_table():
    print("\n--- Final Symbol Table ---")
    print(f"{'Lexeme':<15} {'Token Type':<15} {'Scope':<15} {'Data Type':<15}")
    print("-" * 62)
    for lexeme, (ttype, scope, dtype) in symbol_table.items():
        print(f"{lexeme:<15} {ttype:<15} {scope:<15} {dtype:<15}")
    print("-" * 62)

def main():
    if len(sys.argv) < 2:
        return
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
    
    print("Starting Compilation...\n")
    print("--- Lexical Analysis (Tokens) ---")
    
    for line in lines:
        line = line.strip()
        if not line: continue
        tokens = lexer(line)
        parser = Parser(tokens)
        ast = parser.parse_statement()
        if ast:
            print(f"\n--- AST for Assignment to '{ast.left.val}' ---")
            print_ast(ast)
            print(f"\n--- TAC for Assignment to '{ast.left.val}' ---")
            generate_tac(ast)
            for tac in tac_list:
                print(tac)
            tac_list.clear()

    display_symbol_table()
    print("\nCompilation Completed Successfully.")

if __name__ == '__main__':
    main()
