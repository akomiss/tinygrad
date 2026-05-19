class Value:
    def __init__(self, data, parents=(), op=''):
        self.data = data
        self.parents = set(parents)
        self.op = op

    def __repr__(self):
        return f'Value(data={self.data})'

    def __add__(self, other):
        child = Value(self.data + other.data, (self, other), op='+')
        return child

    def __mul__(self, other):
        child = Value(self.data * other.data, (self, other), op='*')
        return child

    def __div__(self, other):
        child = Value(self.data / other.data, (self, other), op='/')
        return child
