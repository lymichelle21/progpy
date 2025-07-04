Release Notes
=================

.. ..  contents:: 
..     :backlinks: top

Updates in v1.8.0
----------------------

progpy
**************
* **New Feature** :term:`Discrete States<discrete state>` (created by :py:func:`progpy.create_discrete_state`): Inputs, states, outputs, or performance metrics can now be represented by a discrete state object, which will only exist in a set of defined states. See the `Discrete State Notebook <https://github.com/nasa/progpy/blob/release/v1.8/examples/discrete_state.ipynb>`__ for examples of use
* **New model**: Simplified Battery (:py:class:`progpy.models.BatterySimplified`). This is a simplified version of the BatteryElectroChemEOD model by `Gina Sierra et al. <https://www.sciencedirect.com/science/article/abs/pii/S0951832018301406>`__ first introduced in the `PHM Society Conference ProgPy Tutorial <https://github.com/nasa/progpy/blob/master/examples/2024PHMTutorial.ipynb>`__ from November 2024. See `Included Models <https://nasa.github.io/progpy/api_ref/progpy/IncludedModels.html>`__ for details
* Support for Python3.13 (with the exception of ProgPy's data driven dependencies due to Tensorflow not yet supporting this Python version)
* Dropped support of end-of-life Python3.7 and Python3.8
* Improved “ProgPy Short Course”: A series of Jupyter Notebooks designed to help users get started with ProgPy and understand how to use it for prognostics. See https://github.com/nasa/progpy/tree/master/examples
* Various bugfixes and efficiency improvements

prog_server
************
* Support for Python3.13

Updates in v1.7.1
----------------------

progpy
**************
Hotfix fixing issue with dataset download

Updates in v1.7
----------------------

progpy
**************
* Started "ProgPy Short Course": A series of Jupyter Notebooks designed to help users get started with ProgPy and understand how to use it for prognostics. See https://github.com/nasa/progpy/tree/master/examples
* Updates to improve composite model:
   * Support setting parameters in composed models using [model].[param] format (e.g., composite_model["model1.Param1"] = 12)
   * Support adding functions to composite. Useful for simple translations 
* Prediction and Simulation event strategy. For models with multiple events can now specify if you would like prediction or simulation to end when "first" or "any" of the events are met
* Updates to parameter estimation
  * Users can now estimate nested parameters (e.g., parameters['x0']['a']) using a tuple. For example params=(('x0', 'a'), ...)
  * MSE updated to include a penalty if model becomes unstable (i.e., returns NaN) before minimum threshold. This encourages parameter estimation to converge on parameters for which the model is stable
* Tensorflow no longer installed by default (this is important for users who are space constrained). If you're using the data-driven features install ProgPy like so: pip install progpy[datadriven] or pip install -e '.[datadriven]' (if using local copy)
* Support for Python 3.12
* Removed some warnings
* Various Bugfixes and Performance optimizations

**Notes for upgrading:**
* If you're using the data-driven features install ProgPy like so: pip install progpy[datadriven] or pip install -e '.[datadriven]' (if using local copy)
* Use "events" keyword instead of "threshold_keys" in simulation

prog_server
**************
* Add support for custom model, state_estimator, and predictor
* New output and output prediction endpoints
* Various bug fixes and optimizations

Updates in v1.6
----------------------

progpy
**************
* Combined previous prog_models and prog_algs packages into a single package, progpy.
* Added new :py:class:`progpy.MixtureOfExpertsModel`, which combines multiple models of the same system into a single model, where only the best of the comprised models will be used at each timestep.
* Added ability to set random seed in :py:class:`progpy.loading.GaussianNoiseWrapper`, allowing for repeatable experiments
* Various bug fixes and performance improvements

Upgrading from v1.5
^^^^^^^^^^^^^^^^^^^^^^
v1.6 combined prog_models and prog_algs into a single package progpy. To upgrade to 1.6, you will need to download the new progpy package (pip install progpy) and update all imports to use progpy. For example `from prog_models import PrognosticsModel` becomes `from progpy import PrognosticsModel`, and `from prog_algs import predictors` becomes `from progpy import predictors`.

prog_server
************
* Updated to work with progpy v1.6

Updates in V1.5
-----------------------

prog_models
***************
* **Direct Models**: Added support for new model type: Direct Models. Direct Models directly map current state and future load to time of event, rather than state-transition models which simulate forward to calculate time of event. They're created by implementing the :py:meth:`prog_models.PrognosticsModel.time_of_event`.
* New model types that combine multiple models. See `06. Combining Models <https://github.com/nasa/prog_models/blob/master/examples/06_Combining Models.ipynb>`__ for example of use. 

  * **Ensemble Model**: Combinations of multiple models of the same system where results are aggregated.
  * **Composite Model**: Combinations of models of different systems that are interdependent.

* **New Model Type**: Aircraft flight model interface, :py:class:`prog_models.models.aircraft_model.AircraftModel`. Anticipated prognostics applications with the aircraft flight model include estimating and predicting loading of other aircraft systems (e.g., powertrain) and safety metrics.
* New Model: Small Rotorcraft AircraftModel.
* New DataModel: Polynomial Chaos Expansion (PCE) Direct Surrogate Model (:py:class:`prog_models.data_models.PolynomialChaosExpansion`). See `chaos example <https://github.com/nasa/prog_models/blob/master/examples/pce.py>`__ for example of use.
* Started transition of InputContainers, StateContainers, OutputContainer and SimResult to use Pandas DataFrames. This release will bring the interface more in compliance with DataFrames. v1.6 will fully transition the classes to DataFrames.
* Implemented new metrics that can be used in :py:meth:`prog_models.PrognosticsModel.calc_error`: Root Mean Square Error (RMSE), Maximum Error (MAX_E), Mean Absolute Error (MAE), Mean Absolute Percentage Error (MAPE), and Dynamic Time Warping (DTW)
* Error calculation metric (above) can now be set when calling :py:meth:`prog_models.PrognosticsModel.estimate_params`
* Reworked integration methods in simulation

  * New integration methods: RK4 and methods from scipy.integrate
  * Integration can now be set at the model level. For continuous models the specified integration method will apply when calling next_state

* Python3.11 support
* Various bug fixes and performance improvements

prog_algs
**********
* Integration method can now be set for state estimation and prediction by setting model.parameters[‘integration_method’].
* Minimum time step can now be set in state estimation, using the argument 'dt'. This is useful for models that become unstable with large time steps.
* Python3.11 support

prog_server
************
* Python3.11 support

Updates in V1.4
-----------------------

prog_models
**************
* **Data-Driven Models**

  * Created new :py:class:`prog_models.data_models.DataModel` class as interface/superclass for all data-driven models. Data-driven models are interchangeable in use (e.g., simulation, use with prog_algs) with physics-based models. DataModels can be trained using data (:py:meth:`prog_models.data_models.DataModel.from_data`), or an existing model (:py:meth:`prog_models.data_models.DataModel.from_model`)
  * Introduced new LSTM State Transition DataModel (:py:class:`prog_models.data_models.LSTMStateTransitionModel`). 
  * DMD model (:py:class:`prog_models.data_models.DMDModel`) updated to new data-driven model interface. Can now be created from data as well as an existing model
  * Added ability to integrate training noise to data for DMD Model (:py:class:`prog_models.data_models.DMDModel`)

* **New Model**: Single-Phase DC Motor (:py:class:`prog_models.models.DCMotorSP`)
* Added the ability to select integration method when simulating (see ``integration_method`` keywork argument for :py:func:`prog_models.PrognosticsModel.simulate_to_threshold`). Current options are Euler and RK4
* New feature allowing serialization of model parameters as JSON. See :py:meth:`prog_models.PrognosticsModel.to_json`, :py:meth:`prog_models.PrognosticsModel.from_json`, and serialization example
* Added automatic step size feature in simulation. When enabled, step size will adapt to meet the exact save_pts and save_freq. Step size range can also be bounded
* New Example Model: Simple Paris' Law (:py:class:`prog_models.models.ParisLawCrackGrowth`)
* Added ability to set bounds when estimating parameters (See :py:meth:`prog_models.PrognosticsModel.estimate_params`)
* Initialize method is now optional
* Various bug fixes and performance improvements

prog_algs
**********
* Added new :py:class:`prog_algs.predictors.ToEPredictionProfile` Metric: Monotonicity. See :py:func:`prog_algs.predictors.ToEPredictionProfile.monotonicity`
* Updated to support prog_models v1.4
* Various bug fixes and performance improvements

prog_server and prog_client
****************************
* Added new endpoint (GET /api/v1/session/{id}/model) and client function (:py:meth:`prog_client.Session.get_model`) to get the model from the server.
* Updated to support prog_models and prog_algs v1.4
* Various bug fixes and performance improvements

Updates in V1.3
-----------------------

prog_models
**************
* **Surrogate Models** Added initial draft of new feature to generate surrogate models automatically from :class:`prog_models.PrognosticsModel`. Initial implementation uses Dynamic Mode Decomposition. Additional Surrogate Model Generation approaches will be explored for future releases. [Developed by NASA's DRF Project]
* **New Example Models** Added new :class:`prog_models.models.DCMotor`, :class:`prog_models.models.ESC`, and :class:`prog_models.models.Powertrain` models [Developed by NASA's SWS Project]
* **Datasets** Added new feature that allows users to access prognostic datasets programmatically
* Added new :class:`prog_models.LinearModel` class - Linear Prognostics Models can be represented by a Linear Model. Similar to PrognosticsModels, LinearModels are created by subclassing the LinearModel class. Some algorithms will only work with Linear Models.
* Added new StateContainer/InputContainer/OutputContainer objects for classes which allow for data access in matrix form and enforce expected keys. 
* Added new metric for SimResult: :py:func:`prog_models.sim_result.SimResult.monotonicity`.
* :py:func:`prog_models.sim_result.SimResult.plot` now automatically shows legends
* Added drag to :class:`prog_models.models.ThrownObject` model, making the model non-linear. Degree of nonlinearity can be effected using the model parameters (e.g., coefficient of drag cd).
* `observables` from previous releases are now called `performance_metrics`
* model.simulate_to* now returns named tuple, allowing for access by property name (e.g., result.states)
* Updates to :class:`prog_models.sim_result.SimResult` and :class:`prog_models.sim_result.LazySimResult` for robustness
* Various performance improvements and bug fixes

.. :note::

    Now input, states, and output should be represented by model.InputContainer, StateContainer, and OutputContainer, respectively

.. :note::

    Python 3.6 is no longer supported.

prog_algs
**********
* **New State Estimator Added** :class:`prog_algs.state_estimators.KalmanFilter`. Works with models derived from :class:`prog_models.LinearModel`.
* **New Predictor Added** :class:`prog_algs.predictors.UnscentedTransformPredictor`.
* Initial state estimate (x0) can now be passed as `UncertainData` to represent initial state uncertainty.
* Added new metrics for :class:`prog_algs.predictors.ToEPredictionProfile`: Prognostics horizon, Cumulative Relative Accuracy (CRA).
* Added ability to plot :class:`prog_algs.predictors.ToEPredictionProfile`: profile.plot().
* Added new metric for :class:`prog_algs.predictors.Prediction`: Monotonicity, Relative Accuracy (RA)
* Added new metric for :class:`prog_algs.uncertain_data.UncertainData` (and subclasses): Root Mean Square Error (RMSE)
* Added new describe method for :class:`prog_algs.uncertain_data.UncertainData` (and subclasses)
* Add support for python 3.10
* Various performance improvements and bugfixes

prog_server
************
* Added ability to set state using pickled prog_algs.uncertain_data.UncertainData type

prog_client
************
* Added new set_state method

Updates in V1.2
------------------------

prog_models
**************
* New Feature: Vectorized Models
    * Distributed models were vectorized to support vectorized sample-based prognostics approaches
* New Feature: Dynamic Step Sizes
    * Now step size can be a function of time or state
    * See `examples.dynamic_step_size` for more information
* New Feature: New method model.apply_bounds
    * This method allows for other classes to use applied bound limits
* Simulate_to* methods can now specify initial time. Also, outputs are now optional
* Various bug fixes

prog_algs
**************

.. :note::

    This release includes changes to the return format of the MonteCarlo Predictor's `predict` method. These changes were necessary to support non-sample based predictors. The non backwards-compatible changes are listed below:

    * times: 
        * previous ```List[List[float]]``` where times[n][m] corresponds to timepoint m of sample n. 
        * new ```List[float]``` where times[m] corresponds to timepoint m for all samples.
    * End of Life (EOL)/ Time of Event (ToE) estimates:
        * previous ```List[float]``` where the times correspond to the time that the first event occurs.
        * new ```UnweightedSamples``` where keys correspond to the individual events predicted.
    * State at time of event (ToE).
    * previous: element in states.
    * new: member of ToE structure (e.g., ToE.final_state['event1']).

* New Feature: Histogram and Scatter Plot of UncertainData.
* New Feature: Vectorized particle filter.
    * Particle Filter State Estimator is now vectorized for vectorized models - this significantly improves performance.
* New Feature: Unscented Transform Predictor.
    * New predictor that propogates sigma points forward to estimate time of event and future states.
* New Feature: `Prediction` class to represent predicted future values.
* New Feature: `ToEPredictionProfile` class to represent and operate on the result of multiple predictions generated at different prediction times.
* Added metrics `percentage_in_bounds` and `metrics` and plots to UncertainData .
* Add support for Python3.9.
* General Bugfixes.

Updates in V1.1
------------------------

prog_models
**************
* New Feature: Derived Parameters
    * Users can specify callbacks for parameters that are defined from others. These callbacks will be called when the dependency parameter is updated.
    * See `examples.derived_params` for more information.
* New Feature: Parameter Estimation
    * Users can use the estimate_parameters method to estimate all or select parameters. 
    * see `examples.param_est`
* New Feature: Automatic Noise Generation
    * Now noise is automatically generated when next_state/dx (process_noise) and output (measurement_noise). This removed the need to explicitly call apply_*_noise functions in these methods. 
    * See `examples.noise` for more details in setting noise
    * For any classes users created using V1.0.*, you should remove any call to apply_*_noise functions to prevent double noise application. 
* New Feature: Configurable State Bounds
    * Users can specify the range of valid values for each state (e.g., a temperature in celcius would have to be greater than -273.15 - absolute zero)
* New Feature: Simulation Result Class
    * Simulations now return a simulation result object for each value (e.g., output, input, state, etc) 
    * These simulation result objects can be used just like the previous lists. 
    * Output and Event State are now "Lazily Evaluated". This speeds up simulation when intermediate states are not printed and these properties are not used
    * A plot method has been added directly to the class (e.g., `event_states.plot()`)
* New Feature: Intermediate Result Printing
    * Use the print parameter to enable printing intermediate results during a simulation 
    * e.g., `model.simulate_to_threshold(..., print=True)`
    * Note: This slows down simulation performance
* Added support for python 3.9
* Various bug fixes

ElectroChemistry Model Updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* New Feature: Added thermal effects. Now the model include how the temperature is effected by use. Previous implementation only included effects of temperature on performance.
* New Feature: Added `degraded_capacity` (i.e., EOL) event to model. There are now three different models: BatteryElectroChemEOL (degraded_capacity only), BatteryElectroChemEOD (discharge only), and BatteryElectroChemEODEOL (combined). BatteryElectroChem is an alias for BatteryElectroChemEODEOL. 
* New Feature: Updated SOC (EOD Event State) calculation to include voltage when near V_EOD. This prevents a situation where the voltage is below lower bound but SOC > 0. 

CentrifugalPump Model Updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* New Feature: Added CentrifugalPumpBase class where wear rates are parameters instead of part of the state vector. 
    * Some users may use this class for prognostics, then use the parameter estimation tool occasionally to update the wear rates, which change very slowly.
* Bugfix: Fixed bug where some event states were returned as negative
* Bugfix: Fixed bug where some states were saved as parameters instead of part of the state. 
* Added example on use of CentrifugalPump Model (see `examples.sim_pump`)
* Performance improvements

PneumaticValve Model Updates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* New Feature: Added PneumaticValveBase class where wear rates are parameters instead of part of the state vector. 
    * Some users may use this class for prognostics, then use the parameter estimation tool occasionally to update the wear rates, which change very slowly.
* Added example on use of PneumaticValve Model (see `examples.sim_valve`)

