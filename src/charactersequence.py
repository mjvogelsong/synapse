from sequence import Sequence
from charactersequencetransducer import CharacterSequenceTransducer
import io

class CharacterSequence(Sequence):
	def __init__(self, filename, max_response, max_signal):
		super(CharacterSequence, self).__init__(max_response=max_response, max_signal=max_signal)
		self._filename = filename
		self._stream = None
		self._char = None

	def open(self):
		self._stream = io.open(self._filename)

	def close(self):
		self._stream.close()
		self._stream = None

	def reset(self):
		self.close()
		self.open()

	def next(self):
		self._char = self._stream.read(1)
		return self._char
		
	def get_char(self):
		return self._char

	def get_transducer(self, valid_neuron_ids, neurons, memory_timepoints):
		return CharacterSequenceTransducer(valid_neuron_ids=valid_neuron_ids, max_response=self._max_response, max_signal=self._max_signal, neurons=neurons, memory_timepoints=memory_timepoints)
