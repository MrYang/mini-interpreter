from ast_ import *
from token_ import *
from lexer import Lexer
from parser_ import Parser

binary_func = {
    PLUS: lambda a, b: a + b,
    MINUS: lambda a, b: a - b,
    TIMES: lambda a, b: a * b,
    DIVIDE: lambda a, b: a / b,
    MODULO: lambda a, b: a % b,
    EQUAL: lambda a, b: a == b,
    NOTEQUAL: lambda a, b: a != b,
    GT: lambda a, b: a > b,
    GTE: lambda a, b: a >= b,
    LT: lambda a, b: a < b,
    LTE: lambda a, b: a <= b,
}

unary_func = {
    NOT: lambda a: not a,
    MINUS: lambda a: -a,
}


class Interpreter:
    def __init__(self, _parser):
        self.parser = _parser
        self.vars = {}
        self.nest_vars = {}

    def assign(self, key, value):
        self.vars[key] = value

    def assign_nest(self, key, value):
        self.nest_vars[key] = value

    def remove_nest(self, key):
        del self.nest_vars[key]

    def lookup(self, key):
        if key in self.nest_vars:
            return self.nest_vars[key]
        if key in self.vars:
            return self.vars[key]
        return None

    def execute(self):
        program = self.parser.program()
        self.execute_block(program.block())

    def execute_block(self, block):
        result = None
        for stmt in block.statements:
            result = self.execute_statement(stmt)

        return result

    def execute_statement(self, statement):
        stmt_type = type(statement)
        if stmt_type == Assign:
            left = statement.left_expression
            left_type = type(left)
            if left_type == Variable:
                self.assign(left.name, self.eval(statement.vale_expression))
            elif left_type == Subscript:
                container = self.eval(left.container)
                subscript = self.eval(left.subscript)
                value = self.eval(statement.vale_expression)
                container[subscript] = value

        elif stmt_type == If:
            condition = self.eval(statement.condition)
            if condition:
                self.execute_block(statement.if_body)
            else:
                self.execute_block(statement.else_body)
        elif stmt_type == While:
            condition = self.eval(statement.condition)
            while condition:
                self.execute_block(statement.body)
                condition = self.eval(statement.condition)
        elif stmt_type == For:
            iterable = self.eval(statement.iterable)
            key = statement.key
            value = statement.value
            if isinstance(iterable, list):
                for k, v in enumerate(iterable):
                    self.assign_nest(key, k)
                    self.assign_nest(value, v)
                    self.execute_block(statement.body)
            elif isinstance(iterable, dict):
                for k, v in iterable.items():
                    self.assign_nest(key, k)
                    self.assign_nest(value, v)
                    self.execute_block(statement.body)
            self.remove_nest(key)
            self.remove_nest(value)
        elif stmt_type == FuncDefinition:
            self.assign(statement.func_name, statement)
        elif stmt_type == Return:
            return self.eval(statement.result)
        elif stmt_type == ExpressionStatement:
            return self.eval(statement.expression)

    def eval(self, expression):
        expr_type = type(expression)
        if expr_type == Binary:
            left = expression.left
            right = expression.right
            operator = expression.operator
            if operator in binary_func:
                return binary_func[operator](self.eval(left), self.eval(right))
            if operator == AND:
                return self.eval(left) and self.eval(right)
            if operator == OR:
                return self.eval(left) or self.eval(right)
        elif expr_type == Unary:
            operator = expression.operator
            return unary_func[operator](self.eval(expression.operand))
        elif expr_type == Call:
            func = self.eval(expression.func_name)
            args = []
            for arg in expression.args:
                args.append(self.eval(arg))
        elif expr_type == Subscript:
            container = self.eval(expression.container)
            subscript = self.eval(expression.subscript)
            return container[subscript]
        elif expr_type == Literal:
            return expression.value
        elif expr_type == Variable:
            return self.lookup(expression.name)
        elif expr_type == List:
            arr = []
            for v in expression.values:
                arr.append(self.eval(v))
            return arr
        elif expr_type == Map:
            m = {}
            for item in expression.items():
                m[item.key] = self.eval(item.value)
            return m


if __name__ == '__main__':
    lexer = Lexer('demo.mini')
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.execute()
