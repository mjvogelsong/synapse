class Sequence(object):
	def __init__(self, max_response, max_signal):
		self._max_response = max_response
		self._max_signal = max_signal

	def next(self):
		raise NotImplementedError

	def get_transducer(self):
		raise NotImplementedError
