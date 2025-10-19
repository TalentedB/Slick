# The Environment class is responsible for managing the state of the program,
# specifically the bindings of variables to their values.

class Environment():
    def __init__(self, parent=None):
        """
        Initialize a new environment.
        
        Args:
            parent: Reference to the parent (enclosing) scope for nested scopes.
                    None for the global scope.
        """
        self.vars = {}  # Dictionary to store variable name -> value mappings
        self.parent = parent  # Parent environment for scope chaining

    def define(self, name, value):
        """
        Define a new variable in the current scope.
        This creates a new binding in this environment, even if the variable
        exists in a parent scope (variable shadowing).
        
        Args:
            name: The variable name (string)
            value: The value to bind to the variable
        """
        self.vars[name] = value

    def get(self, name):
        """
        Retrieve the value of a variable by name.
        Searches the current scope first, then parent scopes recursively.
        
        Args:
            name: The variable name to look up
            
        Returns:
            The value bound to the variable
            
        Raises:
            NameError: If the variable is not found in any scope
        """
        if name in self.vars:
            return self.vars[name]  # Found in current scope
        elif self.parent:
            return self.parent.get(name)  # Search parent scope
        else:
            raise NameError(f"Variable '{name}' is not defined.")
        

    def set(self, name, value):
        """
        Update an existing variable's value.
        Searches current scope first, then parent scopes recursively.
        Unlike define(), this will NOT create a new variable.
        
        Args:
            name: The variable name to update
            value: The new value to assign
            
        Raises:
            NameError: If the variable doesn't exist in any scope
        """
        if name in self.vars:
            self.vars[name] = value  # Update in current scope
        elif self.parent:
            self.parent.set(name, value)  # Update in parent scope
        else:
            raise NameError(f"Variable '{name}' is not defined.")
        
        #commented using claude sonnet 4.5