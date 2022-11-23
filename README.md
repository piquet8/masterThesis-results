# masterThesis-results
This repository contains most of the material used in the course of my thesis project. 
Within the three folders you will find the log files obtained from the different experiment modes (2 in the simulated environment and 1 with the real robot).
The implemented tool traceGenerator and its documentation can be found at its dedicated repository: [traceGenerator](https://github.com/piquet8/TraceGenerator_Script.git) 
If you try the trace generator, before selecting the file(s) to convert in the first two functions you will be asked to enter the coordinates of the extremes of the map used. Below you will find the different coordinates for the experiments done:

For the RAL2022-experiments simulation the parameters are:
- a0 = -15.5
- a1 = 6.5
- b0 = -10.8
- b1 = 16.8

For the tour-guide-robot simulation, the parameters are:
- a0 = -3.4
- a1 = 64
- b0 = -19.2
- b1 = 16.9

For the R1 experiments in arena, the parameters are:
-	a0 = -5.6
-	a1 = 6.6
-	b0 = -5
-	b1 = 8.6

The last file contains the same version of the tool but produces uncompressed traces.
If you also want to try to get the solutions seen in the thesis using the iit solver find the tool and its documentation here: [learn_LTL](https://github.com/EnricoGhiorzi/learn_ltl.git)
