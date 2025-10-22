from lark import Transformer, v_args, Token, Tree
import rich
import ast
import math
from Environment import Environment
import os

# Base functionality of some functions was written with AI, to allow for faster iterations, and was built on top of.
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

class Evaluator(Transformer):
    def __init__(self, environment: Environment):
        super().__init__()
        self.environment = environment
    
    def _transform_tree(self, tree):
        # Override to handle for_stmt and while_stmt specially
        # For these, we don't want to auto-transform children
        if tree.data in ('for_stmt', 'while_stmt', 'if_stmt'):
            # Call the method with the raw tree, not transformed children
            return getattr(self, tree.data)(tree)
        else:
            # Default behavior for all other nodes
            return super()._transform_tree(tree)

    @v_args(inline=True)
    def typed_decl(self, type_tok, name_tok: Token, value=None):
        # Names are tokens; store by string name
        name = name_tok.value
        # Basic redefinition check in current env only (optional)
        if name in self.environment.vars:
            raise ValueError(f"You have redefined the variable {name}.")
        self.environment.define(name, value)
        return value
    
    @v_args(inline=True)
    def assign(self, name_tok: Token, expr):
        # Children are already transformed; don't visit again
        name = name_tok.value
        value = expr
        self.environment.set(name, value)
        return value
    
    @v_args(inline=True)
    def assign_nosemi(self, name_tok: Token, expr):
        # Same as assign, but without semicolon (for use in for loops)
        return self.assign(name_tok, expr)
    
    @v_args(inline=True)
    def decl_nosemi(self, type_tok, name_tok: Token, value=None):
        # Same as typed_decl, but without semicolon (for use in for loops)
        return self.typed_decl(type_tok, name_tok, value)

    # Primitives
    @v_args(inline=True)
    def int_lit(self, tok: Token):    
        return int(tok.value)
    @v_args(inline=True)
    def float_lit(self, tok: Token):  
        return float(tok.value)
    @v_args(inline=True)
    def string_lit(self, tok: Token): 
        return ast.literal_eval(tok.value) 
    @v_args(inline=True)
    def char_lit(self, tok: Token):
        ch = ast.literal_eval(tok.value)  # "'a'" -> "a"
        if len(ch) != 1: 
            raise TypeError("char literal must be exactly one character")
        return ch
    @v_args(inline=True)
    def true_lit(self):  
        return True
    @v_args(inline=True)
    def false_lit(self): 
        return False
    @v_args(inline=True)
    def null_lit(self):  
        return None

    # Built in functions
    @v_args(inline=True)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    @v_args(inline=True)
    def print_stmt(self, value):
        # Child is already transformed
        print(value)

    # Helper Functions
    @v_args(inline=True)
    def var(self, name_tok: Token):
        return self.environment.get(name_tok.value)
    
    def _is_num(self, x):      
        return isinstance(x, (int, float))

    # Unary
    @v_args(inline=True)
    def neg_evaluator(self, x):
        if not self._is_num(x):
            raise TypeError("unary - needs number")
        return -x
    @v_args(inline=True)
    def not_evaluator(self, x):
        return not bool(x)

    # Comparisons / Equality
    @v_args(inline=True)
    def lt(self, a, b):  return a < b
    @v_args(inline=True)
    def le(self, a, b):  return a <= b
    @v_args(inline=True)
    def gt(self, a, b):  return a > b
    @v_args(inline=True)
    def ge(self, a, b):  return a >= b

    @v_args(inline=True)
    def eq(self, a, b):  return a == b
    @v_args(inline=True)
    def ne(self, a, b):  return a != b
    
    ## Arithmetic Operations
    @v_args(inline=True)
    def add(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a + b
        if isinstance(a, str) or isinstance(b, str):
            return str(a) + str(b)
        raise TypeError(f"Unsupported '+' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def sub(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a - b
        raise TypeError(f"Unsupported '-' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def mul(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a * b
        raise TypeError(f"Unsupported '*' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def div(self, a, b):
        if self._is_num(a) and self._is_num(b):
            if b == 0:
                raise ZeroDivisionError("division by zero")
            return a / b
        raise TypeError(f"Unsupported '/' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def mod(self, a, b):
        if self._is_num(a) and self._is_num(b):
            return a % b
        raise TypeError(f"Unsupported '%' for {type(a).__name__} and {type(b).__name__}")
    
    # Boolean OR/AND
    @v_args(inline=True)
    def lor(self, a, b):
        return bool(a) or bool(b)
    
    @v_args(inline=True)
    def land(self, a, b):
        return bool(a) and bool(b)

    # Loop Operations / Conditionals  
    # Don't use decorators for these - we want raw Tree access
    def for_stmt(self, tree):
        # tree.children gives us raw, untransformed children
        children = tree.children
        for_init_tree = children[0] if len(children) > 0 else None
        cond_tree = children[1] if len(children) > 1 else None
        for_update_tree = children[2] if len(children) > 2 else None
        body_tree = children[3] if len(children) > 3 else None
        
        # Create a new scope for the for loop
        loop_env = Environment(parent=self.environment)
        old_env = self.environment
        self.environment = loop_env
        
        try:
            # Execute initialization (if present)
            if for_init_tree is not None:
                self.transform(for_init_tree)
            
            # Loop execution
            while True:
                # Re-evaluate condition each iteration
                if cond_tree is not None:
                    cond_val = self.transform(cond_tree)
                    if not bool(cond_val):
                        break
                
                # Execute body
                if body_tree is not None:
                    self.transform(body_tree)
                
                # Execute update (if present)
                if for_update_tree is not None:
                    self.transform(for_update_tree)
        finally:
            # Restore the original environment
            self.environment = old_env
        
        return None


    def while_stmt(self, tree):
        # tree.children gives us raw, untransformed children
        children = tree.children
        condition_tree = children[0]
        body_tree = children[1]
        
        result = None
        while True:
            # Re-evaluate condition each iteration
            cond_val = self.transform(condition_tree)
            if not bool(cond_val):
                break
            # Execute body
            result = self.transform(body_tree)
        return result


    def if_stmt(self, tree):
        # tree.children gives us raw, untransformed children
        children = tree.children
        condition_tree = children[0]
        then_block_tree = children[1]
        else_block_tree = children[2] if len(children) > 2 else None
        
        cond_val = self.transform(condition_tree)
        if bool(cond_val):
            return self.transform(then_block_tree)
        elif else_block_tree is not None:
            return self.transform(else_block_tree)
        return None

