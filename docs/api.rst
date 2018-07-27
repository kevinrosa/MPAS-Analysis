#############
API reference
#############

This page provides an auto-generated summary of the MPAS-Analysis API. For
more details and examples, refer to the relevant chapters in the main part of
the documentation.

Top-level script: run_mpas_analysis
===================================
.. autosummary::
   :toctree: generated/

   run_mpas_analysis.build_analysis_list
   run_mpas_analysis.determine_analyses_to_generate
   run_mpas_analysis.add_task_and_subtasks
   run_mpas_analysis.update_generate
   run_mpas_analysis.run_analysis
   run_mpas_analysis.wait_for_task


Analysis tasks
==============

Base Class
----------

.. currentmodule:: mpas_analysis.shared.analysis_task

.. autosummary::
   :toctree: generated/

   AnalysisTask
   AnalysisTask.setup_and_check
   AnalysisTask.run_task
   AnalysisTask.run_after
   AnalysisTask.add_subtask
   AnalysisTask.run
   AnalysisTask.check_generate
   AnalysisTask.check_analysis_enabled
   AnalysisTask.set_start_end_date

Ocean tasks
-----------

.. currentmodule:: mpas_analysis.ocean

.. autosummary::
   :toctree: generated/

   ClimatologyMapSST
   ClimatologyMapSSS
   ClimatologyMapMLD
   ClimatologyMapSSH
   ClimatologyMapEKE
   ClimatologyMapOHCAnomaly
   ClimatologyMapAntarcticMelt
   ClimatologyMapSose
   ClimatologyMapArgoTemperature
   ClimatologyMapArgoSalinity
   IndexNino34
   MeridionalHeatTransport
   StreamfunctionMOC
   TimeSeriesOHCAnomaly
   TimeSeriesTemperatureAnomaly
   TimeSeriesSalinityAnomaly
   TimeSeriesSST
   TimeSeriesAntarcticMelt

.. currentmodule:: mpas_analysis.ocean.compute_anomaly_subtask

.. autosummary::
   :toctree: generated/

   ComputeAnomalySubtask

.. currentmodule:: mpas_analysis.ocean.plot_climatology_map_subtask

.. autosummary::
   :toctree: generated/

   PlotClimatologyMapSubtask
   PlotClimatologyMapSubtask.set_plot_info

.. currentmodule:: mpas_analysis.ocean.plot_depth_integrated_time_series_subtask

.. autosummary::
   :toctree: generated/

   PlotDepthIntegratedTimeSeriesSubtask

.. currentmodule:: mpas_analysis.ocean.plot_hovmoller_subtask

.. autosummary::
   :toctree: generated/

   PlotHovmollerSubtask


Sea ice tasks
-------------

.. currentmodule:: mpas_analysis.sea_ice

.. autosummary::
   :toctree: generated/

   ClimatologyMapSeaIceConc
   ClimatologyMapSeaIceThick
   TimeSeriesSeaIce

.. currentmodule:: mpas_analysis.sea_ice.plot_climatology_map_subtask

.. autosummary::
   :toctree: generated/

   PlotClimatologyMapSubtask
   PlotClimatologyMapSubtask.set_plot_info


Configuration
==============
.. currentmodule:: mpas_analysis.configuration

.. autosummary::
   :toctree: generated/

   MpasAnalysisConfigParser
   MpasAnalysisConfigParser.getWithDefault
   MpasAnalysisConfigParser.getExpression


Shared modules
==============

Reading MPAS Datasets
---------------------
.. currentmodule:: mpas_analysis.shared.io

.. autosummary::
   :toctree: generated/

   open_mpas_dataset

.. currentmodule:: mpas_analysis.shared.mpas_xarray

.. autosummary::
   :toctree: generated/

   mpas_xarray.open_multifile_dataset
   mpas_xarray.preprocess
   mpas_xarray.remove_repeated_time_index
   mpas_xarray.subset_variables

.. currentmodule:: mpas_analysis.shared.generalized_reader

.. autosummary::
   :toctree: generated/

   generalized_reader.open_multifile_dataset


Climatology
-----------
.. currentmodule:: mpas_analysis.shared.climatology

.. autosummary::
   :toctree: generated/

   get_comparison_descriptor
   get_antarctic_stereographic_projection
   get_remapper
   compute_monthly_climatology
   compute_climatology
   add_years_months_days_in_month
   get_unmasked_mpas_climatology_directory
   get_unmasked_mpas_climatology_file_name
   get_masked_mpas_climatology_file_name
   get_remapped_mpas_climatology_file_name

   MpasClimatologyTask
   MpasClimatologyTask.add_variables
   MpasClimatologyTask.get_file_name

   RemapMpasClimatologySubtask
   RemapMpasClimatologySubtask.get_masked_file_name
   RemapMpasClimatologySubtask.get_remapped_file_name

   RemapObservedClimatologySubtask
   RemapObservedClimatologySubtask.get_observation_descriptor
   RemapObservedClimatologySubtask.build_observational_dataset
   RemapObservedClimatologySubtask.get_file_name

Time Series
-----------
.. currentmodule:: mpas_analysis.shared.time_series

.. autosummary::
   :toctree: generated/

    cache_time_series
    compute_moving_avg_anomaly_from_start
    compute_moving_avg

    MpasTimeSeriesTask

Interpolation
-------------
.. currentmodule:: mpas_analysis.shared.interpolation

.. autosummary::
   :toctree: generated/

   Remapper

.. currentmodule:: mpas_analysis.shared.grid

.. autosummary::
   :toctree: generated/

   MpasMeshDescriptor
   LatLonGridDescriptor
   ProjectionGridDescriptor


Namelist and Streams Files
--------------------------
.. currentmodule:: mpas_analysis.shared.io.namelist_streams_interface

.. autosummary::
   :toctree: generated/

   convert_namelist_to_dict
   NameList.__init__
   NameList.__getattr__
   NameList.__getitem__
   NameList.get
   NameList.getint
   NameList.getfloat
   NameList.getbool

   StreamsFile.__init__
   StreamsFile.read
   StreamsFile.readpath
   StreamsFile.has_stream
   StreamsFile.find_stream

I/O Utilities
-------------
.. currentmodule:: mpas_analysis.shared.io

.. autosummary::
   :toctree: generated/

   utility.paths
   utility.make_directories
   utility.build_config_full_path
   utility.check_path_exists
   write_netcdf


Plotting
--------
.. currentmodule:: mpas_analysis.shared.plot

.. autosummary::
   :toctree: generated/

   plotting.timeseries_analysis_plot
   plotting.timeseries_analysis_plot_polar
   plotting.plot_polar_comparison
   plotting.plot_global_comparison
   plotting.plot_1D
   plotting.plot_vertical_section
   plotting.setup_colormap
   plotting.plot_xtick_format


Timekeeping
-----------
.. currentmodule:: mpas_analysis.shared.timekeeping

.. autosummary::
   :toctree: generated/

   utility.get_simulation_start_time
   utility.string_to_datetime
   utility.string_to_relative_delta
   utility.string_to_days_since_date
   utility.days_to_datetime
   utility.datetime_to_days
   utility.date_to_days
   MpasRelativeDelta.MpasRelativeDelta

