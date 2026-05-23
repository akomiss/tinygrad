from engine import *
import random

class Neuron:
    def __init__(self, num_inputs):
        self.weights = [
            Value(random.uniform(-1,1)) for _ in range(num_inputs)
        ]
        self.bias = Value(random.uniform(-1,1))

    def descend(self, step_size):
        for weight in self.weights:
            weight.data -= step_size * weight.grad
            weight.grad = 0
        self.bias.data -= step_size * self.bias.grad
        self.bias.grad = 0

    def __call__(self, inputs):
        assert len(inputs) == len(self.weights)
        val = sum(wi*xi for (wi,xi) in zip(self.weights, inputs)) + self.bias
        # tanh, not relu, because I am a noob and don't know how to init anything
        return val.tanh() 

class Layer:
    def __init__(self, num_inputs, num_neurons):
        self.neurons = [
            Neuron(num_inputs) for _ in range(num_neurons)
        ]
    
    def __call__(self, inputs):
        return [
            n(inputs) for n in self.neurons
        ]
    
    def descend(self, step_size):
        for n in self.neurons:
            n.descend(step_size)

# 
class MLP:
    def __init__(self, num_inputs, layer_sizes):
        layers = [
            Layer(num_inputs=num_inputs if ix == 0 else layer_sizes[ix-1],
                  num_neurons=layer_sizes[ix]
            )
            for ix in range(len(layer_sizes))
        ]
        self.layers = layers
        self.num_inputs = num_inputs
        
    def __call__(self, inputs):
        assert len(inputs) == self.num_inputs
        prev_outputs = inputs
        for ix, layer in enumerate(self.layers):
            prev_outputs = layer(prev_outputs)
        assert len(prev_outputs) == 1
        return prev_outputs[0]

    def descend(self, step_size):
        for layer in self.layers:
            layer.descend(step_size)

