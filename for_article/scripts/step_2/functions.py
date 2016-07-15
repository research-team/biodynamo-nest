import datetime
import numpy as np
import matplotlib.pyplot as plt
from parameters import *

start_time = 0
time_simulation = 0
time_init = 0

def formula(new_size, old_size):
    """ Grow up distance formula"""
    events = new_size - old_size
    return float(coef) * events / dt


def connect_generator():
    """ Generator connection method"""
    sg_pre = nest.Create('poisson_generator')
    nest.SetStatus(sg_pre, {'rate': 300.0})
    nest.Connect(sg_pre, gen_list, syn_spec=static_syn)


def getID(x, y):
    """ Get neuron ID by coordinates"""
    return network_coord_id[ (x, y) ]


def getNeighbors(coords, radius):
    """ Return list of neighbors for these coords in radius"""
    x = coords[0]
    y = coords[1]
    neigbors_list = []
    radCube = radius ** 2
    # FixMe not perfomance algorithm, try to optimize
    for neuron_id in network:
        neuron = network[neuron_id]
        if (x - neuron[k_X]) ** 2 + (y - neuron[k_Y]) ** 2 <= radCube:
            neigbors_list.append(neuron_id)
    # delete center neuron
    neigbors_list.remove(getID(x, y))

    return neigbors_list


def connect(pre, post, step):
    """ Coonection method"""
    # Connect these neurons (convert to tuple)
    nest.Connect( (pre,), (post,), syn_spec=network[pre][k_model] )
    # Save information about connection
    monitoring[step].append("pre: {0} post: {1} type: {2}".format(pre, post, network[pre][k_model]))


def getDistance(source, target):
    """ sqrt( dx^2 + dy^2 )"""
    return np.sqrt((network[source][k_X] - network[target][k_X]) ** 2 +
                   (network[source][k_Y] - network[target][k_Y]) ** 2)


def initialize(n, m, radius):
    """ Initialize neuron coords and neigbors"""
    global start_time, time_init
    start_time = datetime.datetime.now()

    inhibitory_neurons_temp = list(inhibitory_neurons)
    nest.SetDefaults('iaf_neuron', iaf_neuronparams)
    # init first ID (by standard it is 1)
    neuronID = nest.Create('iaf_neuron', neuron_number)[0]
    # build 2D dimension area
    for y in xrange(m):
        for x in xrange(n):
            # introduce some chaotic into grid
            temp_x = x + np.random.uniform(-spreading_x, spreading_x)
            temp_y = y + np.random.uniform(-spreading_y, spreading_y)
            # add to main dict tuple of coords
            network[neuronID] = (temp_x, temp_y)
            # fill support dict
            network_coord_id[ (temp_x, temp_y) ] = neuronID
            # increase neuronID
            neuronID += 1

    # init neighbors and add info
    for neuron_id in network:
        # key: neuron ID | value: current distance, full distance, connected or not
        dict_neighbors = {}
        # getNeighbor and fill info
        for neighbor_id in getNeighbors(network[neuron_id][:2], radius):
            # calculate distance to this neighbor neuron
            dict_neighbors[neighbor_id] = [0, getDistance(neuron_id, neighbor_id), False]
        # attach spikedetector
        spike_detector = nest.Create('spike_detector')
        nest.Connect( (neuron_id,), spike_detector )

        mm = nest.Create('multimeter', params=multimeter_param)
        nest.Connect( mm, (neuron_id,) )

        # expand data by concatenation of tuples
        network[neuron_id] += (dict(dict_neighbors), spike_detector, mm, [0, 0])

        # init neurotransmitter type
        if neuron_id in inhibitory_neurons_temp:
            network[neuron_id] += (gaba_synapse,)
            inhibitory_neurons_temp.remove(neuron_id)
        else:
            network[neuron_id] += (glu_synapse,)

        # System information about neuron and his neighbors
        neurons_info.append('ID: {0}, {1}, {2}, {3}'.format(neuron_id,
                                                            network[neuron_id][:2],
                                                            network[neuron_id][k_neighbors].keys(),
                                                            network[neuron_id][k_model]))
    if draw_flag:
        for neuron_id in network:
            x_list.append(network[neuron_id][k_X])
            y_list.append(network[neuron_id][k_Y])

    time_init = datetime.datetime.now() - start_time


def initActivity():
    """ Calculate activity of neuron"""
    for neuron_id in network:
        # get old size of events
        old_size = network[neuron_id][k_activity][k_size]
        # get new size of events
        new_size = len(nest.GetStatus(network[neuron_id][k_detector])[0]['events']['times'])
        # if was any activity
        if new_size != old_size:
            # get grow up value by formula and activity
            result = formula(new_size, old_size)
            # if activity is growing up
            if result >= network[neuron_id][k_activity][k_result]:
                # set new growing distance value
                network[neuron_id][k_activity][k_result] = result
            else:
                # set zero growing distance value
                network[neuron_id][k_activity][k_result] = 0
        # update the size of senders
        network[neuron_id][k_activity][k_size] = new_size


def updateDistanceAndCheck(step):
    """ Update distances for all neighbors of neuron"""
    for neuron_id in network:
        for neighbor_id in network[neuron_id][k_neighbors]:
            # update info if neurons are not connected
            if not network[neuron_id][k_neighbors][neighbor_id][k_connected]:
                # get list of information between neuron and his neighbor
                neighbor_info = network[neuron_id][k_neighbors][neighbor_id]
                # increase current distance by new grow up value
                neighbor_info[k_current] += network[neighbor_id][k_activity][k_result]
                # check if there new connections
                if neighbor_info[k_current] >= neighbor_info[k_absolute]:
                    # connect them, also send log information about 'step' iteartion
                    connect(neighbor_id, neuron_id, step)
                    # Set 'connected' status
                    network[neuron_id][k_neighbors][neighbor_id][k_connected] = True
    if draw_flag:
        draw(step)

def simulate(steps):
    """ Simulation method"""
    global start_time, time_simulation
    start_time = datetime.datetime.now()
    for step in xrange(steps):
        # Simulate dt
        nest.Simulate(dt)
        # Refresh activity
        initActivity()
        # Update info and check on connection
        updateDistanceAndCheck(step)
    time_simulation = datetime.datetime.now() - start_time

def save():
    """ Save all results into files"""
    with open("monitor.txt", 'w') as f:
        f.write('Init time: {0} | Real time: {1} | Simulation time {2}s\n'.format(time_init,
                                                                                  time_simulation,
                                                                                  dt*time*0.001))
        for item in monitoring:
            f.write('- - - - - {0} - - - - -\n'.format(item))
            for element in monitoring[item]:
                f.write('{0}\n'.format(element))
            f.write('\n')

    with open("neurons_info", 'w') as f:
        f.write('Inhibitory: {}\n'.format(sorted(inhibitory_neurons)))
        f.write('With generator: {}\n'.format(sorted(gen_list)))

        for item in neurons_info:
            f.write('{}\n'.format(item))

    with open("database.txt", 'w') as f:
        for neuron_id in network:
            f.write('{0} | {1} | {2} | {3} | {4}\n'.format(
                neuron_id,
                network[neuron_id][:2],
                [round(item, 1) for item in nest.GetStatus(network[neuron_id][k_detector])[0]['events']['times']],
                [round(item, 1) for item in nest.GetStatus(network[neuron_id][k_multimeter])[0]['events']['V_m']],
                [round(item, 1) for item in nest.GetStatus(network[neuron_id][k_multimeter])[0]['events']['times']]))


def draw(step):
    """ Drawing method"""
    # init figure
    ax = plt.subplot()
    ax.plot(x_list, y_list, marker='.', ls='')
    plt.title("{0}/{1}".format(step+1, time))
    #init distances
    for neuron_id in network:
        for neighbor_id in network[neuron_id][k_neighbors]:
            # get start point
            startX = network[neuron_id][k_X]
            startY = network[neuron_id][k_Y]
            # init color
            color = 'r' if network[neighbor_id][k_model] == glu_synapse else 'b'
            # if neurons are not connected
            if not network[neuron_id][k_neighbors][neighbor_id][k_connected]:
                # get distances
                current  = float(network[neuron_id][k_neighbors][neighbor_id][k_current])
                absolute = float(network[neuron_id][k_neighbors][neighbor_id][k_absolute])
                # if current distance not zero
                if current:
                    # draw new distance and check on delta
                    if absolute - current > 0:
                        # get coord of point in new distance
                        alpha = current / (absolute - current)
                        Xa = (startX + alpha * network[neighbor_id][k_X]) / (1 + alpha)
                        Ya = (startY + alpha * network[neighbor_id][k_Y]) / (1 + alpha)
                        # draw
                        ax.plot( [startX, Xa], [startY, Ya], color='black')
            # if connected draw full connection distance
            else:
                ax.plot( [startX, network[neighbor_id][k_X]],
                         [startY, network[neighbor_id][k_Y]], color=color)
    # show new window
    plt.show()