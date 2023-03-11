import jpype
import jpype.imports

try:
   jpype.startJVM(classpath=[f"resources/tetrad-gui-current-launch.jar"])
except OSError:
    print("JVM already started")

# Note: This is an example of how to write an algcomparison script to do algorithm
# comparison in Tetrad. It may not be the best example yet, but it does make
# clear how the script can be written. JR 2023-02-27

from edu.cmu.tetrad.util import Params, Parameters

from edu.cmu.tetrad.algcomparison import Comparison
from edu.cmu.tetrad.algcomparison.algorithm import Algorithms
from edu.cmu.tetrad.algcomparison.simulation import Simulations
import edu.cmu.tetrad.algcomparison.simulation as sim
import edu.cmu.tetrad.algcomparison.score as score
import edu.cmu.tetrad.algcomparison.graph as graph
import edu.cmu.tetrad.algcomparison.independence as ind
import edu.cmu.tetrad.algcomparison.statistic as stat
import edu.cmu.tetrad.algcomparison.algorithm.oracle.pag as pag

# df = pd.read_csv(f"{BASE_DIR}/examples/resources/airfoil-self-noise.continuous.txt", sep="\t")
# df = df.astype({col: "float64" for col in df.columns})

params = Parameters()
params.set(Params.ALPHA, 1e-5, 0.0001, 0.001, 0.01, 0.1)
params.set(Params.PENALTY_DISCOUNT, 1, 2, 4)

params.set(Params.SAMPLE_SIZE, 1000, 10000)
params.set(Params.NUM_MEASURES, 30)
params.set(Params.AVG_DEGREE, 6)
params.set(Params.NUM_LATENTS, 8)
params.set(Params.RANDOMIZE_COLUMNS, True)
params.set(Params.COEF_LOW, 0)
params.set(Params.COEF_HIGH, 1)
params.set(Params.VAR_LOW, 1)
params.set(Params.VAR_HIGH, 3)
params.set(Params.VERBOSE, False)

params.set(Params.NUM_RUNS, 10)

params.set(Params.BOSS_ALG, 1)
params.set(Params.DEPTH, -1)
params.set(Params.MAX_PATH_LENGTH, 2)
params.set(Params.COMPLETE_RULE_SET_USED, True)
params.set(Params.POSSIBLE_DSEP_DONE, True)
params.set(Params.DO_DISCRIMINATING_PATH_TAIL_RULE, True)

# Flags
params.set(Params.GRASP_USE_RASKUTTI_UHLER, False)
params.set(Params.GRASP_USE_SCORE, True)
params.set(Params.GRASP_USE_DATA_ORDER, True)
params.set(Params.NUM_STARTS, 1)

# default
params.set(Params.SEM_GIC_RULE, 4)
params.set(Params.SEM_BIC_STRUCTURE_PRIOR, 3)

params.set(Params.DIFFERENT_GRAPHS, True)

params.set(Params.ADD_ORIGINAL_DATASET, False)

score = score.SemBicScore()
test = ind.FisherZ()

algorithms = Algorithms()

algorithms.add(pag.Fci(test))
algorithms.add(pag.Rfci(test))
algorithms.add(pag.GFCI(test, score))
algorithms.add(pag.BFCI(test, score))
algorithms.add(pag.LVSWAP_1(test, score))
algorithms.add(pag.LVSWAP_2a(test, score))
algorithms.add(pag.LVSWAP_2b(test, score))

simulations = Simulations()
simulations.add(sim.SemSimulation(graph.RandomForward()))

statistics = stat.Statistics()
statistics.add(stat.LegalPag())
statistics.add(stat.NoAlmostCyclicPathsCondition())
statistics.add(stat.NoAlmostCyclicPathsInMagCondition())
statistics.add(stat.NoAlmostCyclicPathsInMagCondition())
statistics.add(stat.NoCyclicPathsInMagCondition())
statistics.add(stat.MaximalityCondition())

statistics.add(stat.ParameterColumn(Params.ALPHA))
statistics.add(stat.ParameterColumn(Params.PENALTY_DISCOUNT))
statistics.add(stat.ParameterColumn(Params.SAMPLE_SIZE))
statistics.add(stat.ParameterColumn(Params.DEPTH))
statistics.add(stat.ParameterColumn(Params.ZS_RISK_BOUND))
statistics.add(stat.ParameterColumn(Params.EBIC_GAMMA))

statistics.add(stat.LegalPag())
statistics.add(stat.NumDirectedEdges())
statistics.add(stat.TrueDagPrecisionTails())
statistics.add(stat.TrueDagPrecisionArrow())
statistics.add(stat.NumDirectedShouldBePartiallyDirected())
statistics.add(stat.NumDirectedEdges())
statistics.add(stat.TrueDagPrecisionTails())
statistics.add(stat.NumDirectedShouldBePartiallyDirected())
statistics.add(stat.NumDirectedEdges())
statistics.add(stat.NumBidirectedEdgesEst())
statistics.add(stat.BidirectedLatentPrecision())

statistics.add(stat.AncestorPrecision())
statistics.add(stat.AncestorRecall())
statistics.add(stat.AncestorF1())
statistics.add(stat.SemidirectedPrecision())
statistics.add(stat.SemidirectedRecall())
statistics.add(stat.SemidirectedPathF1())
statistics.add(stat.NoSemidirectedPrecision())
statistics.add(stat.NoSemidirectedRecall())
statistics.add(stat.NoSemidirectedF1())

statistics.add(stat.ElapsedCpuTime())

comparison = Comparison()
comparison.setShowAlgorithmIndices(True)
comparison.setComparisonGraph(Comparison.ComparisonGraph.true_DAG)
comparison.setParallelized(True)

comparison.compareFromSimulations("../testLvSwap", simulations, algorithms, statistics, params)
