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
    def __init__(self, environment: Environment, explain=False, source_lines=None):
        super().__init__()
        self.environment = environment
        self.explain = explain
        self.source_lines = source_lines or []
        self.indent_level = 0
    
    def _explain(self, message, meta=None):
        """Print an explanation message if explain mode is enabled"""
        if self.explain:
            indent = "  " * self.indent_level
            if meta and hasattr(meta, 'line'):
                line_num = meta.line
                # Get the source line if available
                if 0 < line_num <= len(self.source_lines):
                    source = self.source_lines[line_num - 1].strip()
                    print(f"{indent}📍 Line {line_num}: {source}")
                print(f"{indent}💡 {message}")
            else:
                print(f"{indent}💡 {message}")
    
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
        # type_tok is the string type name ("int", "double", etc.)
        type_name = type_tok
        
        # Basic redefinition check in current env only (optional)
        if name in self.environment.vars:
            raise ValueError(f"You have redefined the variable {name}.")
        
        self._explain(f"Declaring variable '{name}' of type '{type_name}' with value: {value}")
        
        self.environment.define(name, value)
        return value
    
    @v_args(inline=True)
    def assign(self, name_tok: Token, expr):
        # Children are already transformed; don't visit again
        name = name_tok.value
        value = expr
        
        old_value = self.environment.get(name) if name in self.environment.vars else None
        self._explain(f"Assigning to variable '{name}': {old_value} → {value}")
        
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
    
    # Type keyword handler
    def type_kw(self, args):
        # args is the list of children
        # For type_kw rule which is: "int" | "double" | "boolean" | "char" | "string"
        # The children would be empty since it's just matching literals
        # So we need to check the tree itself
        # Actually, let's not transform this - just return a placeholder
        # and handle it in typed_decl by checking the Tree
        return "TYPE_PLACEHOLDER"

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
        self._explain(f"Printing value: {value}")
        print(value)

    # Helper Functions
    @v_args(inline=True)
    def var(self, name_tok: Token):
        name = name_tok.value
        value = self.environment.get(name)
        self._explain(f"Looking up variable '{name}': {value}")
        return value
    
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
    def lt(self, a, b):
        result = a < b
        self._explain(f"Comparing: {a} < {b} = {result}")
        return result
    @v_args(inline=True)
    def le(self, a, b):
        result = a <= b
        self._explain(f"Comparing: {a} <= {b} = {result}")
        return result
    @v_args(inline=True)
    def gt(self, a, b):
        result = a > b
        self._explain(f"Comparing: {a} > {b} = {result}")
        return result
    @v_args(inline=True)
    def ge(self, a, b):
        result = a >= b
        self._explain(f"Comparing: {a} >= {b} = {result}")
        return result

    @v_args(inline=True)
    def eq(self, a, b):
        result = a == b
        self._explain(f"Comparing: {a} == {b} = {result}")
        return result
    @v_args(inline=True)
    def ne(self, a, b):
        result = a != b
        self._explain(f"Comparing: {a} != {b} = {result}")
        return result
    
    ## Arithmetic Operations
    @v_args(inline=True)
    def add(self, a, b):
        if self._is_num(a) and self._is_num(b):
            result = a + b
            self._explain(f"Adding: {a} + {b} = {result}")
            return result
        if isinstance(a, str) or isinstance(b, str):
            result = str(a) + str(b)
            self._explain(f"Concatenating: {a} + {b} = {result}")
            return result
        raise TypeError(f"Unsupported '+' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def sub(self, a, b):
        if self._is_num(a) and self._is_num(b):
            result = a - b
            self._explain(f"Subtracting: {a} - {b} = {result}")
            return result
        raise TypeError(f"Unsupported '-' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def mul(self, a, b):
        if self._is_num(a) and self._is_num(b):
            result = a * b
            self._explain(f"Multiplying: {a} * {b} = {result}")
            return result
        raise TypeError(f"Unsupported '*' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def div(self, a, b):
        if self._is_num(a) and self._is_num(b):
            if b == 0:
                raise ZeroDivisionError("division by zero")
            result = a / b
            self._explain(f"Dividing: {a} / {b} = {result}")
            return result
        raise TypeError(f"Unsupported '/' for {type(a).__name__} and {type(b).__name__}")

    @v_args(inline=True)
    def mod(self, a, b):
        if self._is_num(a) and self._is_num(b):
            result = a % b
            self._explain(f"Modulo: {a} % {b} = {result}")
            return result
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
        
        self._explain("Starting for loop", tree.meta)
        self.indent_level += 1
        
        # Create a new scope for the for loop
        loop_env = Environment(parent=self.environment)
        old_env = self.environment
        self.environment = loop_env
        
        try:
            # Execute initialization (if present)
            if for_init_tree is not None:
                self._explain("Executing for loop initialization")
                self.transform(for_init_tree)
            
            # Loop execution
            iteration = 0
            while True:
                # Re-evaluate condition each iteration
                if cond_tree is not None:
                    cond_val = self.transform(cond_tree)
                    if not bool(cond_val):
                        self._explain(f"Loop condition is false, exiting loop after {iteration} iterations")
                        break
                    if iteration == 0:
                        self._explain(f"Loop condition is true, entering loop")
                    else:
                        self._explain(f"Loop condition is true, continuing iteration {iteration + 1}")
                
                iteration += 1
                
                # Execute body
                if body_tree is not None:
                    self.transform(body_tree)
                
                # Execute update (if present)
                if for_update_tree is not None:
                    self._explain("Executing for loop update")
                    self.transform(for_update_tree)
        finally:
            # Restore the original environment
            self.environment = old_env
            self.indent_level -= 1
            self._explain("For loop completed")
        
        return None


    def while_stmt(self, tree):
        # tree.children gives us raw, untransformed children
        children = tree.children
        condition_tree = children[0]
        body_tree = children[1]
        
        self._explain("Starting while loop", tree.meta)
        self.indent_level += 1
        
        result = None
        iteration = 0
        while True:
            # Re-evaluate condition each iteration
            cond_val = self.transform(condition_tree)
            if not bool(cond_val):
                self._explain(f"While condition is false, exiting loop after {iteration} iterations")
                break
            
            if iteration == 0:
                self._explain("While condition is true, entering loop")
            else:
                self._explain(f"While condition is true, continuing iteration {iteration + 1}")
            
            iteration += 1
            
            # Execute body
            result = self.transform(body_tree)
        
        self.indent_level -= 1
        self._explain("While loop completed")
        return result


    def if_stmt(self, tree):
        # tree.children gives us raw, untransformed children
        children = tree.children
        condition_tree = children[0]
        then_block_tree = children[1]
        else_block_tree = children[2] if len(children) > 2 else None
        
        cond_val = self.transform(condition_tree)
        self._explain(f"If condition evaluated to: {cond_val}", tree.meta)
        
        if bool(cond_val):
            self._explain("Taking 'then' branch")
            self.indent_level += 1
            result = self.transform(then_block_tree)
            self.indent_level -= 1
            return result
        elif else_block_tree is not None:
            self._explain("Taking 'else' branch")
            self.indent_level += 1
            result = self.transform(else_block_tree)
            self.indent_level -= 1
            return result
        else:
            self._explain("Skipping if statement (no else branch)")
        return None

