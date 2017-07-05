class Operation:
    QUANTOR = 0
    VARIABLE = 1
    LOGICAL = 2
    RELATION = 3
    EXPRESSION = 4
    PLACEHOLDER = 5

    def __init__(self, id,no_of_args, print_scheme, name, type):
        self.id=id
        self.no_of_args = no_of_args
        self.print_scheme = print_scheme.strip() + ' '
        self.name = name
        self.type = type

    def printout(self, list_of_args):
        return self.print_scheme.format(*list_of_args)


    def to_json(self):
        return {
            "id":self.id,
            "name":self.name,
            "valence":self.no_of_args,
            "type":self.type,
            "print_scheme":self.print_scheme,
        }

    @staticmethod
    def from_dict(dic):
        return Operation(dic["id"], dic["valence"], dic["print_scheme"], dic["name"], dic["type"])

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
                return Operation(chr(i),0, chr(i), chr(i), Operation.VARIABLE)

    @staticmethod
    def get_new_expression(set_of_ops, no_of_args, var=False):
        for i in range(1, 100):
            if "S_" + str(i) not in [op.name for op in set_of_ops]:
                return Operation("S" + str(i),0, "s_" + str(i), "S_" + str(i), Operation.EXPRESSION) if no_of_args == 0 else \
                    Operation("S" + str(i),no_of_args, "S_" + str(i) + " \left( " + ",".join(['{}'] * no_of_args) + "\\right)",
                              "S_" + str(i), Operation.EXPRESSION)


FORALL = Operation(1,2, "\\forall {} : \, {}", "forall", Operation.QUANTOR)
EXISTS = Operation(2,2, "\\exists {} : \, {}", "exists", Operation.QUANTOR)
UNIQUE = Operation(3,2, "\\exists ! {} : \, {}", "unique", Operation.QUANTOR)

IF = Operation(4,2, "\left[ {} \\rightarrow {} \\right]", "if", Operation.LOGICAL)
EQUI = Operation(5,2, "\left[ {} \Leftrightarrow {} \\right]", "equivalent", Operation.LOGICAL)
OR = Operation(6,2, "\left[ {} \\vee {} \\right]", "or", Operation.LOGICAL)
AND = Operation(7,2, "\left[ {} \\wedge {} \\right]", "and", Operation.LOGICAL)
NOT = Operation(8,1, "\\neg {}", "not", Operation.LOGICAL)

IN = Operation(11,2, "{} \in {}", "in", Operation.RELATION)
EQUALS = Operation(9,2, "{} = {}", "equals", Operation.RELATION)
EMPTY = Operation(10,0, "\emptyset", "emptyset", Operation.EXPRESSION)

POK = Operation("pok",2, "\left( {} \otimes {} \\right)", "pok", Operation.EXPRESSION)

A = Operation("var1",0, "a", "a", Operation.VARIABLE)
B = Operation("var2",0, "b", "b", Operation.VARIABLE)
C = Operation("var3",0, "c", "c", Operation.VARIABLE)
D = Operation("var4",0, "d", "d", Operation.VARIABLE)
E = Operation("var5",0, "e", "e", Operation.VARIABLE)
F = Operation("var6",0, "f", "f", Operation.VARIABLE)
G = Operation("var7",0, "g", "g", Operation.VARIABLE)
H = Operation("var8",0, "h", "h", Operation.VARIABLE)

PLACEHOLDER = Operation("place",0, "\Box", "placeholder", Operation.PLACEHOLDER)

builtin_operations = [FORALL, EXISTS, UNIQUE, IF, OR, AND, NOT, EQUI, EQUALS, POK]
global_operations=[EMPTY,IN]
