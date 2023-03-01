import os
import sys

# this needs to happen before import pytetrad (otherwise lib cant be found)
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(BASE_DIR)

from pytetrad.util import startJVM
startJVM()

import pandas as pd
import numpy as np
import pytetrad.translate as tr

import edu.cmu.tetrad.search as ts

from causallearn.search.ConstraintBased.FCI import fci
from causallearn.utils.cit import chisq, fisherz, kci, d_separation

df = pd.read_csv(f"{BASE_DIR}/examples/resources/airfoil-self-noise.continuous.txt", sep="\t")
df = df.astype({col: "float64" for col in df.columns})

data = tr.pandas_to_tetrad(df)

print("\nCL FCI\n")
G, edges = fci(np.array(df), fisherz, 0.05)
out = str(G)
for i, col in enumerate(df.columns):
    out = out.replace(f"X{i+1}", col)
print(out)

print("\nTetrad FCI\n")
test = ts.IndTestFisherZ(data, 0.05)
tetrad_fci = ts.Fci(test)
tetrad_fci_graph = tetrad_fci.search()

print(tetrad_fci_graph)

# CL FCI
#
# Depth=3, working on node 5: 100%|██████████| 6/6 [00:00<00:00, 1104.78it/s]
# Graph Nodes:
# Frequency;Attack;Chord;Velocity;Displacement;Pressure
#
# Graph Edges:
# 1. Frequency o-> Attack
# 2. Frequency o-o Velocity
# 3. Frequency o-> Pressure
# 4. Attack <-> Chord
# 5. Velocity o-> Attack
# 6. Displacement o-> Attack
# 7. Chord o-o Displacement
# 8. Chord <-> Pressure
# 9. Velocity o-> Pressure
# 10. Displacement o-> Pressure
#
#
# Tetrad FCI
#
# new thread
# Starting BK Orientation.
# Finishing BK Orientation.
# Starting BK Orientation.
# Finishing BK Orientation.
# Graph Nodes:
# Frequency;Attack;Chord;Velocity;Displacement;Pressure
#
# Graph Edges:
# 1. Attack <-> Chord
# 2. Chord <-> Pressure
# 3. Displacement o-> Attack
# 4. Displacement o-> Chord
# 5. Displacement o-> Pressure
# 6. Frequency o-> Attack
# 7. Frequency o-> Pressure
# 8. Frequency o-o Velocity
# 9. Velocity o-> Attack
# 10. Velocity o-> Pressure
#
# NOTE: The CL result is missing one R3 rule application according to Tetrad
# Tetrad verbose output:
# "Orienting edge (R3: Double triangle): Displacement o-> Chord"