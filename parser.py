from token import *
from ast import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = next(self.lexer.next_token())

    def next(self):
        try:
            self.current_token = next(self.lexer.next_token())
        except:
            self.current_token = EOF

    def expect(self, token):
        if self.current_token != token:
            raise Exception('expect token:%s' % token.type)
        self.next()

    def match(self, *operators):
        for operator in operators:
            if self.current_token == operator:
                return True
        return False

    def program(self):
        block = self.statements(EOF)
        return Program(block)

    def statements(self, end):
        statements = []
        while self.current_token != end:
            stmt = self.statement()
            statements.append(stmt)
        return statements

    # statement = if | while | for | return | func | assign | expression
    # assign = NAME ASSIGN expression
    #          call subscript ASSIGN expression
    def statement(self):
        tok = self.current_token
        if tok == IF:
            return self.if_()
        elif tok == WHILE:
            return self.while_()
        elif tok == FOR:
            return self.for_()
        elif tok == RETURN:
            return self.return_()
        elif tok == FUNC:
            pass

        expr = self.expression()
        if self.current_token == ASSIGN:
            self.next()
            value = self.expression()
            return Assign(expr, value)
        return ExpressionStatement(expr)

    # if = IF expression block |
    #      IF expression block ELSE block |
    #      IF expression block ELSE IF
    def if_(self):
        self.expect(IF)
        condition = self.expression()
        body = self.block()
        else_body = Block([])
        if self.current_token == ELSE:
            self.next()
            if self.current_token == LBRACE:
                else_body = self.block()
            elif self.current_token == IF:
                else_body = Block([self.if_()])
            else:
                raise 'error program if'

        return If(condition, body, else_body)

    # while = WHILE expression block
    def while_(self):
        self.expect(WHILE)
        condition = self.expression()
        body = self.block()
        return While(condition, body)

    # for = FOR NAME, NAME IN expression block
    def for_(self):
        self.expect(FOR)
        key = self.current_token.value
        self.expect(NAME)
        self.expect(COMMA)
        value = self.current_token.value
        self.expect(NAME)
        self.expect(IN)
        iterable = self.expression()
        body = self.block()
        return For(key, value, iterable, body)

    # return = RETURN expression
    def return_(self):
        self.expect(RETURN)
        return Return(self.expression())

    def block(self):
        self.expect(LBRACE)
        body = self.statements(RBRACE)
        self.expect(RBRACE)
        return body

    def expression(self):
        pass
