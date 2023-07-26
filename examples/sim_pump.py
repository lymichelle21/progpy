# Copyright © 2021 United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration.  All Rights Reserved.

"""
Example of a centrifugal pump being simulated until threshold is met. 
"""

from progpy.models import CentrifugalPump
import matplotlib.pyplot as plt  
from progpy.sim_result import SimResult
def run_example(): 
    # Step 1: Setup Pump
    pump = CentrifugalPump(process_noise= 0)
    pump.parameters['x0']['wA'] = 0.01  # Set Wear Rate

    # Step 2: Setup Future Loading
    cycle_time = 3600
    def future_loading(t, x=None):
        t = t % cycle_time
        if t < cycle_time/2.0:
            V = 471.2389
        elif t < cycle_time/2 + 100:
            V = 471.2389 + (t-cycle_time/2)
        elif t < cycle_time - 100:
            V = 571.2389
        else:
            V = 471.2398 - (t-cycle_time)

        return pump.InputContainer({
            'Tamb': 290,
            'V': V,
            'pdisch': 928654, 
            'psuc': 239179, 
            'wsync': V * 0.8
        })

    # Step 3: Sim
    first_output = pump.output(pump.initialize(future_loading(0),{}))
    config = {
        'horizon': 1e5,
        'save_freq': 1e3,
        'print': True
    }
    simulated_results = pump.simulate_to_threshold(future_loading, first_output, **config)

    # Step 4: Plot Results
    simulated_results.inputs.plot(compact = False, title = 'Inputs', xlabel = 'time', ylabel = {lbl: lbl for lbl in pump.inputs})
    simulated_results.outputs.plot(compact = False, title = 'Outputs', xlabel = 'time', ylabel = '')
    simulated_results.states.plot(compact = False, title = 'States', xlabel = 'time', ylabel = '')
    simulated_results.event_states.plot(compact = False, title = 'Events', xlabel = 'time', ylabel = '')

    thresholds_met = [pump.threshold_met(x) for x in simulated_results.states]
    thresholds_met = SimResult(simulated_results.times, thresholds_met)
    thresholds_met.plot(compact = False, title = 'Threshold Met', xlabel = 'time', ylabel = '')

    plt.show()

# This allows the module to be executed directly 
if __name__ == '__main__':
    run_example()
