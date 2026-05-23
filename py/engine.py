import math

class Value:
    def __init__(self, data, parents=(), op='', label='unlabeled', _back=lambda: None):
        self.data = data
        self.parents = list(parents)
        self.op = op
        self.grad = 0
        self._back = _back
        self.label = label

    def __repr__(self):
        return f'Value(data={self.data}, grad={self.grad}, label={self.label})'

    def __neg__(self):
        return -1 * self

    def __rsub__(self, other):
        return other + -self

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        child = Value(self.data + other.data, (self, other), op='+')
        def back():
            self.grad += child.grad
            other.grad += child.grad
        child._back = back
        return child

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        child = Value(self.data * other.data, (self, other), op='*')
        def back():
            self.grad += other.data * child.grad
            other.grad += self.data * child.grad
        child._back = back
        return child

    def __rmul__(self, other):
        return self * other

    def __radd__(self, other):
        return self + other

    def __rtruediv__(self, other):
        return other * (self**-1)

    def __sub__(self, other):
       return self + -other 

    def __pow__(self, power):
        if isinstance(power, Value):
            p = power.data
        else:
            p = power
        child = Value(self.data ** p, (self, ), op='**')
        def back():
            self.grad += (p * (self.data)**(p-1)) * child.grad
        child._back = back
        return child

    def __truediv__(self, other):
        return self * (other**-1)

    def relu(self):
        child = Value(max(0, self.data), parents=(self, ), op='relu', label='relu')
        def back():
            self.grad += (child.data > 0) * child.grad
        child._back = back
        print(f'relu: {child}')
        return child

    def tanh(self):
        n = self.data
        val = (math.exp(2*n) - 1)/(math.exp(2*n) + 1)
        def back():
            self.grad += (1 - val**2) * child.grad
        child = Value(data=val, parents=(self, ), op='tanh', label='tanh()')
        child._back = back
        return child

    def backward(self):
        self.grad = 1
        order = topo_sort(self)
        for n in order:
            n._back()
        
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

