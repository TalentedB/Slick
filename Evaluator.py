from lark import Transformer, v_args, Token
import rich
import ast
import math
from Environment import Environment
import os

def typeof(v) -> str:
    if v is None:
        return "nulltype"
    if isinstance(v, bool):
        return "boolean"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "double"
    if isinstance(v, str):
        return "char" if len(v) == 1 else "string"
    raise TypeError("Unfamiliar type found")

def is_assignable(dst: str, src: str) -> bool:
    if dst == src:
        return True
    # numeric widening: int -> double
    if dst == "double" and src == "int":
        return True
    # numeric shortening: double _. int
    if dst == "int" and src == "double":
        return True
    # allow null to reference-like types
    if src == "nulltype" and dst in {"string", "char"}:
        return True
    return False

@v_args(inline=True)
class Evaluator(Transformer):
    def __init__(self, environment: Environment):
        self.environment = environment

    def typed_decl(self, type_tok, name_tok: Token, value=None):
        # Names are tokens; store by string name
        name = name_tok.value
        # Basic redefinition check in current env only (optional)
        if name in self.environment.vars:
            raise ValueError(f"You have redefined the variable {name}.")
        self.environment.define(name, value)
        return value
    
    def assign(self, name_tok: Token, expr):
        # Children are already transformed; don't visit again
        name = name_tok.value
        value = expr
        self.environment.set(name, value)
        return value

    # Primitives
    def int_lit(self, tok: Token):    
        return int(tok.value)
    def float_lit(self, tok: Token):  
        return float(tok.value)
    def string_lit(self, tok: Token): 
        return ast.literal_eval(tok.value) 
    def char_lit(self, tok: Token):
        ch = ast.literal_eval(tok.value)  # "'a'" -> "a"
        if len(ch) != 1: 
            raise TypeError("char literal must be exactly one character")
        return ch
    def true_lit(self):  
        return True
    def false_lit(self): 
        return False
    def null_lit(self):  
        return None

    # Built in functions
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_stmt(self, value):
        # Child is already transformed
        print(value)

    # Helper Functions
    def var(self, name_tok: Token):
        return self.environment.get(name_tok.value)
    
    def _is_num(self, x):      
        return isinstance(x, (int, float))

    # Unary
    def neg_evaluator(self, x):
        if not self._is_num(x):
            raise TypeError("unary - needs number")
        return -x
    def not_evaluator(self, x):
        return not bool(x)

    # Comparisons / Equality
    def lt(self, a, b):  return a < b
    def le(self, a, b):  return a <= b
    def gt(self, a, b):  return a > b
    def ge(self, a, b):  return a >= b

    def eq(self, a, b):  return a == b
    def ne(self, a, b):  return a != b
    
    ## Arithmetic Operations
    def add(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a + b
        if isinstance(a, str) or isinstance(b, str):
            return str(a) + str(b)
        raise TypeError(f"Unsupported '+' for {type(a).__name__} and {type(b).__name__}")

    def sub(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a - b
        raise TypeError(f"Unsupported '-' for {type(a).__name__} and {type(b).__name__}")

    def mul(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a * b
        raise TypeError(f"Unsupported '*' for {type(a).__name__} and {type(b).__name__}")

    def div(self, a, b):
        if self._is_num(a) and self._is_num(b):
            if b == 0:
                raise ZeroDivisionError("division by zero")
            return a / b
        raise TypeError(f"Unsupported '/' for {type(a).__name__} and {type(b).__name__}")

    def mod(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a % b
        raise TypeError(f"Unsupported '%' for {type(a).__name__} and {type(b).__name__}")
    
    # Boolean OR/AND
    def lor(self, a, b):
        return bool(a) or bool(b)
    
    def land(self, a, b):
        return bool(a) and bool(b)

    # Loop Operations / Conditionals
    def for_stmt(self, for_init, cond_expr, for_update, body_tree):
        # if for_init is not None:
        #     self.visit(for_init)
        while True:
            if cond_expr is not None and not bool(cond_expr):
                break
            body_tree
            if for_update is not None:
                for_update


    def while_stmt(self, condition, body_tree):
        result = None
        while True:
            if not bool(condition):
                break
        #     result = self.visit(body_tree)
        # return result
        return body_tree


    def if_stmt(self, condition, then_block, else_block=None):
        if bool(condition):
            return then_block
        elif else_block is not None:
            return else_block
        return None

