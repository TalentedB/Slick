# Language Documentation: Studium
*A teaching-oriented language built for students to understand programming basics.*

---

## 1. Overview

**Language Name:** Studium 
**Version:** 1.0  
**Developed by:** Team Awesome
**Competition:** UVEC

### Description  
Studium is a simple, educational programming language designed to help beginners understand **the underlying programming basics**.  

It can execute code **line-by-line**, explaining the goal of each operation.

### Key Features
- **Line-by-line explanations** for each executed statement  
- **Support variables, loops, conditionals, and functions**  
- **Educational focus:** simple syntax, ideal for students learning programming  
- **Built using:** Python + Lark (for parsing)

---

## 2. Language Specification

### 2.1 Lexical Elements

**Comments:**
```plaintext
# This is a comment
```

**Identifiers:**
```plaintext
# This is a comment
```

**Keywords:**
```plaintext
# This is a comment
```

**Operators:**
```plaintext
# This is a comment
```

### 2.2 Grammar (EBNF)

The grammar defines the **structure and syntax rules** of Studium. It is written in EBNF notation and implemented in Lark.

The code block below show cases **Variables Declarations**, **Assignments**, **Print statements**, **Blocks**, **Expressions**, and **Primitive Literals**.

```ebnf
start ::= stmt+

stmt ::= decl_stmt
       | assign_stmt
       | print_stmt
       | block
       | expr ";"

decl_stmt ::= type_kw NAME ("=" expr)? ";"
assign_stmt ::= NAME "=" expr ";"
print_stmt ::= "print" "(" expr ")" ";"
block ::= "{" stmt* "}"

type_kw ::= "int" | "double" | "boolean" | "char" | "string"

?expr ::= logic_or
?logic_or ::= logic_and | logic_or "||" logic_and
?logic_and ::= equality | logic_and "&&" equality
?equality ::= comparison | equality ("==" | "!=") comparison
?comparison ::= addsub | comparison ("<"|"<="|">"|">=") addsub
?addsub ::= muldiv | addsub ("+"|"-") muldiv
?muldiv ::= unary | muldiv ("*"|"/"|"%") unary
?unary ::= "!" unary | "-" unary | primary
?primary ::= primitive | NAME | "(" expr ")"

primitive ::= INT_LIT | FLOAT_LIT | CHAR_LIT | STRING | "true" | "false" | "null"

```

### 2.3 Type System

Studium supports the following types:
- **int**: integers
- **double**: floating-point numbers
- **boolean**: `true` or `false`
- **char**: single character
- **string**: sequence of characters
- **nulltype**: represents absence of value

**Type Rules:**
- Assignment is allowed only between compatible types.
- Numeric widening is allowed: `int → double`.
- Numeric shortening is allowed: `double → int`.
- `null` can be assigned to `char` or `string`.
- Operations are type-checked at runtime; invalid operations raise `TypeError`.

### 2.4 Operators & Expressions

| Operator | Type         | Behavior                                         |
|----------|--------------|------------------------------------------------|
| +        | numeric/str  | Adds numbers or concatenates strings           |
| -        | numeric      | Subtracts numbers                              |
| *        | numeric      | Multiplies numbers                              |
| /        | numeric      | Divides numbers; raises ZeroDivisionError if denominator is 0 |
| %        | numeric      | Modulus                                       |
| ==, !=   | any          | Equality/Inequality                            |
| <, <=, >, >= | numeric  | Comparisons                                   |
| &&       | boolean      | Logical AND                                   |
| ||       | boolean      | Logical OR                                    |
| !        | boolean      | Logical NOT                                   |
| unary -  | numeric      | Negation                                      |

## 3. Example Programs

### 3.1 Variable Binding

### 3.2 Conditional Logic

### 3.3 Loop Example

### 3.4 Functions

## 4. Interpreter Architecture

### 4.1 Architecture Overview

Studium's interpreter follows modern language implementation that separates parsing and evaluation. This makes it easy to maintain and extend.

The interpreter consists of several layers:
```plaintext
Source Code
   ↓
Lexer & Parser (via Lark)
   ↓
Abstract Syntax Tree (AST)
   ↓
Evaluator Engine (Transforms AST)
   ↓
Output
   ↓
Explanation Layer (Educational Output)
```

### 4.2 Layer Responsibilities

1. **Lexer & Parser**
   - Uses **Lark** to tokenize source code and generate a parse tree.  
   - Transforms text input into an **Abstract Syntax Tree (AST)** for evaluation.
        - Text input means source code.

2. **Abstract Syntax Tree (AST)**
   - Represents the program as a **hierarchy of nodes**, such as:
        - Statements (`decl_stmt`, `assign_stmt`, `print_stmt`, `block`)  
        - Expressions (`addsub`, `muldiv`, `logic_or`)  
        - Primitives (`INT_LIT`, `STRING`, `boolean`)  
   - AST makes it easy to traverse and evaluate code **recursively**.

3. **Evaluator Engine**
   - Walks the AST nodes to **execute statements** and **evaluate expressions**.  
   - Responsibilities:
      - Evaluate arithmetic, logical and unary expressions.
      - Execute statements: variable declarations, assignments, prints, blocks and loops.
      - Type-check values using `typeof()` and `is_assignable()`.

4. **Explanation Layer**
   - Generates **step-by-step output** for each executed line.  
   - Prints:
     - Variable creation and updates  
     - Expression evaluations  
     - Conditional and block decisions  
     - Print outputs

### 4.3 Evaluator Engine
The interpreter in Studium is implemented as a **class-based AST evaluator** using Lark’s `Transformer`.

Key Features:
- **Lark Transformer Integration**
  - Uses `@v_args(inline=True)` to simplify method signatures, allowing each AST node to be passed directly as function arguments.
  - Example: `def addsub(self, left, op, right)` receives operands and operator directly from the parser.

- **Environment**
  - `__init__` initializes an **environment dictionary** that tracks:
    - Variable names  
    - Types (`int`, `double`, `boolean`, `char`, `string`)  
    - Values  

- **Expression Evaluation**
  - Evaluates arithmetic, logical, and unary operations using internal functions.  
  - Operations are type-checked during evaluation.  

- **Type Management**
  - `typeof(expr) -> str` returns the type of a given expression.  
  - `is_assignable(target_type, value_type) -> bool` ensures assignments obey type rules.  

- **Statements Handling**
  - **Variable Declarations**: Adds variable to environment and optionally evaluates initializer.  
  - **Assignments**: Checks type compatibility and updates the environment.  
  - **Print Statements**: Evaluates expressions and outputs values to the explanation layer.  
  - **Blocks**: Handles nested scopes (future-proofed for loops and function scopes).

- **Extensibility**
  - The evaluator currently handles expressions, assignments, conditional and loops.  
  - It is designed to **extend to functions and classes** seamlessly.

#### 4.3.1 Evalutator Engine Methods
| Method Name         | Arguments                        | Purpose |
|--------------------|---------------------------------|---------|
| int_lit / float_lit / char_lit / string_lit | Token | Converts literal tokens to Python values |
| true_lit / false_lit / null_lit | - | Returns corresponding Python value |
| var                 | Token | Retrieves variable value from environment |
| addsub / muldiv     | a, op_tok, b | Performs arithmetic operations with type checking |
| cmp / eq            | a, op_tok, b | Performs comparison operations |
| lor / land          | a, b | Performs logical OR / AND |
| neg_evaluator / not_evaluator | x | Performs unary operations |
| if_stmt             | condition, then_block, else_block | Evaluates conditional statement |
| while_stmt          | condition_tree, body_tree | Evaluates while loops |
| for_stmt            | for_init, expr, for_update, body_tree | Placeholder for future for-loops |

## 5. Error Handling

| Error Type     | Example                           | Description |
|----------------|----------------------------------|------------|
| TypeError      | 'a' - 3                           | Invalid type operation |
| ZeroDivisionError | 5 / 0                          | Division by zero |
| NameError      | print(x) when x undefined        | Variable not found |
| ValueError     | Unsupported operator             | Operator not recognized |

## 6. Flags

Educational Mode.

## 7. Implementation Details

| Component | Library/Tool | Notes |
| --------- | ------------ | ----- |
| Parser | Lark | The Grammar (of the language) defined by `.lark` file. |
| Evaluator | Python | Recursive AST evaluation. |
| CLI interface | argparse | Supports ```--explain```. |


## 8. Future Enhancements

- Implement full `for` loops with initialization, condition, update, and block execution
- Extend `Evaluator` to support:
    - User-defined functions
    - Nested function scopes
    - Classes and objects
- Integrate line-by-line explanation in real-time for educational mode
- Integration O(n) evaluator for performance analysis mode
- Itegrate automated test suites for programs for test mode.
- Add debugging features: step execution, breakpoints, variable watches

## 9. License & Credits
© 2025 Team Awesome.
This project was developed for UVEC to promote computer science education through interactive language design.

