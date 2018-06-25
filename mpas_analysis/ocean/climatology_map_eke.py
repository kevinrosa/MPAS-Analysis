# Copyright (c) 2018,  Los Alamos National Security, LLC (LANS)
# and the University Corporation for Atmospheric Research (UCAR).
#
# Unless noted otherwise source code is licensed under the BSD license.
# Additional copyright and license information can be found in the LICENSE file
# distributed with this code, or at http://mpas-dev.github.com/license.html
#
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import xarray as xr
import datetime

from mpas_analysis.shared import AnalysisTask

from mpas_analysis.shared.io.utility import build_config_full_path

from mpas_analysis.shared.climatology import RemapMpasClimatologySubtask, \
    RemapObservedClimatologySubtask

from mpas_analysis.ocean.plot_climatology_map_subtask import \
    PlotClimatologyMapSubtask

from mpas_analysis.shared.grid import LatLonGridDescriptor


class ClimatologyMapEKE(AnalysisTask):  # {{{
    """
    An analysis task for comparison of eddy kinetic energy (eke) against
    observations
    """
    # Authors
    # -------
    # Luke Van Roekel, Xylar Asay-Davis, Milena Veneziani, Kevin Rosa

    def __init__(self, config, mpasClimatologyTask,
                 refConfig=None):  # {{{
        """
        Construct the analysis task.

        Parameters
        ----------
        config :  ``MpasAnalysisConfigParser``
            Configuration options

        mpasClimatologyTask : ``MpasClimatologyTask``
            The task that produced the climatology to be remapped and plotted

        refConfig :  ``MpasAnalysisConfigParser``, optional
            Configuration options for a reference run (if any)
        """
        # Authors
        # -------
        # Xylar Asay-Davis, Kevin Rosa

        fieldName = 'eke'
        # call the constructor from the base class (AnalysisTask)
        super(ClimatologyMapEKE, self).__init__(
                config=config, taskName='climatologyMapEKE',
                componentName='ocean',
                tags=['climatology', 'horizontalMap', fieldName, 'publicObs'])

        mpasFieldName = 'timeMonthly_avg_velocityZonal'
        iselValues = {'nVertLevels': 0}

        sectionName = self.taskName

        # read in what seasons we want to plot
        seasons = config.getExpression(sectionName, 'seasons')
        
        # EKE observations are annual climatology so only accept annual climatology
        if seasons != ['ANN']:
            raise ValueError('config section {} does not contain valid list '
                             'of seasons. For EKE, may only request annual '
                             'climatology'.format(sectionName))

        comparisonGridNames = config.getExpression(sectionName,
                                                   'comparisonGrids')

        if len(comparisonGridNames) == 0:
            raise ValueError('config section {} does not contain valid list '
                             'of comparison grids'.format(sectionName))

        # the variable mpasFieldName will be added to mpasClimatologyTask
        # along with the seasons.
        remapClimatologySubtask = RemapMpasClimatologySubtask(
            mpasClimatologyTask=mpasClimatologyTask,
            parentTask=self,
            climatologyName=fieldName,
            variableList=[mpasFieldName],
            comparisonGridNames=comparisonGridNames,
            seasons=seasons,
            iselValues=iselValues)

        if refConfig is None:

            refTitleLabel = \
                'Observations (Surface Current Variance from Drifter Data)'

            observationsDirectory = build_config_full_path(
                config, 'oceanObservations',
                '{}Subdirectory'.format(fieldName))

            obsFileName = \
                "drifter_variance.nc".format(
                    observationsDirectory)
            refFieldName = 'eke'
            outFileLabel = 'ekeDRIFTER'
            galleryName = 'Observations: Current Variance from Drifters'

            remapObservationsSubtask = RemapObservedEKEClimatology(
                    parentTask=self, seasons=seasons, fileName=obsFileName,
                    outFilePrefix=refFieldName,
                    comparisonGridNames=comparisonGridNames)
            self.add_subtask(remapObservationsSubtask)
            diffTitleLabel = 'Model - Observations'

        else:
            remapObservationsSubtask = None
            refRunName = refConfig.get('runs', 'mainRunName')
            galleryName = None
            refTitleLabel = 'Ref: {}'.format(refRunName)

            refFieldName = mpasFieldName
            outFileLabel = 'eke'
            diffTitleLabel = 'Main - Reference'

        for comparisonGridName in comparisonGridNames:
            for season in seasons:
                # make a new subtask for this season and comparison grid
                subtask = PlotClimatologyMapSubtask(self, season,
                                                    comparisonGridName,
                                                    remapClimatologySubtask,
                                                    remapObservationsSubtask,
                                                    refConfig)

                subtask.set_plot_info(
                        outFileLabel=outFileLabel,
                        fieldNameInTitle='EKE',
                        mpasFieldName=mpasFieldName,
                        refFieldName=refFieldName,
                        refTitleLabel=refTitleLabel,
                        diffTitleLabel=diffTitleLabel,
                        unitsLabel=r'cm$^2$/s$^2$',
                        imageCaption='Mean Surface Eddy Kinetic Energy',
                        galleryGroup='Eddy Kinetic Energy',
                        groupSubtitle=None,
                        groupLink='eke',
                        galleryName=galleryName)

                self.add_subtask(subtask)
        # }}}
    # }}}


class RemapObservedEKEClimatology(RemapObservedClimatologySubtask):  # {{{
    """
    A subtask for reading and remapping EKE observations
    """
    # Authors
    # -------
    # Luke Van Roekel, Xylar Asay-Davis, Milena Veneziani

    def get_observation_descriptor(self, fileName):  # {{{
        '''
        get a MeshDescriptor for the observation grid

        Parameters
        ----------
        fileName : str
            observation file name describing the source grid

        Returns
        -------
        obsDescriptor : ``MeshDescriptor``
            The descriptor for the observation grid
        '''
        # Authors
        # -------
        # Xylar Asay-Davis

        # create a descriptor of the observation grid using the lat/lon
        # coordinates
        obsDescriptor = LatLonGridDescriptor.read(fileName=fileName,
                                                  latVarName='Lat',
                                                  lonVarName='Lon')
        return obsDescriptor  # }}}

    def build_observational_dataset(self, fileName):  # {{{
        '''
        read in the data sets for observations, and possibly rename some
        variables and dimensions

        Parameters
        ----------
        fileName : str
            observation file name

        Returns
        -------
        dsObs : ``xarray.Dataset``
            The observational dataset
        '''
        # Authors
        # -------
        # Xylar Asay-Davis

        sectionName = self.taskName
        '''
        climStartYear = self.config.getint(sectionName, 'obsStartYear')
        climEndYear = self.config.getint(sectionName, 'obsEndYear')
        timeStart = datetime.datetime(year=climStartYear, month=1, day=1)
        timeEnd = datetime.datetime(year=climEndYear, month=12, day=31)
        '''
        dsObs = xr.open_dataset(fileName)
        dsObs.rename({'Up2bar': 'eke'}, inplace=True)
        '''
        dsObs.rename({'time': 'Time', 'EKE': 'eke'}, inplace=True)
        dsObs = dsObs.sel(Time=slice(timeStart, timeEnd))
        dsObs.coords['month'] = dsObs['Time.month']
        dsObs.coords['year'] = dsObs['Time.year']
        '''
        return dsObs  # }}}

    # }}}

# vim: foldmethod=marker ai ts=4 sts=4 et sw=4 ft=python
