from pyjamas import Window

from app.FormulaBuilder import FormulaBuilder
from lion.Formula import Formula
from lion.Operation import FORALL, operations, Operation, EXISTS
from lion.Theorem import AX_EXT


def request_formula(operations, after, type):
    FormulaBuilder(operations, after, type).show()


class Rule:
    def __init__(self, name):
        self.name = name

    def is_applicable(self, formulas):
        pass

    def apply(self, formulas, after):
        pass


gen = Rule("gen")


def gen_is_applicable(formulas):
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == FORALL


def gen_apply(formulas, after):
    def after1(formula):
        f = formulas[0]
        f = Formula(f.body[2:]).substitute(Formula([f.body[1]]), formula)
        after(f, soap="oijo")

    request_formula([op for op in operations if op.available and op.type == Operation.EXPRESSION], after1, type='exp')


gen.is_applicable = gen_is_applicable
gen.apply = gen_apply

exist = Rule("exist")


def exist_is_applicable(formulas):
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == EXISTS


def exist_apply(formulas, after):
    const = Operation.get_new_expression(operations, 0)
    operations.append(const)
    f = formulas[0]
    f = Formula(f.body[2:]).substitute(Formula([f.body[1]]), Formula([const]))
    after(f)


exist.is_applicable = exist_is_applicable
exist.apply = exist_apply

Rules = [gen, exist]

print(gen.is_applicable([AX_EXT.formula]))
