import logging
from environment import Environment
from charactersequence import CharacterSequence
from neuron_reference import NeuronReference
from synapsereference import SynapseReference
from neuron import Neurons
import inspect
import time

def driver(number_neurons=500,
			number_synapses=10000,
			experience_iterations=1,
			experience_duration=1,
			experience_buffer=0,
			input_filename='input/example.txt',
			output_continuation=0,
			synapse_strength=1,
			synapse_max_strength=1,
			synapse_strength_improve_rate=0.1,
			synapse_strength_decrease_rate=0.01,
			synapse_signal_decay=0.01,
			synapse_signal_saturation=1,
			neuron_signal_starting='random',
			neuron_signal_fire_threshold=0.5,
			neuron_response_maximum=10,
			neuron_response_minimum=-10,
			neuron_signal_amplification=1,
			neuron_signal_decay=0.01,
			neuron_response_decay=0.001,
			neuron_signal_starting_lower_bound=-10,
			neuron_signal_starting_upper_bound=10,
			number_without_feedback=0,
			memory_timepoints=10):

	time_start = time.time()

	frame = inspect.currentframe()
	args, _, _, values = inspect.getargvalues(frame)

	logging.basicConfig(format='LOG %(asctime)s: %(message)s', datefmt='%m/%d/%Y-%H:%M:%S', level=logging.INFO)

	synapse_reference = SynapseReference()
	logging.info('Creating neurons...')
	neuron_reference = NeuronReference()
	brain_neurons = Neurons(neuron_reference=neuron_reference, synapse_reference=synapse_reference,
									number_neurons=number_neurons,
									lower_bound=neuron_signal_starting_lower_bound,
									upper_bound=neuron_signal_starting_upper_bound,
									signal=neuron_signal_starting,
									fire_threshold=neuron_signal_fire_threshold,
									max_response=neuron_response_maximum,
									min_response=neuron_response_minimum,
									amplification=neuron_signal_amplification,
									signal_decay=neuron_signal_decay,
									response_decay=neuron_response_decay,
									synapse_strength=synapse_strength,
				                    synapse_max_strength=synapse_max_strength,
				                    synapse_improve_rate=synapse_strength_improve_rate,
				                    synapse_decrease_rate=synapse_strength_decrease_rate,
				                    synapse_decay=synapse_signal_decay,
				                    synapse_saturation=synapse_signal_saturation)



	logging.info('Creating synapses...')
	brain_neurons.add_random_synapses(number=number_synapses)

	logging.info('Setting up environment...')
	env = Environment(learner=brain_neurons,
						outside=CharacterSequence(filename=input_filename,
													max_response=neuron_response_maximum,
													max_signal=neuron_signal_fire_threshold),
						iterations=experience_iterations,
						duration=experience_duration,
						buffer=experience_buffer,
						output_continuation=output_continuation,
						number_without_feedback=number_without_feedback,
						memory_timepoints=memory_timepoints)

	logging.info('Running...')
	results = env.run()

	return {'config' : values, 'results' : results, 'time' : round(time.time()-time_start,2)}

if __name__ == '__main__':
	driver()
