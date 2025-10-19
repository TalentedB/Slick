# Language Documentation: Studium
*A teaching-oriented language built by students for students to understand programming basics.*

---

## 1. Overview

**Language Name:** Studium

**Version:** 1.0  

**Developed by:** Team Awesome

**Competition:** UVEC 2025

### Description  
Studium is a simple, educational programming language designed to help beginners understand **the underlying programming basics**.  

It is working towards a **line-by-line** execution, explaining the goal of each operation.

### Key Features
- **Support variables, loops and conditionals**  
- **Educational focus:** simple syntax, ideal for students learning programming  
- **Built using:** Python + Lark (for parsing)


## 2. Language Specification

### 2.1 Type System

Studium supports the following types:
- **int**: integers
- **double**: floating-point numbers
- **boolean**: `true` or `false`
- **char**: single character
- **string**: sequence of characters

**Type Rules:**
- Assignment is allowed only between compatible types.
- Numeric widening is allowed: `int → double`.
- Numeric shortening is allowed: `double → int`.
- Operations are type-checked at runtime; invalid operations raise `TypeError`.

### 2.2 Operators & Expressions

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

### 2.3 Keywords

| Keyword | Description | Example |
|---------|-------------|---------|
| `if`    | Begins a conditional branch. Executes the `then` block if the condition is true. | `if (x > 0) { print(x); }` |
| `else`  | Optional part of an `if` statement that executes if the condition is false. | `if (x > 0) { print(x); } else { print(0); }` |
| `for`   | Begins a `for` loop (currently planned/future implementation). | `for (int i = 0; i < 10; i = i + 1) { print(i); }` |
| `while` | Begins a `while` loop that executes while a condition is true. | `while (x < 10) { x = x + 1; }` |
| `print` | Outputs the value of an expression to the console (or explanation layer). | `print("Hello")` |
| `int`   | Declares an integer variable. | `int x = 5;` |
| `double`| Declares a floating-point variable. | `double y = 3.14;` |
| `boolean` | Declares a boolean variable. | `boolean flag = true;` |
| `char`  | Declares a single character variable. | `char c = 'a';` |
| `string`| Declares a string variable. | `string name = "Alice";` |

**Notes:**
- Keywords are **case-sensitive**.
- Using a keyword as an identifier will result in a **SyntaxError**.

## 3. Grammar (EBNF)

The grammar defines the **structure and syntax rules** of Studium. It is written in EBNF notation and implemented in Lark.

The code block below show cases **Variables Declarations**, **Assignments**, **Print statements**, **Blocks**, **Expressions**, and **Primitive Literals**.

```ebnf
// ---------- Entry ----------
start: stmt+

// ---------- Statements ----------
stmt: decl_stmt
    | assign_stmt
    | print_stmt
    | for_stmt
    | while_stmt
    | if_stmt
    | block
    | expr ";"                      -> expr_stmt

decl_stmt: type_kw NAME ("=" expr)? ";"        -> typed_decl
assign_stmt: NAME "=" expr ";"                 -> assign
print_stmt: "print" "(" expr ")" ";"           -> print_stmt
block: "{" stmt* "}"

// Control flow statements
if_stmt: "if" "(" expr ")" block ("else" block)?        -> if_stmt
while_stmt: "while" "(" expr ")" block                  -> while_stmt

// Use *no-semicolon* forms inside for(...)
for_stmt: "for" "(" for_init? ";" expr? ";" for_update? ")" block -> for_stmt
for_init: decl_nosemi | assign_nosemi | expr
for_update: assign_nosemi | expr

// no-semicolon helpers for for(...)
decl_nosemi: type_kw NAME ("=" expr)?
assign_nosemi: NAME "=" expr

// ---------- Types ----------
type_kw: "int" | "double" | "boolean" | "char" | "string"

// ---------- Expressions (low → high precedence) ----------
?expr: logic_or
?logic_or: logic_and
         | logic_or "||" logic_and -> lor
?logic_and: equality
          | logic_and "&&" equality -> land
?equality: comparison
         | equality "==" comparison -> eq
         | equality "!=" comparison -> ne
?comparison: addsub
           | comparison "<" addsub  -> lt
           | comparison "<=" addsub -> le
           | comparison ">" addsub  -> gt
           | comparison ">=" addsub -> ge
?addsub: muldiv
       | addsub "+" muldiv -> add
       | addsub "-" muldiv -> sub
?muldiv: unary
       | muldiv "*" unary -> mul
       | muldiv "/" unary -> div
       | muldiv "%" unary -> mod
?unary: "!" unary                                  -> not_evaluator
      | "-" unary                                  -> neg_evaluator
      | primary
?primary: primitive
        | NAME                                     -> var
        | "(" expr ")"

// ---------- Primitives ----------
primitive: INT        -> int_lit
         | FLOAT      -> float_lit
         | CHAR       -> char_lit
         | STRING     -> string_lit
         | "true"     -> true_lit
         | "false"    -> false_lit
         | "null"     -> null_lit

// ---------- Tokens ----------
%import common.CNAME -> NAME
%import common.INT
%import common.ESCAPED_STRING -> STRING
CHAR: /'([^'\\]|\\.)'/

// Unsigned float: requires a decimal point (and optional exponent)
// (keeps sign handling in the unary rule)
FLOAT: /\d+\.\d+([eE][+-]?\d+)?/ | /\d+[eE][+-]?\d+/

// ---------- Whitespace & comments ----------
%import common.WS
%ignore WS
%ignore /\/\/[^\n]*/              // line comments starting with //
%ignore /(?s:\/\*.*?\*\/)/         // block comments /* ... */
```

## 4. Example Programs

### 4.1 Variable Binding

```plaintext
int x = 10;
int y = x + 2;
print(y);
```

**Explanation Mode Output:**
```csharp
[Line1] Created variable 'x' with value 5
[Line2] Created variable 'y' with value 7
[Line3] Output: 7
```

### 4.2 Conditional Logic

```plaintext
int x = 10;
if (x > 5) {
    print("Large");
} else {
    print("Small");
}
```

**Explanation Mode Output:**
```csharp
[Line1] Created variable 'x' with value 10
[Line2] Condition 'x > 5' evaluated to True
[Line3] Output: Large
```

### 4.3 Loop Example

```plaintext
int i = 0;
while (i < 3) {
    print(i);
    i = i + 1;
}
```

**Explanation Mode Output:**
```csharp
[Line1] Created variable 'i' with value 0
[Line2] Checking condition 'i < 3' → True
[Line3] Output: 0
[Line4] Updated 'i' to 1
...
```

## 5. Interpreter Architecture

### 5.1 Architecture Overview

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
```

### 5.2 Layer Responsibilities

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

### 5.3 Evaluator Engine
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

#### 5.3.1 Evalutator Engine Methods
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

## 6. Error Handling

| Error Type     | Example                           | Description |
|----------------|----------------------------------|------------|
| SyntaxError      | Invalid syntax according to grammar | Invalid Syntax |
| TypeError      | 'a' - 3                           | Invalid type operation |
| ZeroDivisionError | 5 / 0                          | Division by zero |
| NameError      | print(x) when x undefined        | Variable not found |
| ValueError     | Unsupported operator             | Operator not recognized |

## 7. Flags

| Flags     | Description |
|----------------|----------------------------------|
| ```--explain```      | A line-by-line execution of program. |

## 8. Implementation Details

| Component | Library/Tool | Notes |
| --------- | ------------ | ----- |
| Parser | Lark | The Grammar (of the language) defined by `.lark` file. |
| Evaluator | Python | Recursive AST evaluation. |
| CLI interface | argparse | Supports ```--explain```. |


## 9. Future Enhancements

- Implement full `for` loops with initialization, condition, update, and block execution
- Extend `Evaluator` to support:
    - User-defined functions
    - Nested function scopes
    - Classes and objects
- Integrate line-by-line explanation in real-time for educational mode
- Integrate time complexity evaluator for time complexity performance mode
- Integrate automated test suite regeneration for test regeneration mode.
- Integrate test framework
- Add debugging features: step execution, breakpoints, variable watches

## 10. License & Credits
© 2025 Team Awesome.
This project was developed for UVEC to promote computer science education through interactive language design.

Licensed under the MIT License.  
See [LICENSE](./LICENSE) for details.
