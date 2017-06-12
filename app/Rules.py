from pyjamas import Window

from app.FormulaBuilder import FormulaBuilder
from lion.Formula import Formula
from lion.Operation import FORALL, operations, Operation
from lion.Theorem import AX_EXT


class Rule:
    def __init__(self, name):
        self.name = name

    def is_applicable(self, formulas):
        pass

    def apply(self, formulas):
        pass


gen = Rule("gen")


def gen_is_applicable(formulas):
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == FORALL


gen.is_applicable = gen_is_applicable


def gen_apply(formulas,after):
    def after1(formula):
        f=formulas[0]
        f = Formula(f.body[2:]).substitute(Formula([f.body[1]]), formula)
        after(f)

    a = FormulaBuilder([op for op in operations if op.available and op.type==Operation.EXPRESSION], after1, type='exp')
    a.show()

gen.apply = gen_apply

print(gen.is_applicable([AX_EXT.formula]))

def psa():
    def saop():
        x=3

ioasj=object
ioasj.saoi="opsajk"
