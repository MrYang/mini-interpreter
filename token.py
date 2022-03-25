single_char_operators = [
    ':',
    ',',
    '.',
    '@',
    '+',
    '-',
    '*',
    '/',
    '%',
    '{',
    '}',
    '[',
    ']',
    '(',
    ')',
]

double_char_operators = [
    '=', '>', '<', '!'
]

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
    'true',
    'false',
    'null',
]


class Token:
    def __init__(self, _type, _val=None):
        self.type = _type
        self.value = _val

    def __str__(self):
        return 'type:{}, value:{}'.format(self.type, self.value)


EOF = Token('EOF', -1)
EOL = Token('EOL', '\n')
