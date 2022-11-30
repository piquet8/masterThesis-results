# masterThesisProject-Piquet

This repository contains most of the material and tools used and implemented during my thesis project.

The tool implemented for converting log files into traces and later into samples is the [traceGenerator](https://github.com/piquet8/masterThesisProject-Piquet/blob/main/traceGenerator.py) script for which there is a dedicated repository with related documentation [here](https://github.com/piquet8/TraceGenerator_Script).

A version of the same tool that allows, however, to obtain uncompressed traces to allow comparison between files was implemented and provided [traceGeneratorNotComp](https://github.com/piquet8/masterThesisProject-Piquet/blob/main/traceGeneratorNotComp.py).

The three folders [R1-experiments](https://github.com/piquet8/masterThesisProject-Piquet/tree/main/R1-experiments), [RAL-simulation](https://github.com/piquet8/masterThesisProject-Piquet/tree/main/RAL-simulation) and [tour-guide-robot_simulation](https://github.com/piquet8/masterThesisProject-Piquet/tree/main/tour-guide-robot_simulation) contain within them three other folders containing: 
- the log files obtained from the experiments with the different approache (here you can see videos of the different experiments: [RAL-simulation-experiments](https://www.youtube.com/watch?v=dSbK80kEZ0k), [tour-guide-robot_simulation-experiments](https://www.youtube.com/watch?v=8L_4tDIS1Gs) and [R1-experiments](https://www.youtube.com/watch?v=qedEZL8t7cs))
- the folders of traces obtained from the log files through the use of the implemented tool
- the samples composed of the traces obtained through the use of the implemented tool

For the results obtained in the section of the thesis on comparing compressed and uncompressed files, the files used are: 
- [test.txt](https://github.com/piquet8/masterThesisProject-Piquet/blob/main/test.txt) to compare the difference between a compressed and an uncompressed track
- [RAL1](https://github.com/piquet8/masterThesisProject-Piquet/blob/main/RAL-simulation/samples/RAL1.json) and [RAL_sample_notComp](https://github.com/piquet8/masterThesisProject-Piquet/blob/main/RAL-simulation/samples/RAL_sample_notComp.json) for comparison between a sample obtained from compressed traces and one obtained from uncompressed traces

To obtain the solutions seen in the thesis using the IIT solver, you can use the samples contained in the sample folders (or you can generate the samples from the log files using the traceGenerator tool) and use the tool that you find, with its documentation, here: [learn_LTL](https://github.com/EnricoGhiorzi/learn_ltl.git).


