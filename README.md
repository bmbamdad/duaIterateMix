# duaIterateMix
A Multiclass simulation-based traffic assignment model for mixed traffic flow of connected and autonomous vehicles and human-driven vehicles. 

duaIterateMix.py is a traffic assignment tool that helps you to solve the traffic assignment problem in the mix traffic condition (mix flow of Connected and Autonomous Vehicles (CAVs) and Human Driven Vehicles (HDVs)). This tool is based on the duaIterate.py. (https://github.com/eclipse/sumo/tree/main/tools/assign) 
It is assumed that HDVs follow user equilibrium and CAVs follow system optimal.  

Instruction:
1- The travel demand file should be split into two parts (CAVs and HDVs) by DemandGeneratorMeso.py or DemandGeneratorMicro.py
2- open a terminal and run duaiterateMix.py with the new demand files which are generated in the previous step

An example is available in this repository.
