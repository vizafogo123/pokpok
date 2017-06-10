from Formula import Formula
from Operation import FORALL, AND, B, NOT, OR, A, EQUI, C, IN,EQUALS

f = Formula([FORALL, AND, B, NOT, B, B])
print(f.dump())
f = f.substitute_definition(Formula([AND, A, B]), Formula([NOT, OR, NOT, A, NOT, B]))
print(f.dump())

f = Formula([EQUI, EQUI, A, B, C])
print(f.dump())
f = f.simplify()
print(f.to_latex())

f = Formula([AND, FORALL, A, IN, A, A, FORALL, A, IN, A, A])
print(f.dump())
f.rename_one_quantor()
print(f.dump())

f = Formula([FORALL, B,EQUALS,B,B])
print(f.dump())
f=f.substitute(Formula([f.body[1]]),Formula([C]))
print(f.dump())

a=[1,2,3]
print([i for i, e in enumerate(a) if e != 0])
