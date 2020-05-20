
"""
Widgets and functions to use in Nernst Workbook
(Initially created in-notebook, to be called here as functions)
Created on Thu May 14 18:36:59 2020
@author: hurtd

Writing the back-end of ipy widgets here, to be used in the
    Functional Jupyter Notebook for Project BattChem
    (The one to be deployed online)
    So that it mostly contains Descriptive Markdown and Interactive Bits.
    (There will be a "Math and Customization" section at the end)

For now though, Create and use widgets in the
    "Status and Exploration" Workbook
    (Which is also used for testing Binder Online)
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import copy  # Used for copy.deepcopy, to NOT DAMAGE THE RAW LIBRARIES.
import ipywidgets as widgets

import nernst_reference


