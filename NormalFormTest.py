from NormalForm import NormalForm


class pok:
    def __init__(self, c):
        self.c = c

    def __eq__(self, other):
        return self.c == other.c

    def __hash__(self):
        return hash(self.c)

    def __str__(self):
        return self.c

    def is_negation_of(self, other):
        return self.c == '-' + other.c or other.c == '-' + self.c

    def to_latex(self):
        return self.c


a = NormalForm(
        [[pok('A'), pok('B'), pok('A'), pok('A')], [pok('C'), pok('C'), pok('A'), pok('B'), pok('A')], [pok('X')],
         [pok('-Z'), pok('Q'), pok('Z')], [pok('B'), pok('-X'), pok('H')]])

b = NormalForm([])
c = NormalForm([[pok('C')], [pok('X'), pok('Y')], [pok('A')], [pok('-A')]])

a.simplify()

print(a.printout())
print(a.is_empty(), b.is_empty())
print(a.is_degenerate(), c.is_degenerate())

print(a.to_latex())
