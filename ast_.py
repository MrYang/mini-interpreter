class Program:
    def __init__(self, block):
        self.block = block


class Block:
    def __init__(self, statements):
        self.statements = statements


class Statement:
    pass


class Assign(Statement):
    def __init__(self, left_expression, value_expression):
        self.left_expression = left_expression
        self.vale_expression = value_expression


class FuncDefinition(Statement):
    def __init__(self, func_name, params, body_block):
        self.func_name = func_name
        self.params = params
        self.body = body_block


class If(Statement):
    def __init__(self, condition_expression, if_body_block, else_body_block):
        self.condition = condition_expression
        self.if_body = if_body_block
        self.else_body = else_body_block


class While(Statement):
    def __init__(self, condition_expression, body_block):
        self.condition = condition_expression
        self.body = body_block


class For(Statement):
    def __init__(self, key, value, iterable_expression, body_block):
        self.key = key
        self.value = value
        self.iterable = iterable_expression
        self.body = body_block


class Return(Statement):
    def __init__(self, result_expression):
        self.result = result_expression


class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression


class Expression:
    pass


class Binary(Expression):
    def __init__(self, left_expression, operator, right_expression):
        self.left = left_expression
        self.operator = operator
        self.right = right_expression


class Unary(Expression):
    def __init__(self, operator, operand_expression):
        self.operator = operator
        self.operand = operand_expression


class Call(Expression):
    def __init__(self, func_name_expression, args_expressions):
        self.func_name = func_name_expression
        self.args = args_expressions


class Subscript(Expression):
    def __init__(self, container, subscript):
        self.container = container
        self.subscript = subscript


class Literal(Expression):
    def __init__(self, value):
        self.value = value


class Variable(Expression):
    def __init__(self, name):
        self.name = name


class List(Expression):
    def __init__(self, value_expression):
        self.values = value_expression


class Map(Expression):
    def __init__(self, items):
        self.items = items


class MapItem:
    def __init__(self, key, value):
        self.key = key
        self.value = value
