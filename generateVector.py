import vtk
import sys
import math
import random
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
base0 = [1,0,0]
base1 = [0,1,0]
base2 = [0,0,1]

baseVector = [base0,base1,base2,[-1,0,0],[0,-1,0],[0,0,-1],[1,0,0]]
value = 1/math.sqrt(3)
baseVector.append([value, value, value])
baseVector.append([-value, value, value])
baseVector.append([value, -value, value])
baseVector.append([value, value, -value])
baseVector.append([-value, -value, value])
baseVector.append([-value, value, -value])
baseVector.append([value, -value, -value])
baseVector.append([-value, -value, -value])

