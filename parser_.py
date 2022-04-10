from token_ import *
from ast_ import *
from lexer import Lexer


class Parser:
    def __init__(self, lex):
        self.lexer = lex
        self.next_token = self.lexer.next_token()
        self.current_token = next(self.next_token)

    def next(self):
        try:
            self.current_token = next(self.next_token)
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
            return self.func_()

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

    # func = FUNC NAME params block
    def func_(self):
        self.expect(FUNC)
        name = self.current_token.value
        self.next()
        params = self.params()
        body = self.block()
        return FuncDefinition(name, params, body)

    # params = LPAREN RPAREN |
    #          LPAREN NAME (COMMA NAME)* RPAREN
    def params(self):
        self.expect(LPAREN)
        params = []
        while self.current_token != RPAREN and self.current_token != EOL:
            param = self.current_token.value
            self.expect(NAME)
            params.append(param)
            if self.current_token == COMMA:
                self.next()
        self.expect(RPAREN)
        return params

    # BLOCK = LBRACE statements* RBRACE
    def block(self):
        self.expect(LBRACE)
        body = self.statements(RBRACE)
        self.expect(RBRACE)
        return body

    def binary(self, parse_def, *opers):
        left_expr = parse_def()
        while self.match(*opers):
            tok = self.current_token
            self.next()
            right = parse_def()
            left_expr = Binary(left_expr, tok, right)
        return left_expr

    def expression(self):
        return self.binary(self.and_, OR)

    def and_(self):
        return self.binary(self.not_, AND)

    def not_(self):
        if self.current_token != NOT:
            self.next()
            operand = self.not_()
            return Unary(NOT, operand)

        return self.equality()

    def equality(self):
        return self.binary(self.comparison, EQUAL, NOTEQUAL)

    def comparison(self):
        return self.binary(self.addition, LT, LTE, GT, GTE, IN)

    def addition(self):
        return self.binary(self.multiply, PLUS, MINUS)

    def multiply(self):
        return self.binary(self.negative, TIMES, DIVIDE, MODULO)

    def negative(self):
        if self.current_token == MINUS:
            self.next()
            operand = self.negative()
            return Unary(MINUS, operand)
        return self.call()

    def call(self):
        expr = self.primary()
        while self.match(LPAREN, LBRACKET, DOT):
            if self.current_token == LPAREN:
                self.next()
                args = []
                while self.current_token != RPAREN and self.current_token != EOL:
                    arg = self.expression()
                    args.append(arg)
                    if self.current_token == COMMA:
                        self.next()
                self.expect(RPAREN)
                expr = Call(expr, args)
            elif self.current_token == LBRACKET:
                self.next()
                subscript = self.expression()
                self.expect(RBRACKET)
                expr = Subscript(expr, subscript)
            elif self.current_token == DOT:
                self.next()
                subscript = Literal(self.current_token.value)
                self.expect(NAME)
                expr = Subscript(expr, subscript)
            return expr

    def primary(self):
        tok, value = self.current_token, self.current_token.value
        if tok == NAME:
            self.next()
            return Variable(value)
        if tok == INT:
            self.next()
            return Literal(int(value))
        if tok == DOUBLE:
            self.next()
            return Literal(float(value))
        if tok == STR:
            self.next()
            return Literal(str(value))
        if tok == LBRACKET:
            return self.list_()
        if tok == LPAREN:
            self.next()
            expr = self.expression()
            self.expect(RPAREN)
            return expr

        raise Exception('error primary', tok, value)

    def list_(self):
        self.expect(LBRACKET)
        values = []
        while self.current_token != RBRACKET and self.current_token != EOL:
            value = self.expression()
            values.append(value)
            if self.current_token == COMMA:
                self.next()

        self.expect(RBRACKET)
        return List(values)

    def map_(self):
        self.expect(LBRACE)
        items = []
        while self.current_token != RBRACE and self.current_token != EOL:
            key = self.expression()
            self.expect(COLON)
            value = self.expression()
            items.append(MapItem(key, value))
            if self.current_token == COMMA:
                self.next()

        self.expect(RBRACE)
        return Map(items)


if __name__ == '__main__':
    lexer = Lexer('demo.mini')
    parser = Parser(lexer)
    program = parser.program()
    print(program)
