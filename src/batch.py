import main
import logging
import time
import random
import gc

def run(	output_switches_minimum=500,
			output_accuracy_minimum=0.5,
			similarity_gain_target_over_top_minimum=-0.03,
			input_filename='input/repetition.txt',
			interesting_finds_filename='output/interesting_finds.txt'):
	logging.basicConfig(format='LOG %(asctime)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

	run_number = 1
	total_runs = 'N/A'

	with open(interesting_finds_filename, 'w') as output:
		pass

	start_time = time.time()
	interesting_finds = 0
	output_switches_maximum = 0
	output_switches_maximum_run = 'N/A'
	output_switches_maximum_run_count = 0
	output_switches_histogram = {}

	max_similarity_gain_target_over_top = float('-inf')
	max_similarity_gain_target_over_top_run = 'N/A'

	max_output_accuracy = 0.0
	max_output_accuracy_run = 'N/A'

	max_similarity_target_avg = 0.0
	max_similarity_target_avg_run = 'N/A'

	random.seed()

	while True:
		number_neurons = int(random.uniform(72, 250))
		number_synapses = int(random.uniform(500, 10000))
		neuron_response_maximum = random.uniform(0, 1)
		logging.info('number_neurons = ' + str(number_neurons))
		logging.info('number_synapses = ' + str(number_synapses))
		logging.info('neuron_response_maximum = ' + str(neuron_response_maximum))
		run = main.driver(number_neurons=number_neurons,
						number_synapses=number_synapses,
						synapse_strength_improve_rate=random.uniform(0, 1),
						synapse_strength_decrease_rate=random.uniform(0, 1),
						synapse_signal_decay=random.uniform(0, 1),
						neuron_signal_decay=random.uniform(0, 1),
						neuron_response_decay=random.uniform(0, 1),
						synapse_max_strength=random.uniform(0,1),
						neuron_response_minimum=0,
						neuron_response_maximum=neuron_response_maximum,
						neuron_signal_fire_threshold=random.uniform(0, 1),
						neuron_signal_starting_lower_bound=0,
						neuron_signal_starting_upper_bound=random.uniform(0, 1),

						synapse_signal_saturation=1,
						neuron_signal_amplification=random.uniform(0, 1),

						number_without_feedback=int(random.uniform(0, 1000)),

						memory_timepoints=int(random.uniform(1,20)),

						input_filename=input_filename
						)

		logging.info('Individual run time = ' + str(run['time']))
		elapsed_time = round(time.time() - start_time, 2)
		logging.info('Total elapsed time = ' +  str(elapsed_time))
		logging.info('RUN ' + str(run_number) + ' out of ' + str(total_runs) + ' completed.')

		output_switches = run['results']['output_switches']
		similarity_gain_target_over_top = run['results']['similarity_gain_target_over_top']
		output_accuracy = run['results']['output_accuracy']
		similarity_target_avg = run['results']['similarity_target_avg']

		if output_switches in output_switches_histogram:
			output_switches_histogram[output_switches] += 1
		else:
			output_switches_histogram[output_switches] = 1
		if similarity_gain_target_over_top > max_similarity_gain_target_over_top:
			max_similarity_gain_target_over_top = similarity_gain_target_over_top
			max_similarity_gain_target_over_top_run = run_number
		if output_accuracy > max_output_accuracy:
			max_output_accuracy = output_accuracy
			max_output_accuracy_run = run_number
		if similarity_target_avg > max_similarity_target_avg:
			max_similarity_target_avg = similarity_target_avg
			max_similarity_target_avg_run = run_number
		if output_switches > output_switches_maximum:
			output_switches_maximum = output_switches
			output_switches_maximum_run = run_number
			output_switches_maximum_run_count = 1
		elif output_switches == output_switches_maximum:
			output_switches_maximum_run_count += 1
		if output_switches >= output_switches_minimum or \
				run['results']['output_accuracy'] >= output_accuracy_minimum or \
				run['results']['similarity_gain_target_over_top'] >= similarity_gain_target_over_top_minimum:
			interesting_finds += 1
		logging.info(str(run['config']))
		with open(interesting_finds_filename, 'a') as output:
			output.write('RUN ' + str(run_number) + ' out of ' + str(total_runs) +
							'\n~~ Time ~~\nrun_time : ' + str(run['time']) + '\nelapsed_time : ' + str(elapsed_time) +
						 	'\n~~ Config ~~\n' + '\n'.join(sorted([str(item) for item in run['config'].items()])) +
						 	'\n~~ Results ~~\n' + '\n'.join(sorted([str(item) for item in run['results'].items()])) +
						 	'\n\n')
		logging.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		logging.info('Interesting finds = ' + str(interesting_finds))
		logging.info('Output switches histogram = ' + str(sorted(output_switches_histogram.items())))
		logging.info('Maximum output_switches = ' + str(output_switches_maximum) +
			       		' (RUN ' + str(output_switches_maximum_run) +
			       			', COUNT ' + str(output_switches_maximum_run_count) + ')')
		logging.info('Maximum similarity_gain_target_over_top = ' + str(max_similarity_gain_target_over_top) + \
					' (RUN ' + str(max_similarity_gain_target_over_top_run) + ')')
		logging.info('Maximum output_accuracy = ' + str(max_output_accuracy) + \
					' (RUN ' + str(max_output_accuracy_run) + ')')
		logging.info('Maximum similarity_target_avg = ' + str(max_similarity_target_avg) + \
					' (RUN ' + str(max_similarity_target_avg_run) + ')')
		run_number += 1
		logging.info('---------------------------------------------')

		gc.collect()

if __name__ == '__main__':
	run()
