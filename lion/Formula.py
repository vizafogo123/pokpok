from lion.Operation import PLACEHOLDER, AND, OR, NOT, IF, FORALL, EXISTS, Operation, EQUI, EQUALS, UNIQUE


class Formula:
    def __init__(self, body):
        self.body = list(body)

    def __eq__(self, other):
        return self.body == other.body

    def __hash__(self):
        return hash(tuple(self.body))

    def deepcopy(self):
        return Formula(self.body)

    def list_of_ops(self):
        res = []
        for op in self.body:
            if op not in res:
                res.append(op)
        return res

    def is_negation_of(self, other):
        return ([NOT] + self.body if self.body[0] != NOT else self.body[1:]) == other.body

    def negation(self):
        return Formula([NOT] + self.body) if self.body[0] != NOT else Formula(self.body[1:])

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

    def get_vars(self):
        vars = []
        for op in self.body:
            if op.type == Operation.VARIABLE and op not in vars:
                vars.append(op)
        return vars

    def parent(self, child):
        k = child - 1
        n = self.body[k].no_of_args - 1
        while n < 0:
            k -= 1
            n += self.body[k].no_of_args - 1
        return k

    def add_one_op(self, op, type='rel'):
        if len(self.body) == 0:
            parent = (NOT if type == 'rel' else EQUALS)
            no_of_child = 1
        else:
            parent, no_of_child = self.parent_and_no_of_child(len(self.body))
            parent = self.body[parent]
        if Operation.can_follow(parent, op, no_of_child):
            if op.type == Operation.VARIABLE:
                if parent.type == Operation.QUANTOR and no_of_child == 1:
                    for i in range(len(self.body)):
                        if self.body[i] == op:
                            return
                else:
                    p, x = self.parent_and_no_of_child(len(self.body))
                    while p >= 0:
                        if self.body[p].type == Operation.QUANTOR and self.body[p + 1] == op:
                            self.body += [op]
                            return
                        p, x = self.parent_and_no_of_child(p)
                    if p < 0:
                        return
            self.body += [op]

    def parent_and_no_of_child(self, k):
        if k == 0:
            return -1, 1
        k -= 1
        n = self.body[k].no_of_args - 1
        while n < 0:
            k -= 1
            n += self.body[k].no_of_args - 1
        return k, self.body[k].no_of_args - n

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

    def substitute_equivalence(self, n):
        if self.body[n] == EQUI:
            self.body = self.body[:n] + [AND, IF] + self.body[n + 1:self.start_of_child(n, 3)] \
                        + [IF] + self.body[self.start_of_child(n, 2):self.start_of_child(n, 3)] \
                        + self.body[n + 1:self.start_of_child(n, 2)] + self.body[self.start_of_child(n, 3):]

    def substitute_unique(self, n):
        new_var = Operation.get_new_variable([op for op in self.body if op.type == Operation.VARIABLE])
        if self.body[n] == UNIQUE:
            self.body = self.body[:n] + [EXISTS, self.body[n + 1], AND] + self.body[n + 2:self.start_of_child(n, 3)] + \
                        [FORALL, new_var, IF] + Formula(self.body[n + 2:self.start_of_child(n, 3)]).substitute(
                Formula([self.body[n + 1]]),
                Formula([new_var])).body \
                        + [EQUALS, new_var, self.body[n + 1]] + self.body[self.start_of_child(n, 3):]

    def substitute_ifs(self):
        self.body = self.substitute(Formula([IF]), Formula([OR, NOT])).body

    def remove_duplicate_negations(self):
        for n in range(len(self.body) - 1):
            if n < len(self.body) - 1 and self.body[n] == NOT and self.body[n + 1] == NOT:
                del self.body[n]
                del self.body[n]

    def rename_one_quantor(self):
        for k in range(len(self.body)):
            if self.body[k].type == Operation.QUANTOR:
                for n in range(k + 2, len(self.body)):
                    if self.body[n].type == Operation.QUANTOR and self.body[k + 1] == self.body[n + 1]:
                        new_var = Operation.get_new_variable([op for op in self.body if op.type == Operation.VARIABLE])
                        s = Formula(self.body[n:self.start_of_child(n, 3)]).substitute(Formula([self.body[n + 1]]),
                                                                                       Formula([new_var]))
                        self.body = self.body[:n] + s.body + self.body[self.start_of_child(n, 3):]
                        return True
        return False

    def move_one_negation_down(self):
        for n in range(len(self.body)):
            if self.body[n] == NOT and self.body[n + 1] == OR:
                self.body.insert(self.start_of_child(n + 1, 2), NOT)
                self.body[n] = AND
                self.body[n + 1] = NOT
                return True
            if self.body[n] == NOT and self.body[n + 1] == AND:
                self.body.insert(self.start_of_child(n + 1, 2), NOT)
                del self.body[n + 1]
                self.body[n] = IF
                return True
            if self.body[n] == NOT and self.body[n + 1] == IF:
                self.body.insert(self.start_of_child(n + 1, 2), NOT)
                del self.body[n + 1]
                self.body[n] = AND
                return True
            if self.body[n] == NOT and self.body[n + 1] in [FORALL, EXISTS]:
                self.body[n] = (FORALL if self.body[n + 1] == EXISTS else EXISTS)
                self.body[n + 1] = self.body[n + 2]
                self.body[n + 2] = NOT
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

    def remove_one_forall(self):
        for k in range(len(self.body)):
            if self.body[k] == FORALL:
                del self.body[k]
                del self.body[k]
                return True
        return False

    def simplify(self):
        if len(self.body) == 0:
            return self
        res = Formula(self.body)
        res.remove_duplicate_negations()
        if res.body[0] == NOT and res.body[1] == EQUI:
            res.substitute_equivalence(1)
        if res.body[0] == UNIQUE or (res.body[0] == NOT and res.body[1] == UNIQUE):
            res.substitute_unique(0 if res.body[0] == UNIQUE else 1)
        for s in [res.rename_one_quantor, res.move_one_negation_down]:
            while s():
                res.remove_duplicate_negations()
        return res

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

    def to_json(self):
        return [op.id for op in self.body]

    @staticmethod
    def from_list(lis, ops):
        def find_op_by_id(id):
            for op in ops:
                if op.id == id:
                    return op

        return Formula([find_op_by_id(id) for id in lis])

    def is_in_unique_form(self):
        if len(self.body) == 0:
            return False
        i = 0
        while True:
            if self.body[i] == UNIQUE:
                return True
            if self.body[i] == FORALL:
                i += 2
            else:
                return False

    def get_def_theorem(self, op):
        i = 0
        k=[]
        while self.body[i] != UNIQUE:
            i += 2
            k.append(self.body[i-1])

        return Formula(self.body[:i] + Formula(self.body[i + 2:]).substitute(Formula([self.body[i + 1]]),
                                                                             Formula([op] + k)).body)

    def get_no_of_args_for_unique_form(self):
        i = 0
        while self.body[2 * i] != UNIQUE:
            i += 1
        return i


if __name__ == '__main__':
    A = Operation("var1", 0, "a", "a", Operation.VARIABLE)
    B = Operation("var2", 0, "b", "b", Operation.VARIABLE)
    C = Operation("var3", 0, "c", "c", Operation.VARIABLE)
    OAS = Operation("var3", 2, "oas", "oas", Operation.EXPRESSION)
    pok = Operation("erg", 1, "pok", "pok", Operation.EXPRESSION)
    f = Formula([FORALL, A, UNIQUE, C, EQUALS, A, C])
    print(f.get_def_theorem(pok).dump(),Operation.get_new_id())
    Operation.get_new_id()