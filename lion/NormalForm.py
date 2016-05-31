class NormalForm:
    def __init__(self, body):
        self.body = [[formula.deepcopy() for formula in tag] for tag in body]
        self.simplify()

    def deepcopy(self):
        return NormalForm(self.body)

    def printout(self):
        return '\n'.join(['\t'.join([str(x) for x in y]) for y in self.body])

    def is_empty(self):
        return len(self.body) == 0

    def is_degenerate(self):
        for x in range(len(self.body)):
            for y in range(x + 1, len(self.body)):
                if len(self.body[x]) == 1 and len(self.body[y]) == 1 and self.body[x][0].is_negation_of(
                        self.body[y][0]):
                    return True
        return False

    def remove_duplicates(self):
        for t in self.body:
            for x in range(len(t)):
                for y in range(x + 1, len(t)):
                    if t[x] == t[y]:
                        del t[y]
                        return True
        return False

    def remove_supersets(self):
        for x in range(len(self.body)):
            for y in range(x + 1, len(self.body)):
                if set(self.body[y]) > set(self.body[x]):
                    del self.body[y]
                    return True
                if set(self.body[x]) > set(self.body[y]):
                    del self.body[x]
                    return True
        return False

    def remove_degenerates(self):
        for t in self.body:
            for x in range(len(t)):
                for y in range(x + 1, len(t)):
                    if t[x].is_negation_of(t[y]):
                        self.body.remove(t)
                        return True
        return False

    def remove_negations_of_singletons(self):
        for t_sing in [tag for tag in self.body if len(tag) == 1]:
            for t in [tag for tag in self.body if len(tag) > 1]:
                for x in t:
                    if t_sing[0].is_negation_of(x):
                        t.remove(x)
                        return True
        return False

    def simplify(self):
        for s in [self.remove_duplicates, self.remove_supersets, self.remove_degenerates,
                  self.remove_negations_of_singletons]:
            while s():
                pass

    def get_vars(self):
        vars = []
        for tag in self.body:
            for formula in tag:
                for var in formula.get_vars():
                    if var not in vars:
                        vars.append(var)
        return vars

    def substitute(self, source, dest):
        res = NormalForm(self.body)
        for tag in res.body:
            for n in range(len(tag)):
                tag[n] = tag[n].substitute(source, dest)
        return res

    def to_latex(self):
        return "\\begin{cases} " + " \\\\ ".join([" \qquad ".join([formula.to_latex() for formula in tag]) for tag in
                                                  self.body]) + " \end{cases}"
