from Formula import Formula
from Operation import FORALL, AND, B, NOT, OR, A

f = Formula([FORALL, AND, B, NOT, B, B])
print(f.dump())
f = f.substitute_definition(Formula([AND, A, B]), Formula([NOT, OR, NOT, A, NOT, B]))
# print(f.to_cnf().to_latex())
print(f.dump())

