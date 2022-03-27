class Token:
    def __init__(self, _type, _val=None):
        self.type = _type
        self.value = _val

    def __eq__(self, other):
        return self.type == other.type

    def __hash__(self):
        return hash(self.type)

    def __str__(self):
        return 'type:{}, value:{}'.format(self.type, self.value)


COLON = Token('COLON', ':')
COMMA = Token('COMMA', ',')
DOT = Token('DOT', '.')
PLUS = Token('PLUS', '+')
MINUS = Token('MINUS', '=')
TIMES = Token('TIMES', '*')
DIVIDE = Token('DIVIDE', '/')
MODULO = Token('MODULO', '%')
LBRACE = Token('LBRACE', '{')
LBRACKET = Token('LBRACKET', '[')
LPAREN = Token('LPAREN', '(')
RBRACE = Token('RBRACE', '}')
RBRACKET = Token('RBRACKET', ']')
RPAREN = Token('RPAREN', ')')
ASSIGN = Token('ASSIGN', '=')
GT = Token('GT', '>')
LT = Token('LT', '<')
EQUAL = Token('EQUAL', '==')
GTE = Token('GTE', '>=')
LTE = Token('LTE', '<=')
NOTEQUAL = Token('NOTEQUAL', '!=')

IF = Token('IF')
ELSE = Token('ELSE')
FOR = Token('FOR')
IN = Token('IN')
WHILE = Token('WHILE')
FUNC = Token('FUNC')
RETURN = Token('RETURN')
AND = Token('AND')
NOT = Token('NOT')
OR = Token('OR')

INT = Token('INT')
DOUBLE = Token('DOUBLE')
STR = Token('STR')
NAME = Token('NAME')

EOF = Token('EOF', -1)
EOL = Token('EOL', '\n')

single_char_operators = {
    ':': COLON,
    ',': COMMA,
    '.': DOT,
    '+': PLUS,
    '-': MINUS,
    '*': TIMES,
    '/': DIVIDE,
    '%': MODULO,
    '{': LBRACE,
    '[': LBRACKET,
    '(': LPAREN,
    '}': RBRACE,
    ']': RBRACKET,
    ')': RPAREN,
}

double_char_operators = {
    '=': ASSIGN,
    '>': GT,
    '<': LT,
    '!': NOT,
    '==': EQUAL,
    '>=': GTE,
    '<=': LTE,
    '!=': NOTEQUAL
}

keywords = [
    'if',
    'else',
    'for',
    'in',
    'while',
    'func',
    'return',
    'and',
    'not',
    'or',
]
