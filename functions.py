def call(interpreter, args_name, args, body):
    for idx, arg in enumerate(args):
        interpreter.assign_nest(args_name[idx], arg)

    result = interpreter.execute_block(body)
    for arg in args_name:
        interpreter.remove_nest(arg)
    return result


def print_func(interpreter, args):
    print(*args)
    return None


builtin_func = {
    'print': print_func
}
