import numpy
import pylab
import os
import ast

dpi_n = 120
path = ''

def spike_make_diagram(ts, gids, name):
    pylab.figure()
    color_marker = "."
    color_bar = "blue"
    color_edge = "black"
    ylabel = "Neuron ID"

    hist_binwidth = 5.0

    ax1 = pylab.axes([0.1, 0.3, 0.85, 0.6])
    pylab.plot(ts, gids, color_marker)
    pylab.ylabel(ylabel)
    pylab.xticks([])
    xlim = pylab.xlim()

    pylab.axes([0.1, 0.1, 0.85, 0.17])
    t_bins = numpy.arange(numpy.amin(ts), numpy.amax(ts), hist_binwidth)
    n, bins = pylab.histogram(ts, bins=t_bins)
    t_bins = t_bins[:-1]                        # FixMe it must work without cutting the end value
    num_neurons = len(numpy.unique(gids))
    heights = (1000 * n / (hist_binwidth * num_neurons))
    pylab.bar(t_bins, heights, width=hist_binwidth, color=color_bar, edgecolor=color_edge)
    pylab.yticks([int(a) for a in numpy.linspace(0.0, int(max(heights) * 1.1) + 5, 4)])
    pylab.ylabel("Rate (Hz)")
    pylab.xlabel("Time (ms)")
    pylab.xlim(xlim)
    pylab.axes(ax1)

    pylab.title('Spike activity')
    pylab.draw()
    pylab.savefig(path + name + ".png", dpi=dpi_n, format='png')
    pylab.close()


def voltage_make_diagram(times, voltages, name, title):
    timeunit="ms"
    line_style = ""
    for i in xrange(len(times)):
        pylab.plot(times[i], voltages[i], line_style, label=title[i])
    pylab.ylabel("Membrane potential (mV)")
    pylab.xlabel("Time (%s)" % timeunit)
    pylab.legend(loc="best")
    pylab.title("Voltmeter")
    pylab.draw()
    pylab.savefig(path + name + ".png", dpi=dpi_n, format='png')
    pylab.close()


def start(path, spike_interval, volt_interval):
    x_detector = []
    y_detector = []

    neurons_id = []
    x_multimeter = []
    y_multimeter = []

    begin_ID_spike = int(spike_interval[0]) - 1
    end_ID_spike = int(spike_interval[1]) - 1

    begin_ID_volt = int(volt_interval[0]) - 1
    end_ID_volt = int(volt_interval[1]) - 1

    with open(path + 'database.txt', 'r') as f:
        for i, line in enumerate(f):
            # fill detector data
            if begin_ID_spike <= i <= end_ID_spike:
                # 0) ID 1) Coords 2) Spikes time 3) Voltage 4) Time of voltage
                data = line.split('|')
                # Converting a string representation of a list into an actual list object
                spikes = ast.literal_eval(data[2].strip())
                x_detector.extend( spikes )
                y_detector.extend( [int(data[0])]*len(spikes) )

            # fill multimeter value
            if begin_ID_volt <= i <= end_ID_volt:
                # 0) ID 1) Coords 2) Spikes time 3) Voltage 4) Time of voltage
                data = line.split('|')
                # add current neuron ID
                neurons_id.append(int(data[0]))
                # Converting a string representation of a list into an actual list object
                x_multimeter.append( ast.literal_eval(data[4].strip()) )
                y_multimeter.append( ast.literal_eval(data[3].strip()) )

            # break if all is readed
            if i > end_ID_spike and i > end_ID_volt:
                break
    # send detector data list to building diagram (send as one detector)
    if len(x_detector) > 0:
        spike_make_diagram(x_detector, y_detector, 'spike_detector')
    else:
        print "Spike activity not found in this interval {0}".format(spike_interval)

    # send multimeters data lists to building diagram (send as many multimeters for different colors)
    if len(x_multimeter) > 0:
        voltage_make_diagram(x_multimeter, y_multimeter, 'multimeter', neurons_id)
    else:
        print "Membrane potential activity not found in this interval {0}".format(volt_interval)

    print "Diagram created"
    del x_detector, y_detector, x_multimeter, y_multimeter

if __name__ == '__main__':
    global path
    path = raw_input("Enter path to the database.txt: ")
    path += "/" if path[-1:] != "/" else ''

    spike_interval = raw_input("Enter interval for spike detectors. For example: 4 10 ")
    spike_interval = spike_interval.split(' ')

    volt_interval = raw_input("Enter interval for voltemer: ")
    volt_interval = volt_interval.split(' ')

    start(path, spike_interval, volt_interval)