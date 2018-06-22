## *Design Document*
# **Eddy Kinetic Energy Climatology Mapping**

#### Kevin Rosa
June 18, 2018



Table of Contents  
====================
1. [Summary](#summary)  
1. [Requirements](#requirements)  
1. [Physics](#physics)
1. [Design and Implementation](#design)
1. [Testing](#testing)
1. [Next Steps](#next)
1. [Bibliography](#bibliography)

----------------

<a name="summary"/>
# Summary

The document describes a new feature which will be added to the MPAS-Analysis
tools package: visualization of surface Eddy Kinetic Energy (EKE).
The EKE climatology map will function very similarly to other climatological fields (e.g. SSH, SST, etc.).
The output file will contain three images: the modeled EKE climatology, the observed EKE climatology, and the difference.
Plotting EKE is particularly important for MPAS-O because one can configure meshes with eddy-permitting regions and would then want to compare the EKE in these regions against observations.

<a name="requirements"/>
# Requirements

1. Model output must contain the meridional and zonal components of both `timeMonthly_avg_velocity*` and `timeMonthly_avg_velocity*Squared`.
1. User can download the EKE observations data, via 1 of 2 methods:
  - Run `./download_analysis_data.py -o /path/to/output/directory` if they wish to download all observations data.  
  *or*
  - Download only the EKE dataset at [https://web.lcrc.anl.gov/public/e3sm/diagnostics/observations/Ocean/EKE/drifter_variance.nc](https://web.lcrc.anl.gov/public/e3sm/diagnostics/observations/Ocean/EKE/drifter_variance.nc)
1. In config file...
  1. Specify `ekeSubdirectory` with location of EKE observations file.
  1. Under `[climatologyMapEKE]`, leave `seasons =  ['ANN']`.  *Only annual observations are available currently.*
  1. When setting `generate`, task `climatologyMapEKE` has tags: `climatology, horizontalMap, eke`


<a name="physics"/>
# Physics

In the ocean, it is convenient to separate the the horizontal current, *u*,
into its mean and eddy components:  
(1) <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?u=\overline{u}+u'" title="u = ubar + uprime" /></a>

This approach separates the total kinetic energy into mean kinetic energy
(MKE) and eddy kinetic energy (EKE).

The EKE over much of the ocean is at least an order of magnitude greater than
the MKE (Wytrki, 1976).
This eddy energy is important for transporting momentum, heat, mass, and chemical
constituents of seawater (Robinson, 1983).

### Algorithms

Time mean of equation 1: <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overline{u^2}=\overline{u}^2+\overline{u'^2}" title="u = ubar + uprime" /></a>

The model outputs <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overline{u}" title="ubar" /></a>
and <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overline{u^2}" title="u-squared bar" /></a>
while the observational dataset provides <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overline{u'^2}" title="u-prime-squared bar" /></a>
so two different EKE equations must be used:

(2) <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overline{EKE_{model}}=(\overline{u^2}-\overline{u}^2+\overline{v^2}-\overline{v}^2)/2" title="EKE model" /></a>

(3) <a href="" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overline{EKE_{obs}}=(\overline{u'^2}+\overline{v'^2})/2" title="EKE observations" /></a>



<a name="design"/>
# Design and Implementation
The primary design consideration for this feature is that it integrate
seamlessly with the rest of the analysis tools.
To this end, the sea surface temperature (SST) plotting tools will be used as a
template.

Files to create:
- `mpas_analysis/ocean/climatology_map_eke.py`
- `docs/tasks/climatologyMapEKE.rst`

Files to edit:
- `mpas_analysis/ocean/__init__.py`
- `docs/analysis_tasks.rst`
- `docs/api.rst`
- `mpas_analysis/config.default`

The main challenge for plotting EKE is that EKE is a function of several model variables and is not itself a variable that is directly written by the model.
Because of this, the climatology mapping functions for SSH, SST, SSS, and MLD will not serve as a direct template for the EKE formulation in `mpas_analysis/ocean/climatology_map_eke.py`.
I will try to follow the structure of `mpas_analysis/ocean/compute_transects_with_vel_mag.py` as much as possible.

# Testing

I will test runs of varying durations and resolutions to make sure the EKE plotting is working.  I will also ensure that the following jobs fail:
1. Input model results files missing at least one of the 4 necessary velocity variables.
1. Request seasonal plots.
1. 


<a name="bibliography"/>
# Bibliography
- https://latex.codecogs.com/eqneditor/editor.php
- Chelton, D. B., Schlax, M. G., Samelson, R. M. & Szoeke, R. A. de. Global observations of large oceanic eddies. Geophysical Research Letters 34, (2007).
- Laurindo, L. C., Mariano, A. J. & Lumpkin, R. An improved near-surface velocity climatology for the global ocean from drifter observations. Deep Sea Research Part I: Oceanographic Research Papers 124, 73–92 (2017).
- Wyrtki, K., Magaard, L. & Hager, James. Eddy energy in the oceans. Journal of Geophysical Research 81, 2641–2646



<!---

# TRASH
The EKE plot will not require any additional input files.
The only new concern is an oceanographic one: EKE is most relevant for  
eddy-permitting configurations of the model.  

Unlike temperature or SSH, EKE is not a field that is calculated in MPAS-O.

mpasField = (ds.timeMonthly_avg_velocityZonalSquared[0,0,:,:].values - ds.timeMonthly_avg_velocityZonal[0,0,:,:].values**2 + \
        ds.timeMonthly_avg_velocityMeridionalSquared[0,0,:,:].values - ds.timeMonthly_avg_velocityMeridional[0,0,:,:].values**2)/2.

from ncdump: `double timeMonthly_avg_velocityZonal(Time, nCells, nVertLevels)`

Calculations and spatial interpolation performed in `mpas_analysis/ocean/climatology_map_eke.py`.
Colormaps are set in `docs/tasks/climatologyMapEKE.rst` and(or?) `mpas_analysis/config.default`.  
- `config.default` doesn't specify colorbar units or title

Actual plotting is done in `mpas_analysis/shared/plot/plotting.py`.

Surface EKE only (?)

Fields to read in (specified in `mpas_analysis/config.default` and also `config.myrun`):
- `timeMonthly_avg_velocityZonal`, `timeMonthly_avg_velocityMeridional`
- `timeMonthly_avg_velocityZonalSquared`, `timeMonthly_avg_velocityMeridionalSquared`


Colorbar: range 0 to 1000 cm2/s2.
contourLevelsResult same as colorbarTicksResult (SSH it was same as colorbarLevelsResult but for SSH there were more ticks than levels -- the opposite of Luke's EKE script).

#### Where is the analysis getting the lat, lon?
e.g. in `mpaso.hist.am.timeSeriesStatsMonthly.0499-01-01`, for time it has these 3 variables:
```
int timeMonthly_counter(Time) ;
      timeMonthly_counter:units = "unitless" ;
char xtime_startMonthly(Time, StrLen) ;
      xtime_startMonthly:units = "unitless" ;
char xtime_endMonthly(Time, StrLen) ;
      xtime_endMonthly:units = "unitless" ;
```

**Answer:** it's in the rst file.


A different approach, it has total KE
```
double timeMonthly_avg_avgValueWithinOceanVolumeRegion_avgVolumeKineticEnergyCell(Time, nOceanRegionsTmp) ;
              timeMonthly_avg_avgValueWithinOceanVolumeRegion_avgVolumeKineticEnergyCell:long_name = "Average kinetic energy within region volume" ;
              timeMonthly_avg_avgValueWithinOceanVolumeRegion_avgVolumeKineticEnergyCell:units = "m^2 s^{-2}" ;
```

namelist and streams are checks for whether mpas model itself has certain analysis on (e.g. MOC).

streams specifies filenames and filepaths

Bug test: If EKE was turned on in namelist but necessary variable(s) were never written to output netcdf file.

plan
1. just get the eke to plot and leave ssh (or sst) as the observations
1. add in eke observations second

dealing with needing multiple variables from the output netcdf:
- see the climatology_map_schmidtko?

In config.default, under `[climatologyMapEKE]` set
`seasons =  ['ANN']`

For high-resolution eddy-permitting MPAS-O experiments, it is important that
researchers have tools to visualize model predictions of EKE in order to
compare the model EKE to observations.

### Explicitly resolved vs. sub-grid scale processes
Processes in the ocean occur across scales ranging from thousands of kilometers (tides and Rossby waves) to centimeters (capillary waves) and all the way down to molecular diffusion.
A wave must have a wavelength longer than 4 grid cells in order to be resolved in a numerical model so all of the small sub-grid scale processes must be parameterized.


####Lit Notes

- "...The named ocean currents, such as the Gulf Stream and the Peru Current... are the home of "rings" spun off from major currents, and they have a complex eddy structure of their own." (Knauss p.186)
- "The energy sources are varied. They include Gulf Stream rings and analogous phenomena associated with other major currents, turbulence generated by currents passing over complex bottom topography and coastal jets associate with upwelling.  The strongest eddies are found near the strong western boundary currents." (Knauss p.186)
- Wytrki 1976
  - "The results are consistent with the idea that eddy motion in the ocean is generated in areas of strong mean shear flow and is subsequently distributed over the whole ocean."
  - E_mean / E_eddy
    - Gulf stream: 2
    - Subtropical gyre: 1/20 - 1/40
- "The kinetic energy of mesoscale variability (scales of tens to hundreds of km and tens to hundreds of days) is more than an order of magnitude greater than the mean kinetic energy over most of the ocean [Wyrtki et al., 1976; Richardson, 1983]. Mesoscale variability occurs as linear Rossby waves and as nonlinear vortices or eddies. In contrast to linear waves, nonlinear vortices can transport momentum, heat, mass and the chemical constituents of seawater, and thereby contribute to the general circulation, large‐scale water mass distributions, and ocean biology [Robinson, 1983]." (Chelton 2007)

--->
