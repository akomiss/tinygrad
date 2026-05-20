class Value:
    def __init__(self, data, parents=(), op='', label='unlabeled'):
        self.data = data
        self.parents = set(parents)
        self.op = op
        self.grad = 0
        self.label = label

    def __repr__(self):
        return f'Value(data={self.data}, grad={self.grad}, label={self.label})'

    def __add__(self, other):
        child = Value(self.data + other.data, (self, other), op='+')
        return child

    def __mul__(self, other):
        child = Value(self.data * other.data, (self, other), op='*')
        return child

    def __div__(self, other):
        child = Value(self.data / other.data, (self, other), op='/')
        return child

    def backwards(self):
        self.grad = 1
        order = topo_sort(self)
        print(order)
        for n in order:
            if len(n.parents) == 0:
                continue
            p1,p2 = list(n.parents)[0], list(n.parents)[1]
            if n.op == '+':
                p1.grad += n.grad
                p2.grad += n.grad
            elif n.op == '*':
                p1.grad += p2.data * n.grad
                p2.grad += p1.data * n.grad
            else:
                raise RuntimeError('unknown operand', n.op)

            print('backwards', n, p1, p2)
        
def topo_sort(root):
    def inner(node, stk, seen):
        if node in seen:
           return 
        seen.add(node)
        for p in node.parents:
            inner(p, stk, seen)
        stk.append(node)
    order = []
    seen = set()
    inner(root, order, seen)
    return order[::-1]




