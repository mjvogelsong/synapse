from neuron_reference import NeuronReference
import random

class Synapses(object):
    def __init__(self, synapse_reference, neuron_reference,
                    strength,
                    max_strength,
                    improve_rate,
                    decrease_rate,
                    decay,
                    saturation):
        self._synapses = set([])
        self._brain_synapses = synapse_reference
        self._neuron_reference = neuron_reference
        self._strength = strength
        self._max_strength = max_strength
        self._improve_rate = improve_rate
        self._decrease_rate = decrease_rate
        self._decay = decay
        self._saturation = saturation

    def add_connection(self, presynaptic_id, postsynaptic_id):
        pair = (presynaptic_id, postsynaptic_id)
        self._synapses.add(pair)
        self._brain_synapses.set_synapse(pair, self.get_synapse(presynaptic_id, postsynaptic_id, random.uniform(0, self._max_strength)))

    def remove_connection(self, presynaptic_id, postsynaptic_id):
        pair = (presynaptic_id, postsynaptic_id)
        if pair in self._synapses:
            self._synapses.remove(pair)
            self._brain_synapses.remove_synapse(pair)

    def adjust_connection(self, presynaptic_id, postsynaptic_id, strength):
        pair = (presynaptic_id, postsynaptic_id)
        self._synapses.add(pair)
        self._brain_synpases.set_synapse(pair, self.get_synapse(presynaptic_id, postsynaptic_id, strength))

    def get_synapse(self, presynaptic_id, postsynaptic_id, strength):
        return Synapse(neuron_reference = self._neuron_reference,
                        presynaptic_id = presynaptic_id,
                        postsynaptic_id = postsynaptic_id,
                        strength = strength,
                        max_strength = self._max_strength,
                        improve_rate = self._improve_rate,
                        decrease_rate = self._decrease_rate,
                        decay = self._decay,
                        saturation = self._saturation)

    def iter_synapses_ids(self):
        return self._synapses

    def iter_synapses_values(self):
        return [self._brain_synapses.get_synapse(pair) for pair in self._synapses]

class Synapse(object):
    def __init__(self, neuron_reference,
                    presynaptic_id,
                    postsynaptic_id,
                    strength,
                    max_strength,
                    improve_rate,
                    decrease_rate,
                    decay,
                    saturation):
        self._neuron_reference = neuron_reference
        self._pre_id = presynaptic_id
        self._post_id = postsynaptic_id
        self._strength = strength
        self._saturation = saturation
        self._max_strength = max_strength
        self._improve_rate = improve_rate
        self._decrease_rate = decrease_rate
        self._decay = decay
        self._signal = 0

    def improve_strength(self):
        self._strength += (self._max_strength - self._strength) * self._improve_rate
        return self._strength

    def decrease_strength(self):
        self._strength *= (1 - self._decrease_rate)
        return self._strength

    def get_strength(self):
        return self._strength

    def get_postsynaptic_id(self):
        return self._post_id

    def get_presynaptic_id(self):
        return self._pre_id

    def get_signal(self):
        if self._signal > self._saturation:
            return self._saturation * self._strength
        elif self._signal < -self._saturation:
            return -self._saturation * self._strength
        else:
            return self._signal * self._strength

    def transmit_signal(self, value):
        self._signal += value
        return self._signal

    def signal_decay(self):
        self._signal *= (1 - self._decay)
        return self._signal

    def adapt(self):
        if self._neuron_reference.get_neuron(self.get_postsynaptic_id()).is_firing():
            self.improve_strength()
            return True
        else:
            self.decrease_strength()
            return False
