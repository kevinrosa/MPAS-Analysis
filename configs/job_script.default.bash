#!/bin/bash
# This software is open source software available under the BSD-3 license.
#
# Copyright (c) 2018 Los Alamos National Security, LLC. All rights reserved.
# Copyright (c) 2018 Lawrence Livermore National Security, LLC. All rights
# reserved.
# Copyright (c) 2018 UT-Battelle, LLC. All rights reserved.
#
# Additional copyright and license information can be found in the LICENSE file
# distributed with this code, or at
# https://raw.githubusercontent.com/MPAS-Dev/MPAS-Analysis/master/LICENSE

export HDF5_USE_FILE_LOCKING=FALSE

# MPAS/ACME job to be analyzed, including paths to simulation data and
# observations. Change this name and path as needed
run_config_file="config.run_name_here"
# no prefix is needed for jobs running on a laptop or desktop computer
command_prefix=""
# change this if not submitting this script from the directory
# containing run_mpas_analysis
mpas_analysis_dir="."
# the number of parallel tasks (anything between 1 and the total number
# of tasks to run)
parallel_task_count=8
# ncclimo can run with 1 (serial) or 12 (bck) threads
ncclimo_mode=bck

if [ ! -f $run_config_file ]; then
    echo "File $run_config_file not found!"
    exit 1
fi
if [ ! -f $mpas_analysis_dir/run_mpas_analysis ]; then
    echo "run_mpas_analysis not found in $mpas_analysis_dir!"
    exit 1
fi

# This is a config file generated just for this job with the output directory,
# command prefix and parallel task count from above.
job_config_file=config.output.$RANDOM

# write out the config file specific to this job
cat <<EOF > $job_config_file
[execute]
## options related to executing parallel tasks

# the number of parallel tasks (1 means tasks run in serial, the default)
parallelTaskCount = $parallel_task_count

# the parallelism mode in ncclimo ("serial" or "bck")
# Set this to "bck" (background parallelism) if running on a machine that can
# handle 12 simultaneous processes, one for each monthly climatology.
ncclimoParallelMode = $ncclimo_mode

EOF

$command_prefix $mpas_analysis_dir/run_mpas_analysis $run_config_file \
    $job_config_file

# commend this out if you want to keep the config file, e.g. for debugging
rm $job_config_file

