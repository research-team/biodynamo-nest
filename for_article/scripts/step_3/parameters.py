import nest
from property import *

# Reset old kernel
nest.ResetKernel()


# Neuron parameters
iaf_neuronparams = {'E_L': -70.,        # Resting membrane potential in mV
                    'V_th': -50.,       # Spike threshold in mV
                    'V_reset': -67.,    # Reset membrane potential after a spike in mV
                    'C_m': 2.,          # Capacity of the membrane in pF
                    't_ref': 2.,        # Duration of refractory period (V_m = V_reset) in ms
                    'V_m': -60.,        # Membrane potential in mV at start
}

# Glutamate synapse
synparams_Glu = {'weight': w_Glu}

# GABA synapse
synparams_GABA = {'weight': w_GABA}

# Parameters for generator
synparams_Static = {'weight': w_Glu * 5, 'delay': 1.}

# Set standard synapse behavior
nest.CopyModel('static_synapse', glu_synapse, synparams_Glu)
nest.CopyModel('static_synapse', gaba_synapse, synparams_GABA)
nest.CopyModel('static_synapse', static_syn, synparams_Static)

# Parameters of multimeter
multimeter_param = {'interval': 0.1,
                    'record_from': ['V_m']}




