# TODO: attualmente le mapping/distances e i boundary plots funzionano solo rispettivamente con 'circular' e 'linear boundaries'
# TODO: the code works only plotting primes. It can compute only the linear paths of all numbers to 2^n, but not include them within the next steps. So,
#		the list of mapped_fronts does not have any color array.
# TODO: set as global variables x and y anc color, to be used as keys in array indexes
# TODO: rewrite code using bitarray, bit*, int('10101', 2), etc.
# TODO: gli output x,y devono trasformarsi in una serie di liste. Ogni lista risiede su una boundary curve 2^k
# TODO: graficare la distanza all'interno della riga 2^n
# TODO: fare la mappatura a cerchi e a lobi e e inviluppi esponenziali
# TODO: basta trovare una regolarità per p > K con K a piacere
# TODO: vectorize con numpy: specialmente la mappatura a cerchio
# TODO: implementare una versione OOP

# using some bit manipulation, tkinker embedding of matplotlib and some vectorization through numpy would not hurt.

import time
import math
import numpy as np
import matplotlib.pyplot as plt
import copy

import ctypes, sys
ctypes.windll.shcore.SetProcessDpiAwareness(1) if 'win' in sys.platform else None

# <editor-fold desc="SET GLOBAL PARAMETERS HERE">
log_2_of_total_numers_to_inspect = 12
log_2_limit_for_efficient_visualization = 18
base_graph_segments_length = 100
visualization_factor = 1.1  # a 2-factor reduces squares to half
wavefront = 'circular'
sprout = 'linear'
show_primes = False
# </editor-fold>

# <editor-fold desc="SET PLOTTING OPTIONS HERE">
plot_prime_numbers = True
plot_exp_lines = True
plot_horizon = True
plot_interdistance = True
plot_annotations, n_annotations = False, 200
only_one_graph = False
# </editor-fold>

# <editor-fold desc="pre-calculate useful global variables">
power = log_2_of_total_numers_to_inspect
n = 2 ** power
n_exp_lines = power
s = base_graph_segments_length
r = log_2_limit_for_efficient_visualization
reduction_factor = 2 ** (power - r) if power > r else 1
prime_color, non_prime_color = 'red', 'white'
f = 1 / visualization_factor
h_max = s * (1 - f ** power) / (1 - f)
h = [s * (1 - f ** k) / (1 - f) for k in range(power)]
# </editor-fold>


def generate_Erathostenes_sieve(number_cap):
	t1 = time.time()
	prime_list = list(range(number_cap+1))
	prime_list[0], prime_list[1] = 0, 0
	for index in range(int(math.sqrt(number_cap+1))):
		if prime_list[index]:
			for next_index in range(index*index, number_cap+1, index):
				prime_list[next_index] = 0
	result = set(prime_list)
	result.remove(0)
	return sorted(result), time.time() - t1


def generate_list_of_primes(show_prime_list=False):
	primes_calculated, time_spent = generate_Erathostenes_sieve(n)
	primes_calculated = [1] + list(primes_calculated)
	primes_calculated.remove(2)
	print('number of primes computed: ', len(primes_calculated))
	if reduction_factor > 1:
		primes_calculated = [x for i, x in enumerate(primes_calculated) if i % reduction_factor == 0]
		print('number of values have been reducted to: ', len(primes_calculated))
	if show_prime_list:
		print('list of primes:\n', primes_calculated)
	return len(primes_calculated), primes_calculated


def compute_one_binary_path(decimal):
	xp, yp = 0, 0
	b = bin(decimal)
	for step, i in enumerate(range(2, len(b) - 1)):
		turn = b[-i]
		if turn == '1':
			xp += s / (visualization_factor ** step)
		else:
			yp += s / (visualization_factor ** step)
	return xp, yp


def compute_all_numbers_binary_paths(set_of_primes, only_primes=True):
	# calcola il numero di primi che sono in ogni boundary (2^n-1 .. 2^n)
	single_boundary = [[], [], []]
	boundary_lines = [copy.deepcopy(single_boundary) for value in range(power)]
	x_, y_, color_ = 0, 1, 2

	def loop_in_numbers(set_of_numbers, color_type):
		for decimal in set_of_numbers:
			n_boundary = int(math.log2(decimal))  # n_boundary = len(bin(decimal)) - 2 - 1
			xp, yp = compute_one_binary_path(decimal)
			boundary_lines[n_boundary][x_].append(xp)
			boundary_lines[n_boundary][y_].append(yp)
			boundary_lines[n_boundary][color_].append(color_type)
		return boundary_lines
	boundary_lines = loop_in_numbers(set_of_primes, prime_color)
	if not only_primes:
		all_odds = set(range(1, n, 2))
		set_of_non_primes = all_odds - set(set_of_primes)
		boundary_lines = loop_in_numbers(set_of_non_primes, non_prime_color)

	return boundary_lines


def mapping_to_new_wavefronts():
	if wavefront == 'circular' and sprout == 'linear':
		new_wave_fronts = []
		for front in linear_line_fronts:
			x, y = front[0], front[1]
			x_circle, y_circle = x, y
			number_of_points = len(x)
			for i in range(number_of_points):
				R = x[i] + y[i]
				teta = math.atan2(y[i], x[i])
				x_circle[i], y_circle[i] = R*math.cos(teta), R*math.sin(teta)
			new_wave_fronts.append(copy.deepcopy([x_circle, y_circle, front[2]]))
		return new_wave_fronts
	else:
		return None


def compute_distances_on_one_boundary(list_n, number):
	"""
	
	Args:
		sprout:
		wavefront:
		list_n:
		number:

	Returns: array of angular distances

	"""
	if wavefront == 'circular' and sprout == 'linear':
		if number > 1:
			len_list = len(list_n[0])
			transformed_list = [(list_n[0][i], list_n[1][i]) for i in range(len_list)]	# same as np.transpose()
			sorted_list = sorted(transformed_list, key=lambda value: value[0], reverse=True)
			s_list = np.array(sorted_list).transpose()
			thetas = np.arctan2(s_list[1], s_list[0])
			distances_theta = (thetas - np.roll(thetas, 1))[1:]
			return distances_theta
		else:
			return h[number]*np.array(0)
	else:
		return None


def compute_distances_on_all_boundaries():
	distances_array = []
	for f_i, front in enumerate(mapped_line_fronts):
		d_a = compute_distances_on_one_boundary(front[0:2], f_i)
		distances_array.append(d_a)
	return distances_array


def plot_2raisedN_boundaries_shapes():
	pass


def graph_distances_shapes():
	pass


def graph_prime_numbers_fronts(which_window):
	for front_i in mapped_line_fronts:
		which_window.scatter(front_i[0], front_i[1], s=3, color=front_i[2])


def graph_exp_lines(which_window):
	if wavefront == 'linear' and sprout == 'linear':
		for k in range(n_exp_lines):
			o_x, o_y = [0, h[k]], [h[k], 0]
			which_window.plot(o_x, o_y, linestyle='--')
			which_window.annotate('2^%d..2^%d' %(k, k+1), (0, h[k]), size=8, rotation=-45)


def graph_horizon(which_window):
	# disegna orizzonte degli eventi
	if wavefront == 'linear' and sprout == 'linear':
		h_horiz = s / (1 - 1 / visualization_factor)
		o_x, o_y = [0, h_horiz], [h_horiz, 0]
		which_window.plot(o_x, o_y)


def graph_annotations(plot_window):
	passo_annotations = n_primes**(1/n_annotations)
	set_annotations = [0]
	index_annotazione = 1
	while index_annotazione <= n_primes:
		set_annotations.append(int(index_annotazione))
		index_annotazione = index_annotazione * passo_annotations
	print('N plot_annotations: ', len(set_annotations))
	set_annotations = sorted(list(set(set_annotations)))
	print('N plot_annotations: ', len(set_annotations))
	x, y = [], []
	for front in mapped_line_fronts:
		x.extend(front[0])
		y.extend(front[1])
	for i in set_annotations:
		full_annotation = '%s=%d' % (bin(primes_before_n[i])[2:], primes_before_n[i])
		plot_window.annotate(full_annotation, (x[i], y[i]), size=8)


def plot_distances(which_window, min_range=1, max_range=power, edge_cut_factor=1):
	# PLOT DELLE DISTANZE ANGOLARI PER I VARI FRONTI
	stretch = True
	max_range = min(max_range, power-1)
	maximums = [] # si può fare invece che sotto il "massimo" cadono il 95% dei valori...
	for i in range(min_range, max_range+1):
		maximums.append(max(all_distances_arrays[i]))
	max_d = max(maximums)/edge_cut_factor

	which_window.set_ylim(0, max_d)
	ratio = len(all_distances_arrays[max_range+1-1])/max_d
	which_window.set_aspect(ratio)
	n_max = len(all_distances_arrays[max_range+1-1])
	for i in range(max_range+1-1, min_range-1, -1):
		natural_numbers = np.arange(len(all_distances_arrays[i]))
		if not stretch:
			x_numbers = natural_numbers
		else:
			x_numbers = natural_numbers * n_max/len(natural_numbers)
		distances = all_distances_arrays[i]
		which_window.plot(x_numbers, distances, label='2^%i..2^%i' %(i-1, i))
		which_window.legend()


if __name__ == '__main__':

	print('computing primes ...')
	n_primes, primes_before_n = generate_list_of_primes(show_prime_list=show_primes)
	print('... all primes computed.')

	print('computing linear positions ... ', end='')
	linear_line_fronts = compute_all_numbers_binary_paths(primes_before_n)
	print(' done.')

	print('mapping to %s wavefronts through %s sprout lines ...' %(wavefront, sprout), end='')
	mapped_line_fronts = mapping_to_new_wavefronts()		# WARNING: IT TAKES GLOBAL VARIABLES FOR WAVEFRONTS AND SPROUTS
	print(' done.')
	
	print('computing distances on all wavefronts ...', end='')
	all_distances_arrays = compute_distances_on_all_boundaries()		# WARNING: IT TAKES GLOBAL VARIABLES FOR WAVEFRONTS AND SPROUTS
	print(' done.')
	
	if not only_one_graph:
		fig, ax1 = plt.subplots(2, 2)
		top_left = ax1[0, 0]
		top_right = ax1[0, 1]
		bottom_left = ax1[1, 0]
		bottom_right = ax1[1, 1]
		for ax2 in ax1:
			for ax3 in ax2:
				ax3.set_aspect('equal')
		top_left.set_xlim(-10, int(h_max) + 1), top_left.set_ylim(-10, int(h_max) + 1)
		top_right.set_ylim(-1, 1)
	else:
		ax1 = plt.gca()
		top_left = bottom_left = top_right = bottom_right = ax1
		ax1.set_aspect('equal')

	if plot_prime_numbers:
		graph_prime_numbers_fronts(top_left)
		
	if plot_annotations:
		graph_annotations(top_left)
		
	if plot_exp_lines:
		graph_exp_lines(bottom_left)
		
	if plot_horizon:		
		graph_horizon(bottom_left)
		
	if plot_interdistance:
		plot_distances(top_right, min_range=11, max_range=11, edge_cut_factor=1)
	
	plt.show()
