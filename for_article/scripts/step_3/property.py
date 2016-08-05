import sys
import random

# Keys
k_X = 0          # float:   X coord
k_Y = 1          # float:   Y coord
k_neighbors  = 2 # dict():  info about neighbors
k_detector   = 3 # tuple(): nest detector tuple
k_activity   = 4 # list():  activity info of neuron
k_model      = 5 # str      type of nerotransmitter

# For ACTIVITY list
k_result = 0    # float:   growing up distance value
k_size   = 1    # int:     size of detector events

# For NEIGHBOR dict
k_current   = 0 # float:   current distance
k_absolute  = 1 # float:   full distance
k_connected = 2 # bool:    connected or not

# Synapses keys
glu_synapse  = 'glu_synapse'
gaba_synapse = 'gaba_synapse'
static_syn   = 'gen_synapse'

# Synapses weight
w_Glu  = 3.
w_GABA = -w_Glu * 2

# RANDOM grow or not
random_value = 0.5 # 0.5 ~ 50/50

# mean and standard deviation for growing distance
mu, sigma = 0.4, 0.07

# divide Normal distr by
div = 2

# Simulation iteration
time = 40

# Simulation step for each iteration (in ms)
dt = 5.

# Spread coord (more value -- more chaos)
spreading_x = 0.6
spreading_y = 0.2

# Coeficient for grow up function
coef = 0.5

# N x M (2D dimension)
N = 20
M = 10

# Set radius of catching neighbors
R = 2.

# Neuron number
neuron_number = N * M

# Percent of inhibitory neurons
inhibitory_neuron_percent = 0.3
inhibitory_neurons = random.sample(xrange(1, neuron_number + 1), int(inhibitory_neuron_percent * neuron_number))
# Percent of all neurons with generators
gen_percent = 0.1

# connect GENERATOR to these neurons. Take N*percent different random neurons from all neurons
gen_list = random.sample(xrange(1, neuron_number + 1), int(neuron_number * gen_percent))
# monitoring activity, fill by void lists
monitoring = {key:list() for key in xrange(time)}

# Main dict of neuron information
# key: neuronID | value: X, Y, dict of neighbors, splike_detector, [activity, spikes at dt]
network = {}

# support dict to get id from coordinate
# key: coord (X,Y) | value: neuronID
network_coord_id = {}

# keep info about neurons (for analyse)
neurons_info = []

# draw flag
draw_flag = False

# lists for drawing points
x_list = []
y_list = []