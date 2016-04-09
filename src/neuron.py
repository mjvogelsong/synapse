import random
from synapse import Synapses

class Neurons(object):
    def __init__(self, neuron_reference, synapse_reference,
                    number_neurons,
                    lower_bound,
                    upper_bound,
                    signal,
                    fire_threshold,
                    max_response,
                    min_response,
                    amplification,
                    signal_decay,
                    response_decay,
                    synapse_strength,
                    synapse_max_strength,
                    synapse_improve_rate,
                    synapse_decrease_rate,
                    synapse_decay,
                    synapse_saturation):
        self._firings = 0
        self._neuron_reference = neuron_reference
        self._synapse_reference = synapse_reference
        self._number_synapses = 0
        self._number_neurons = number_neurons
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        for index in range(self._number_neurons):
            self._neuron_reference.add_neuron(index, Neuron(    neuron_reference=neuron_reference,
                                                                synapse_reference=synapse_reference, 
                                                                neuron_id=index,
                                                                signal=random.uniform(lower_bound, upper_bound),
                                                                fire_threshold=fire_threshold,
                                                                max_response=max_response,
                                                                min_response=min_response,
                                                                amplification=amplification,
                                                                signal_decay=signal_decay,
                                                                response_decay=response_decay,
                                                                synapse_strength = synapse_strength,
                                                                synapse_max_strength = synapse_max_strength,
                                                                synapse_improve_rate = synapse_improve_rate,
                                                                synapse_decrease_rate = synapse_decrease_rate,
                                                                synapse_decay = synapse_decay,
                                                                synapse_saturation = synapse_saturation))
    def get_firings(self):
        return self._firings

    def get_positive_adapts(self):
        return self._synapse_reference.get_positive_adapts()

    def get_negative_adapts(self):
        return self._synapse_reference.get_negative_adapts()

    def adapt(self):
        for neuron in self._neuron_reference.get_neurons():
            neuron.adapt()
    
    def add_random_synapses(self, number):
        self._number_synapses = number
        for number in range(self._number_synapses):
            self.add_random_synapse()

    def release_neurotransmitters(self):
        for neuron in self._neuron_reference.get_neurons():
            self._firings += neuron.release_neurotransmitters()

    def integrate_signals(self):
        for neuron in self._neuron_reference.get_neurons():
            neuron.process_dendrites()
    
    def decay(self):
        for neuron in self._neuron_reference.get_neurons():
            neuron.decay()
        for synapse in self._synapse_reference.get_synapses():
            synapse.signal_decay()

    def process(self):
        self.release_neurotransmitters()
        self.integrate_signals()
        self.adapt()
        self.decay()

    def add_random_synapse(self):
        presynaptic = self._neuron_reference.get_neuron(random.randint(0, self._number_neurons-1))
        postsynaptic = self._neuron_reference.get_neuron(random.randint(0, self._number_neurons-1))
        self.add_synapse(presynaptic, postsynaptic)

    def add_synapse(self, presynaptic, postsynaptic):
        presynaptic.add_outgoing_connection(postsynaptic.get_id())
        postsynaptic.add_incoming_connection(presynaptic.get_id())

    def get_number_neurons(self):
        return self._number_neurons

    def get_lower_bound(self):
        return self._lower_bound

    def get_upper_bound(self):
        return self._upper_bound

    def get_neuron(self, neuron_id):
        return self._neuron_reference.get_neuron(neuron_id)

    def neuron_dies(self, neuron_id):
        if neuron_id in self._neurons:
            self.get_neuron().kill()

class Neuron(object):
    def __init__(self, neuron_reference,
                    synapse_reference,
                    neuron_id,
                    signal,
                    fire_threshold,
                    max_response,
                    min_response,
                    amplification,
                    signal_decay,
                    response_decay,
                    synapse_strength,
                    synapse_max_strength,
                    synapse_improve_rate,
                    synapse_decrease_rate,
                    synapse_decay,
                    synapse_saturation):
    
        self._id = neuron_id
        self._signal = signal
        self._fire_threshold = fire_threshold
        self._response = 0
        self._max_response = max_response
        self._min_response = min_response
        self._amplification = amplification
        self._signal_decay = signal_decay
        self._response_decay = response_decay
        self._synapse_reference = synapse_reference
        self._downstream_impact = random.choice([-1, 1])

        self._dendrites = Synapses(neuron_reference=neuron_reference, 
                    synapse_reference=synapse_reference,
                    strength = synapse_strength,
                    max_strength = synapse_max_strength,
                    improve_rate = synapse_improve_rate,
                    decrease_rate = synapse_decrease_rate,
                    decay = synapse_decay,
                    saturation = synapse_saturation)
        self._axon_terminals = Synapses(neuron_reference=neuron_reference,
                    synapse_reference=synapse_reference,
                    strength = synapse_strength,
                    max_strength = synapse_max_strength,
                    improve_rate = synapse_improve_rate,
                    decrease_rate = synapse_decrease_rate,
                    decay = synapse_decay,
                    saturation = synapse_saturation)

    def process_dendrites(self):
        for synapse in self._dendrites.iter_synapses_values():
            self._signal += synapse.get_signal()


    def fire(self):
        if self._signal >= self._fire_threshold:
            self._response = self._max_response
            return 1
        else:
            self._response = self._signal * self._amplification
            if self._response > self._max_response:
                self._response = self._max_response
                return 1
            elif self._response < self._min_response:
                self._response = self._min_response
                return 0
            else:
                return 0

    def adapt(self):
        if self._response >= self._max_response:
            for terminal in self._axon_terminals.iter_synapses_values():
                positive_adaptation = terminal.adapt()
                if positive_adaptation:
                    self._synapse_reference.add_positive_adapt()
                else:
                    self._synapse_reference.add_negative_adapt()

    def release_neurotransmitters(self):
        fired = self.fire()
        for terminal in self._axon_terminals.iter_synapses_values():
            terminal.transmit_signal(self._response * self._downstream_impact)
        return fired

    def decay(self):
        '''
        print 'decay'
        print 'signal before', self._signal
        print 'response before', self._response
        '''
        self._signal *= (1 - self._signal_decay)
        self._response *= (1 - self._response_decay)
        '''
        print 'signal after', self._signal
        print 'response after', self._response
        '''

    def kill(self):
        self._response = 0
        self._signal = 0
        self._dendrites.remove_all_connections()
        self._axon_terminals.remove_all_connections()

    def set_signal(self, value):
        self._signal = value

    def get_id(self):
        return self._id

    def is_firing(self):
        return self._signal >= self._fire_threshold

    def set_response(self, value):
        if value > self._max_response:
            self._response = self._max_response
        elif value < self._min_response:
            self._response = self._min_response
        else:
            self._response = value
        return self._response

    def get_response(self):
        return self._response
    
    def get_signal(self):
        return self._signal

    def add_outgoing_connection(self, neuron_id):
        self._axon_terminals.add_connection(self.get_id(), neuron_id)

    def add_incoming_connection(self, neuron_id):
        self._dendrites.add_connection(neuron_id, self.get_id())

    def remove_outgoing_connection(self, neuron_id):
        self._axon_terminals.remove_connection(self.get_id(), neuron_id)

    def remove_incoming_connection(self, neuron_id):
        self._dendrites.remove_connection(neuron_id, self.get_id())

    def adjust_outgoing_connection(self, neuron_id):
        self._axon_terminals.adjust_connection(self.get_id(), neuron_id)

    def adjust_incoming_connection(self, neuron_id):
        self._dendrites.adjust_connection(self.get_id(), neuron_id)