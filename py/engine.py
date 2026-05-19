class Value:
    def __init__(self, data, parents=()):
        self.data = data
        self.parents = set(parents)

    def __repr__(self):
        return f'Value(data={self.data})'

    def __add__(self, other):
        child = Value(self.data + other.data, (self, other))
        return child

    def __mul__(self, other):
        child = Value(self.data * other.data, (self, other))
        return child

    def __div__(self, other):
        child = Value(self.data / other.data, (self, other))
        return child
