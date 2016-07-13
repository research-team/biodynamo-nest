from parameters import *

import numpy as np
import matplotlib.pyplot as plt


def formula(neuron_id, new_size, old_size):
    """ Grow up distance formula"""
    events = sum(nest.GetStatus(network[neuron_id][k_detector])[0]['events']['senders'][old_size - new_size:])
    return float(coef) * events / dt


def connect_devices():
    """ Device connection method"""
    # multimeter
    mm = nest.Create('multimeter', params=multimeter_param)
    nest.Connect(mm, volt_list)
    multimeters.append(mm)

    # generator
    sg_pre = nest.Create('poisson_generator')
    nest.SetStatus(sg_pre, {'rate': 300.0})
    nest.Connect(sg_pre, gen_list)

    # detector
    sd = nest.Create('spike_detector')
    nest.Connect(detect_list, sd)
    detectors.append(sd)


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
    nest.Connect( (pre,), (post,) )
    # Save information about connection
    monitoring[step].append("pre: {0} post: {1}".format(pre, post))


def getDistance(source, target):
    """ sqrt( dx^2 + dy^2 )"""
    return np.sqrt((network[source][k_X] - network[target][k_X]) ** 2 +
                   (network[source][k_Y] - network[target][k_Y]) ** 2)


def initialize(n, m, radius):
    """ Initialize neuron coords and neigbors"""
    # init first ID (by standard it is 1)
    neuronID = nest.Create('iaf_neuron', n * m)[0]
    # build 2D dimension area
    for y in range(m):
        for x in range(n):
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
        # expand data by concatenation of tuples
        network[neuron_id] += (dict(dict_neighbors), spike_detector, [0, 0] )
        # System information about neuron and his neighbors
        print neuron_id, network[neuron_id][:2], network[neuron_id][k_neighbors].keys()


def initActivity():
    """ Calculate activity of neuron"""
    for neuron_id in network:
        # get old size of senders
        old_size = network[neuron_id][k_activity][k_size]
        # get new size of senders
        new_size = len(nest.GetStatus(network[neuron_id][k_detector])[0]['events']['senders'])
        # if was any activity
        if new_size != old_size:
            # get grow up value by formula and activity
            result = formula(neuron_id, new_size, old_size)
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


def simulate(steps):
    """ Simulation method"""
    for step in xrange(steps):
        # Simulate dt
        nest.Simulate(dt)
        # Refresh activity
        initActivity()
        # Update info and check on connection
        updateDistanceAndCheck(step)


def save():
    """ Save all results into files"""
    import nest.raster_plot
    import nest.voltage_trace

    for detector in detectors:
        if len( nest.GetStatus(detector)[0]['events']['senders'] ) > 0:
            nest.raster_plot.from_device(detector)
            plt.savefig("spikes.png", dpi=120, format='png')
            plt.close()

    for multimeter in multimeters:
        nest.voltage_trace.from_device(multimeter)
        plt.savefig("voltage.png", dpi=120, format='png')
        plt.close()

    with open("monitor.txt", 'w') as f:
        for item in monitoring:
            f.write('- - - - - {0} - - - - -\n'.format(item))
            for element in monitoring[item]:
                f.write('   {0}\n'.format(element))
            f.write('\n')


'''
DRAWING

before build lists of coords:
x_list = []
y_list = []

    for neuron_id in network:
        x_list.append(network[neuron_id][k_X])
        y_list.append(network[neuron_id][k_Y])


def updateDistanceAndCheck(step):
    ax = plt.subplot()
    ax.plot(x_list, y_list, marker='.', ls='')
    plt.title("{0}/{1}".format(step, time-1))

    for neuron_id in network:
        for neighbor_id in network[neuron_id][k_neighbors]:
            startX = network[neuron_id][k_X]
            startY = network[neuron_id][k_Y]
            . . . .

                # drawing
                current  = float(network[neuron_id][k_neighbors][neighbor_id][k_current])
                absolute = float(network[neuron_id][k_neighbors][neighbor_id][k_absolute])
                if current:
                    # curr / abs - curr
                    if absolute - current > 0:
                        alpha = current / (absolute - current)

                        Xa = (startX + alpha * network[neighbor_id][k_X]) / (1 + alpha)
                        Ya = (startY + alpha * network[neighbor_id][k_Y]) / (1 + alpha)
                        ax.plot( [startX, Xa],
                                 [startY, Ya] )
                    else:
                        ax.plot([startX, network[neighbor_id][k_X]],
                                [startY, network[neighbor_id][k_Y]])
            else:
                ax.plot( [startX, network[neighbor_id][k_X]],
                         [startY, network[neighbor_id][k_Y]] )
    plt.show()
'''
'''
SHOW NEURON ID IN PLOT
    n_list = range(network.keys()[0], N * M + 1)
    ax = pylab.subplot()
    ax.scatter(x_list, y_list)

    for i, txt in enumerate(n_list):
        ax.annotate(txt, (x_list[i], y_list[i]))
    pylab.show()
'''