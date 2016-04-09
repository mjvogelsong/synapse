import logging
from history import History

class Transducer(object):
	def __init__(self, valid_neuron_ids, max_response, max_signal, neurons):
		self._vector_length = len(valid_neuron_ids)
		self._neuron_ids = valid_neuron_ids
		self._max_response = max_response
		self._max_signal = max_signal
		self._neurons = neurons

	def process_environment_signal(self, raw_env_input):
		raise NotImplementedError

	def process_environment_response(self, raw_env_input):
		raise NotImplementedError

	def interpret(self):
		raise NotImplementedError
	
	def associate(self, decoded):
		raise NotImplementedError
	
	def get_response_vector(self):
		return [self._neurons.get_neuron(neuron_id).get_response() for neuron_id in self._neuron_ids]
	
	def get_signal_vector(self):
		return [self._neurons.get_neuron(neuron_id).get_signal() for neuron_id in self._neuron_ids]
			
