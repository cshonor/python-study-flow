"""Ch. 18.3: A tiny Scheme subset interpreter using match/case (Norvig-style lis.py)."""

from __future__ import annotations

import math
import operator as op
from collections import ChainMap
from dataclasses import dataclass
from typing import Any, NoReturn, TypeAlias, cast

Symbol: TypeAlias = str
Atom: TypeAlias = float | int | Symbol
Expression: TypeAlias = Atom | list["Expression"]

KEYWORDS: frozenset[str] = frozenset({"quote", "if", "define", "set!", "lambda", "begin"})


def tokenize(source: str) -> list[str]:
    return source.replace("(", " ( ").replace(")", " ) ").split()


def parse(program: str) -> Expression:
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list[str]) -> Expression:
    if not tokens:
        raise SyntaxError("unexpected EOF")

    token = tokens.pop(0)
    if token == "(":
        expr: list[Expression] = []
        while True:
            if not tokens:
                raise SyntaxError("missing ')'")
            if tokens[0] == ")":
                tokens.pop(0)
                return expr
            expr.append(read_from_tokens(tokens))
    if token == ")":
        raise SyntaxError("unexpected ')'")
    return atom(token)


def atom(token: str) -> Atom:
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        return token


class Environment(ChainMap[Symbol, Any]):
    def change(self, key: Symbol, value: Any) -> None:
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        raise NameError(key)


def standard_env() -> dict[Symbol, Any]:
    env: dict[Symbol, Any] = {}
    env.update(vars(math))
    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "//": op.floordiv,
            "%": op.mod,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x, *y],
            "eq?": op.is_,
            "equal?": op.eq,
            "length": len,
            "list": lambda *xs: list(xs),
            "list?": lambda x: isinstance(x, list),
            "map": lambda f, xs: list(map(f, xs)),
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, (int, float)),
            "print": lambda *xs: print(*xs),
        }
    )
    return env


@dataclass(frozen=True)
class Procedure:
    parms: list[Symbol]
    body: list[Expression]
    env: Environment

    def __call__(self, *args: Any) -> Any:
        local = Environment(dict(zip(self.parms, args)), self.env)
        result: Any = None
        for exp in self.body:
            result = evaluate(exp, local)
        return result


def lispstr(exp: object) -> str:
    if isinstance(exp, list):
        return "(" + " ".join(map(lispstr, exp)) + ")"
    return str(exp)


def evaluate(exp: Expression, env: Environment) -> Any:
    match exp:
        case int(x) | float(x):
            return x
        case Symbol(name) if name not in KEYWORDS:
            try:
                return env[name]
            except KeyError as e:
                raise NameError(name) from e
        case ["quote", x]:
            return x
        case ["if", test, conseq, alt]:
            branch = conseq if evaluate(test, env) else alt
            return evaluate(branch, env)
        case ["begin", *body] if body:
            result: Any = None
            for sub in body:
                result = evaluate(sub, env)
            return result
        case ["define", Symbol(name), value_exp]:
            env[name] = evaluate(value_exp, env)
            return None
        case ["define", [Symbol(name), *parms], *body] if body:
            env[name] = Procedure(cast(list[Symbol], parms), body, env)
            return None
        case ["set!", Symbol(name), value_exp]:
            env.change(name, evaluate(value_exp, env))
            return None
        case ["lambda", [*parms], *body] if body:
            return Procedure(cast(list[Symbol], parms), body, env)
        case [func_exp, *args] if func_exp not in KEYWORDS:
            proc = evaluate(func_exp, env)
            values = [evaluate(arg, env) for arg in args]
            return proc(*values)
        case _:
            raise SyntaxError(lispstr(exp))


def repl(prompt: str = "lis.py> ") -> NoReturn:
    env = Environment({}, standard_env())
    while True:
        program = input(prompt)
        if not program.strip():
            continue
        val = evaluate(parse(program), env)
        if val is not None:
            print(lispstr(val))


def demo() -> None:
    env = Environment({}, standard_env())
    programs = [
        "(+ 1 2)",
        "(define x 13)",
        "(+ x 29)",
        "(if (> x 10) 100 200)",
        "(quote (1 2 (3 4) five))",
        "(define (square n) (* n n))",
        "(square 12)",
        "(begin (define y 5) (set! y (+ y 7)) y)",
        # Closure + set! (like a stateful averager / counter)
        "(define (make-counter)\n"
        "  (begin\n"
        "    (define count 0)\n"
        "    (lambda () (begin (set! count (+ count 1)) count))))",
        "(define c (make-counter))",
        "(c)",
        "(c)",
        "(c)",
        # The guard `if func_exp not in KEYWORDS` prevents this from being treated as a call.
        # (Here it should raise a SyntaxError, not a NameError for looking up 'lambda'.)
        "(lambda is not like this)",
    ]

    for p in programs:
        try:
            val = evaluate(parse(p), env)
        except Exception as e:  # demo output
            print("=> ERROR:", type(e).__name__, "-", e)
        else:
            if val is not None:
                print("=>", lispstr(val))


if __name__ == "__main__":
    demo()

