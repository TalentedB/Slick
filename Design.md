# Design of Studium

*Studium* was designed with the purpose in mind to help students understand the **core programming fundamentals** that underlie modern programming languages.

Its design emphasizes clarity, familiarity, and expalinability, making it a teaching oriented language.

## Design Philosophy
The guiding principle behind *Studium* is educational transparency where every exectued statement should not only produce a result, also **explain what is happening under the hood**.

This makes it suitable for students who are learning programming concepts such as variables, conditionals, loops, and functions for the first time.

Key Goals:
- Provide a familiar syntax to reduce the learning curve.
- Offer line-by-line explanations to reinforce conceptual understanding.

## Design Decisions

### Choice of Implementation Language — Python
The interpreter is built in Python. This is because Python has less overhead when writing code which allows the team to focus on the logic of studium. Additionally all team members are familiar with Python.

However, Python is slower than compiled languages like C. Though was not a primary concern since Studium's intention is as an educations tool.

### Parsing Framework — Lark
Instead of creating a parser ourselves (for tokenizing our language), we are using Lark. Lark is a parsing library for grammar definition and parsing. It supports EBNF grammar definitions, automatically handles lexing and parsing, integrates easily with Python and generates abstract syntax trees (ASTs).

However, this abstraction of using Lark reduces flexibility to customize token-level error messages and additionally just adds a layer of depenency on the framework.

### Syntax Design 
The syntax of *Studium* is meant to reflect Java, a programming language that is taught across universities. It will introduce structured programming concetps (e.g., explicit types) that help students understand control flow and data types.

However, this does create boilerplate (e.g., declaring variable types) which can slow implementation. Though this isn't much of a concern as the language is intended to reinforce strong typing concepts.

