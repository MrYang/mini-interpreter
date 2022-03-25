from token import *


class Lexer:
    def __init__(self, fp):
        self.fp = fp

    def next_token(self):
        for line in open(self.fp):
            n, i = len(line), 0

            while i < n:
                ch, i = line[i], i + 1
                if is_whitespace(ch):
                    continue

                if ch == '#':
                    break

                if is_name_start(ch):
                    begin = i - 1
                    while i < n and (is_name_start(line[i])) or is_digit(line[i]):
                        i += 1
                    word = line[begin:i]
                    if word in keywords:
                        yield Token(word.upper(), word)
                    else:
                        yield Token('NAME', word)
                elif is_digit(ch):
                    begin = i - 1
                    dot = False
                    while i < n:
                        if line[i] == '.':
                            if dot:
                                raise Exception('to many dot')
                            dot = True
                        elif not is_digit(line[i]):
                            break
                        i += 1
                    digit = line[begin:i]
                    yield Token('DOUBLE', float(digit)) if dot else Token('INT', int(digit))
                elif ch in '"\'':
                    end = ch
                    begin = i
                    while i < n and line[i] != end:
                        i += 1
                    if i == n:
                        raise Exception('non terminated string quote')
                    yield Token('STR', line[begin:i])
                    i += 1
                elif ch in single_char_operators:
                    if ch == ':':
                        pass

        return EOF


def is_whitespace(ch):
    return ch in ' \t\r\n'


def is_digit(ch):
    return ch in '0123456789'


def is_name_start(ch):
    return ch == '_' or ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')
