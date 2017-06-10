class Operation:
    QUANTOR = 0
    VARIABLE = 1
    LOGICAL = 2
    RELATION = 3
    EXPRESSION = 4
    PLACEHOLDER = 5

    def __init__(self, no_of_args, print_scheme, name, type, available=True, is_function_scheme=False):
        self.no_of_args = no_of_args
        self.print_scheme = print_scheme.strip() + ' '
        self.name = name
        self.available = available
        self.type = type
        self.is_function_scheme=is_function_scheme

    def printout(self, list_of_args):
        return self.print_scheme.format(*list_of_args)

    @staticmethod
    def can_follow(parent, child, no_of_child):
        print(parent.name, child.name, no_of_child)
        print(parent.type, child.type)
        return (parent.type == Operation.QUANTOR and child.type == Operation.VARIABLE and no_of_child == 1) or \
               (parent.type == Operation.QUANTOR and child.type in [Operation.LOGICAL, Operation.RELATION,
                                                                    Operation.QUANTOR] and no_of_child == 2) or \
               (parent.type == Operation.LOGICAL and child.type in [Operation.LOGICAL, Operation.RELATION,
                                                                    Operation.QUANTOR]) or \
               (parent.type == Operation.RELATION and child.type in [Operation.EXPRESSION, Operation.VARIABLE]) or \
               (parent.type == Operation.EXPRESSION and child.type in [Operation.EXPRESSION, Operation.VARIABLE])

    @staticmethod
    def get_new_variable(set_of_vars):
        for i in range(ord('a'), ord('z') + 1):
            if chr(i) not in [var.name for var in set_of_vars]:
                return Operation(0, chr(i), chr(i), Operation.VARIABLE)

    @staticmethod
    def get_new_expression(set_of_ops, no_of_args,var=False):
        if var:
             return Operation(0, var.name.upper(), var.name.upper(), Operation.EXPRESSION) if no_of_args == 0 else \
                    Operation(no_of_args, var.name.upper() + " \left( " + ",".join(['{}'] * no_of_args) + "\\right)",
                              var.name.upper(), Operation.EXPRESSION)

        for i in range(1, 100):
            if "S_" + str(i) not in [op.name for op in set_of_ops]:
                return Operation(0, "s_" + str(i), "S_" + str(i), Operation.EXPRESSION) if no_of_args == 0 else \
                    Operation(no_of_args, "S_" + str(i) + " \left( " + ",".join(['{}'] * no_of_args) + "\\right)",
                              "S_" + str(i), Operation.EXPRESSION)


FORALL = Operation(2, "\\forall {} : \, {}", "forall", Operation.QUANTOR)
EXISTS = Operation(2, "\\exists {} : \, {}", "exists", Operation.QUANTOR)

IF = Operation(2, "\left[ {} \\rightarrow {} \\right]", "if", Operation.LOGICAL)
EQUI = Operation(2, "\left[ {} \Leftrightarrow {} \\right]", "equivalent", Operation.LOGICAL)
OR = Operation(2, "\left[ {} \\vee {} \\right]", "or", Operation.LOGICAL)
AND = Operation(2, "\left[ {} \\wedge {} \\right]", "and", Operation.LOGICAL)
NOT = Operation(1, "\\neg {}", "not", Operation.LOGICAL)

IN = Operation(2, "{} \in {}", "in", Operation.RELATION)
EQUALS = Operation(2, "{} = {}", "equals", Operation.RELATION)
EMPTY = Operation(0, "\emptyset", "emptyset", Operation.EXPRESSION)

POK = Operation(2, "\left( {} \otimes {} \\right)", "pok", Operation.EXPRESSION)

A = Operation(0, "a", "a", Operation.VARIABLE)
B = Operation(0, "b", "b", Operation.VARIABLE)
C = Operation(0, "c", "c", Operation.VARIABLE)
D = Operation(0, "d", "d", Operation.VARIABLE)
E = Operation(0, "e", "e", Operation.VARIABLE)
F = Operation(0, "f", "f", Operation.VARIABLE)
G = Operation(0, "g", "g", Operation.VARIABLE)
H = Operation(0, "h", "h", Operation.VARIABLE)

PHI1=Operation(1, "\phi \left( {} \\right)", "phi1", Operation.RELATION,available=False,is_function_scheme=True)
PHI2=Operation(2, "\phi \left( {} , {} \\right)", "phi2", Operation.RELATION,available=False,is_function_scheme=True)

PLACEHOLDER = Operation(0, "\Box", "placeholder", Operation.PLACEHOLDER, available=False)

operations = [FORALL, EXISTS, IF, OR, AND, NOT, EQUI, IN, EMPTY, EQUALS, A, B, C, D, E, PLACEHOLDER,POK]
