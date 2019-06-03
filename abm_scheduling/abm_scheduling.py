#%%
"""
    bowtievisualization is an OpenSource python package for the analysis of
    networkx networks under the bow-tie structure analysis
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
"""

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import matplotlib.mlab as mlab
import numpy as np
import networkx as nx
import math

import time
from datetime import datetime
