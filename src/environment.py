import logging
from vectormath import VectorMath

class Environment(object):
    def __init__(self, learner, outside, iterations, duration, buffer, output_continuation, number_without_feedback, memory_timepoints):
        self._learner = learner
        self._outside = outside
        self._iterations = iterations
        self._duration = duration
        self._buffer = buffer
        self._output_continuation = output_continuation
        # self._number_without_feedback = number_without_feedback
        self._transducer_in = outside.get_transducer(range(0,36), learner, memory_timepoints)
        self._transducer_out = outside.get_transducer(range(36,72), learner, memory_timepoints)

        self._input_string = ''
        self._in_processed = ''
        self._out_processed = ''

    def run(self):
        self._outside.open()
        self.passive_associate(self._iterations)
        self.buffer(self._buffer)
        responses = self.respond()
        self._outside.close()
        self.continuation(self._output_continuation)
        return self.log_results(responses)

    def experience(self, iterations):
        i = iterations
        while i > 0:
            while self._outside.next():
                outside_input = self._transducer_in.normalize_char(self._outside.get_char())
                for x in range(self._duration):
                    self._transducer_in.process_environment(outside_input, on_signal=True, on_response=True, off_signal=True, off_response=True)
                    self._learner.process()
            self._outside.reset()
            i -= 1

    def passive_associate(self, iterations):
        i = iterations
        while i > 0:
            j = 0
            while self._outside.next():
                outside_input = self._transducer_in.normalize_char(self._outside.get_char())
                for x in range(self._duration):
                    self._transducer_in.process_environment(outside_input, on_signal=True, on_response=True, off_signal=True, off_response=True)
                    self._learner.process()
                    self._transducer_out.associate(outside_input)
                j += 1
                if j % 1000 == 0:
                    logging.info("Passive associated " + str(j))
            self._outside.reset()
            i -= 1

    def decrease_number_without_feedback(self):
        if self._number_without_feedback > 0:
            self._number_without_feedback -= 1
        return self._number_without_feedback

    def with_feedback(self):
        return self._number_without_feedback < 1

    def buffer(self, length):
        for x in range(length):
            self._learner.process()

    def respond(self):
        responses = {'max_value':[],
                    'max_indices_number':[],
                    'target_similarity':[],
                    'top_similarity':[],
                    'avg_similarity':[],
                    'is_output_correct':[]}
        while self._outside.next():
            outside_input = self._transducer_in.normalize_char(self._outside.get_char())
            for x in range(self._duration):
                self._input_string += outside_input
                self._transducer_in.process_environment(outside_input, on_signal=True, on_response=True, off_signal=True, off_response=True)
                self._learner.process()
            in_response = self._transducer_in.interpret()
            out_response = self._transducer_out.interpret()
            out_predicted = self._transducer_out.predict_char(target_char=outside_input)
            self._in_processed += in_response['char']
            self._out_processed += out_predicted['char']
            responses['max_value'].append(out_response['max_value'])
            responses['max_indices_number'].append(out_response['max_indices_number'])
            responses['target_similarity'].append(out_predicted['target_similarity'])
            responses['top_similarity'].append(out_predicted['top_similarity'])
            responses['avg_similarity'].append(out_predicted['avg_similarity'])
            responses['is_output_correct'].append(out_predicted['is_output_correct'])
        return responses

    def continuation(self, length):
        for x in range(length):
            self._in_processed += self._transducer_in.interpret()
            self._out_processed += self._transducer_out.interpret()

    def log_results(self, responses):
        response_initial = responses['max_value'][0]
        response_final = responses['max_value'][-1]
        response_average = sum(responses['max_value']) / float(len(responses['max_value']))
        max_indices_min = min(responses['max_indices_number'])
        max_indices_max = max(responses['max_indices_number'])
        max_indices_average = sum(responses['max_indices_number']) / float(len(responses['max_indices_number']))
        results = {         'firings' : self._learner.get_firings(),
                            'positive_adapts' : self._learner.get_positive_adapts(),
                            'negative_adapts' : self._learner.get_negative_adapts(),
                            'input_processed' : self._in_processed,
                            'input_unique' : self.get_unqiues(self._in_processed),
                            'input_switches' : self.get_switches(self._in_processed),
                            'output_processed' : self._out_processed,
                            'output_unique' : self.get_unqiues(self._out_processed),
                            'output_switches' : self.get_switches(self._out_processed),
                            'response_initial' : response_initial,
                            'response_final' : response_final,
                            'response_average' : response_average,
                            'max_indices_min' : max_indices_min,
                            'max_indices_max' : max_indices_max,
                            'max_indices_average' : max_indices_average,
                            'similarity_target_avg' : VectorMath.average(responses['target_similarity']),
                            'similarity_top_avg' : VectorMath.average(responses['top_similarity']),
                            'similarity_avg_avg' : VectorMath.average(responses['avg_similarity']),
                            'similarity_gain_target_over_top' : VectorMath.average(responses['target_similarity']) - \
                                                                                VectorMath.average(responses['top_similarity']),
                            'similarity_gain_target_over_avg' : VectorMath.average(responses['target_similarity']) - \
                                                                                VectorMath.average(responses['avg_similarity']),
                            'output_accuracy' : float(sum(responses['is_output_correct'])) / len(responses['is_output_correct'])
                            }

        for key, value in sorted(results.iteritems()):
            if key != 'input_processed' and key != 'output_processed':
                logging.info(key + ' = ' + str(value))

        return results

    def get_unqiues(self, string):
        return len(set(string))

    def get_switches(self, string):
        current = None
        switches = 0
        for term in string:
            if current != term:
                switches+= 1
                current = term
        return switches
