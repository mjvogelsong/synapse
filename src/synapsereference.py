class SynapseReference(object):
    def __init__(self):
        self._synapses = {}
        self._positive_adapts = 0
        self._negative_adapts = 0

    def get_synapse(self, neuron_pair):
        return self._synapses[neuron_pair]

    def get_synapses(self):
        return self._synapses.itervalues()

    def set_synapse(self, neuron_pair, synapse):
        self._synapses[neuron_pair] = synapse

    def remove_synapse(self, neuron_pair):
        self._synapses.remove(neuron_pair)

    def add_positive_adapt(self):
    	self._positive_adapts += 1
    	return self._positive_adapts

    def add_negative_adapt(self):
    	self._negative_adapts += 1
    	return self._negative_adapts

    def get_positive_adapts(self):
    	return self._positive_adapts

    def get_negative_adapts(self):
    	return self._negative_adapts
