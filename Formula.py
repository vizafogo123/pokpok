from NormalForm import NormalForm
from Operation import PLACEHOLDER, AND, OR, NOT, A, B, IF, FORALL, EXISTS, C, D, Operation, IN, EQUI


class Formula:
    def __init__(self, body):
        self.body = body

    def __eq__(self, other):
        return self.body == other.body

    def is_negation_of(self, other):
        return ([NOT] + self.body if self.body[0] != NOT else self.body[1:]) == other.body

    def add_one_op(self, op):
        if len(self.body) == 0:
            parent = NOT
            no_of_child = 1
        else:
            k = len(self.body) - 1
            n = self.body[-1].no_of_args - 1
            while n < 0:
                k -= 1
                n += self.body[k].no_of_args - 1
            parent = self.body[k]
            no_of_child = parent.no_of_args - n
        if Operation.can_follow(parent, op, no_of_child):
            self.body += [op]

    def start_of_child(self, n, k):
        i = n
        depth = -1
        ch_n = 0
        while True:
            if depth == -1:
                ch_n += 1
                depth = 0
            if ch_n == k:
                return i + 1
            i += 1
            depth += self.body[i].no_of_args - 1

    def to_latex(self):
        p = [''] * len(self.body)
        i = len(self.body) - 1
        while i >= 0:
            p[i] = self.body[i].printout([p[self.start_of_child(i, k)] for k in range(1, self.body[i].no_of_args + 1)])
            i -= 1
        return p[0]

    def dump(self):
        return ' '.join([op.name for op in self.body])

    def fill_with_placeholders(self):
        no_of_placeholders = 1 + sum([op.no_of_args - 1 for op in self.body])
        return Formula(self.body + [PLACEHOLDER] * no_of_placeholders)

    def is_closed(self):
        return sum([x.no_of_args - 1 for x in self.body]) == -1

    def substitute_ifs(self):
        self.body = self.substitute(Formula([IF]), Formula([OR, NOT])).body

    def substitute_equivalences(self):
        n=0
        while n<len(self.body):
            if self.body[n]==EQUI:
                self.body=self.body[:n]+[AND,IF]+self.body[n+1:self.start_of_child(n,3)]\
                          +[IF]+self.body[self.start_of_child(n,2):self.start_of_child(n,3)]\
                          +self.body[n+1:self.start_of_child(n,2)]+self.body[self.start_of_child(n,3):]
            n+=1

    def remove_duplicate_negations(self):
        for n in range(len(self.body) - 1):
            if n < len(self.body) - 1 and self.body[n] == NOT and self.body[n + 1] == NOT:
                del self.body[n]
                del self.body[n]

    def move_one_negation_down(self):
        for n in range(len(self.body)):
            if self.body[n] == NOT and self.body[n + 1] in [AND, OR]:
                self.body.insert(self.start_of_child(n + 1, 2), NOT)
                self.body[n] = (AND if self.body[n + 1] == OR else OR)
                self.body[n + 1] = NOT
                return True
        return False

    def move_one_quantor_up(self):
        for n in range(len(self.body)):
            if self.body[n] == NOT and self.body[n + 1] in [FORALL, EXISTS]:
                self.body[n] = (FORALL if self.body[n + 1] == EXISTS else EXISTS)
                self.body[n + 1] = self.body[n + 2]
                self.body[n + 2] = NOT
                return True
            if self.body[n] in [AND, OR] and self.body[n + 1] in [FORALL, EXISTS]:
                tmp = self.body[n]
                self.body[n] = self.body[n + 1]
                self.body[n + 1] = self.body[n + 2]
                self.body[n + 2] = tmp
                return True
            if self.body[n] in [AND, OR] and self.body[self.start_of_child(n, 2)] in [FORALL, EXISTS]:
                k = self.start_of_child(n, 2)
                self.body.insert(n, self.body[k])
                self.body.insert(n + 1, self.body[k + 2])
                del self.body[k + 3]
                del self.body[k + 2]
                return True
        return False

    def move_one_and_up(self):
        for n in range(len(self.body)):
            if self.body[n] == OR and self.body[n + 1] == AND:
                self.body[n] = AND
                self.body[n + 1] = OR
                self.body = self.body[:self.start_of_child(n + 1, 2)] + \
                            self.body[self.start_of_child(n, 2):self.start_of_child(n, 3)] + \
                            [OR] + self.body[self.start_of_child(n + 1, 2):]
                return True
            if self.body[n] == OR and self.body[self.start_of_child(n, 2)] == AND:
                self.body[n] = AND
                del self.body[self.start_of_child(n, 2)]
                self.body.insert(n + 1, OR)
                self.body = self.body[:self.start_of_child(n, 2)] + \
                            [OR] + self.body[n + 2:self.start_of_child(n + 1, 2)] + \
                            self.body[self.start_of_child(n, 2):]
                return True
        return False

    def simplify(self):
        res = Formula(self.body)
        res.substitute_equivalences()
        res.substitute_ifs()
        res.remove_duplicate_negations()
        for s in [res.move_one_quantor_up, res.move_one_negation_down, res.move_one_and_up]:
            while s():
                res.remove_duplicate_negations()
        return res

    def to_cnf(self):
        tags = []
        k = 0
        while self.body[k] in [FORALL, EXISTS]:
            k = self.start_of_child(k, 2)

        if self.body[k] != AND:
            tags = [Formula(self.body[k:])]
        else:
            for n in range(k, len(self.body)):
                if self.body[n] == AND and self.body[n + 1] != AND:
                    tags.append(Formula(self.body[n + 1:self.start_of_child(n, 2)]))
                if self.body[n] == AND and self.body[self.start_of_child(n, 2)] != AND:
                    tags.append(Formula(self.body[self.start_of_child(n, 2):self.start_of_child(n, 3)]))

        res = []
        for t in tags:
            if t.body[0] != OR:
                r = [t]
            else:
                r = []
                for n in range(len(t.body)):
                    if t.body[n] == OR and t.body[n + 1] != OR:
                        r.append(Formula(t.body[n + 1:t.start_of_child(n, 2)]))
                    if t.body[n] == OR and t.body[t.start_of_child(n, 2)] != OR:
                        r.append(Formula(t.body[t.start_of_child(n, 2):t.start_of_child(n, 3)]))
            res.append(r)

        return NormalForm(res)

    def substitute(self, source, dest):
        return self.substitute_parallel([source], [dest])

    def substitute_parallel(self, source_list, dest_list):
        k = 0
        res = Formula(self.body)
        while k < len(res.body):
            b = True
            for n in range(len(source_list)):
                if b and res.body[k:k + len(source_list[n].body)] == source_list[n].body:
                    res.body = res.body[:k] + dest_list[n].body + res.body[k + len(source_list[n].body):]
                    k += len(dest_list[n].body)
                    b = False
            if b:
                k += 1
        return res

    def substitute_definition(self, function, definition):
        res = Formula(self.body)
        k = len(res.body) - 1
        while k >= 0:
            if res.body[k] == function.body[0]:
                d = Formula(definition.body)
                d = d.substitute_parallel([Formula([function.body[v]]) for v in range(1, res.body[k].no_of_args + 1)],
                                          [Formula(res.body[res.start_of_child(k, v):res.start_of_child(k, v + 1)]) for
                                           v in range(1, res.body[k].no_of_args + 1)])
                res.body = res.body[:k] + d.body + res.body[res.start_of_child(k, res.body[k].no_of_args + 1):]
            k -= 1
        return res


if __name__ == '__main__':
    f = Formula([EQUI, EQUI, A,B,C])
    print(f.dump())
    f=f.simplify()
    # print(f.to_cnf().to_latex())
    print(f.to_latex())
