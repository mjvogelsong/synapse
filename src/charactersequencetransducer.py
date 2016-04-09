from transducer import Transducer
from history import History

class CharacterSequenceTransducer(Transducer):
	def __init__(self, valid_neuron_ids, max_response, max_signal, neurons, memory_timepoints):
		super(CharacterSequenceTransducer, self).__init__(valid_neuron_ids=valid_neuron_ids,
															max_response=max_response,
															max_signal=max_signal,
															neurons=neurons)

		self._index_to_char = {	26 : ' ',
								27 : '\n',
								28 : '\t',
								29 : ',',
								30 : '\'',
								31 : '"',
								32 : '.',
								33 : '!',
								34 : '?',
								35 : '~'
		}
		for x in range(26):
			self._index_to_char[x] = str(unichr(x + 97))

		self._char_to_index = self.reverse_map(self._index_to_char)
		self._default_index = 35
		self._default_char = '~'
		self._vector_length_needed = self._default_index + 1
		self._history = History(num_timepoints=memory_timepoints, vector_length=self._vector_length, classes=self._char_to_index.keys())

	def reverse_map(self, map):
		reverse_map = {}
		for key, value in map.iteritems():
			reverse_map[value] = key
		return reverse_map

	def process_environment(self,env_input, on_signal=False, on_response=False, off_signal=False, off_response=False):
		vector_index = self.to_index(env_input)

		for i, neuron_id in enumerate(self._neuron_ids):
			if i == vector_index:
				if on_signal:
					self._neurons.get_neuron(neuron_id).set_signal(self._max_signal)
				if on_response:
					self._neurons.get_neuron(neuron_id).set_response(self._max_response)
			else:
				if off_signal:
					self._neurons.get_neuron(neuron_id).set_signal(0)
				if off_response:
					self._neurons.get_neuron(neuron_id).set_response(0)

	def interpret(self):
		values = [self._neurons.get_neuron(neuron_id).get_response() for neuron_id in self._neuron_ids]
		max_index = self.get_max_index(values)
		max_value = values[max_index]
		max_indices = [i for i, value in enumerate(values) if value == max_value]
		char = self.to_char(max_index)
		return {	'char' : char,
					'max_value' : max_value,
					'max_index' : max_index,
					'max_indices' : max_indices,
					'max_indices_number' : len(max_indices)
					}

	def associate(self, decoded):
		response_vector = self.get_response_vector()
		historic_similarity = self._history.get_similarity(response_vector, decoded)
		historic_similarity_average = self._history.get_similarity_average(historic_similarity)
		self._history.update_memory(response_vector, decoded, historic_similarity)
		return historic_similarity_average

	def predict_char(self, target_char=None):
		return self._history.get_most_likely_class(self.get_response_vector(), update_memory=True, target_class=target_char)

	def normalize_char(self, char):
		lower_raw = char.lower()
		return self.to_char(self.to_index(lower_raw))

	def to_char(self, index):
		if index in self._index_to_char:
			return self._index_to_char[index]
		else:
			return self._default_char

	def to_index(self, char):
		if char in self._char_to_index:
			return self._char_to_index[char]
		else:
			return self._default_index

	def get_max_index(self, values):
		return values.index(max(values))

