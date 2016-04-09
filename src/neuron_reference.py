class NeuronReference(object):
    def __init__(self):
        self._neurons = {}

    def get_neuron_ids(self):
        return sorted([x for x in self.neurons.iterkeys()])
    
    def get_neuron(self, neuron_id):
        return self._neurons[neuron_id]

    def add_neuron(self, index, neuron):
        self._neurons[index] = neuron

    def get_neurons(self):
        return self._neurons.itervalues()