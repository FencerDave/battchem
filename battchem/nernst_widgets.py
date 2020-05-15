
"""
Widgets and functions to use in Nernst Workbook
(Initially created in-notebook, to be called here as functions)
Created on Thu May 14 18:36:59 2020
@author: hurtd
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import copy  # Used for copy.deepcopy, to NOT DAMAGE THE RAW LIBRARIES.
import ipywidgets as widgets

import Nernst_Reference
