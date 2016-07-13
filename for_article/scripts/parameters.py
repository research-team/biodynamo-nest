import nest

# Keys
k_X = 0         # float:   X coord
k_Y = 1         # float:   Y coord
k_neighbors = 2 # dict():  info about neighbors
k_detector = 3  # tuple(): nest detector tuple
k_activity = 4  # list():  activity info of neuron

# For ACTIVITY list
k_result = 0    # float:   growing up distance value
k_size = 1      # int:     size of detector events

# For NEIGHBOR dict
k_current = 0   # float:   current distance
k_absolute = 1  # float:   full distance
k_connected = 2 # bool:    connected or not

# Simulation iteration
time = 100

# Simulation step for each iteration (in ms)
dt = 1.

# Spread coord (more value -- more chaos)
spreading_x = 0.6
spreading_y = 0.2

# Coeficient for grow up function
coef = 0.01

# N x M (2D dimension)
N = 5
M = 10
# Set radius of catching neighbors
R = 1.5

# connect GENERATOR to these neurons
gen_list = [2, 5, 10, 18, 25, 34, 48]

# connect global DETECTOR to these neurons
detect_list = range(10, 50)

# connect MULTIMETER to these neurons
volt_list = [2, 3, 10, 12]

# List of all multimeters
multimeters = []

# List of all spike detectors
detectors = []

# monitoring activity, fill by void lists
monitoring = { key:list() for key in range(100) }

# Main dict of neuron information
# key: neuronID | value: X, Y, dict of neighbors, splike_detector, [activity, spikes at dt]
network = {}

# support dict to get id from coordinate
# key: coord (X,Y) | value: neuronID
network_coord_id = {}

# Reset old kernel
nest.ResetKernel()

# Parameters of multimeter
multimeter_param = {'to_memory': True,
                    'to_file': False,
                    'withtime': True,
                    'interval': 0.1,
                    'record_from': ['V_m'],
                    'withgid': True}

# Set standard synapse behavior
nest.SetDefaults("static_synapse", {'weight': 500.})