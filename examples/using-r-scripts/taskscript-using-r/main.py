import json
from ts_sdk.task.__task_script_runner import Context
import numpy as np
import rpy2.robjects as ro
import os

def use_r(input: dict, context: Context):

    # Performing calculations with R
    ro.r('y <- rnorm(10)')          # Create an y object in R
    ro.r['y']                       # get y as rpy2 object
    ro.r['y'].r_repr()              # get y as an R representation
    y_array = np.array(ro.r['y'])   # copy y to a numpy array
    print(y_array)                  # Check the console to see if it worked!

    # Using R scripts
    rscript_file = './func/r-scripts/basic-math.R'
    rscript_file_text = open(rscript_file).read()
    ro.r(rscript_file_text)