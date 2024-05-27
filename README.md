# Control of Multi-Agent System

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Results](#results)
- [Run the Project](#run-the-project)
- [Bibliography](#bibliography)

---

## Overview
In this project we are developing control of a Multi-Agent System. This multi-agent system consists of a novel robot MorphoGear and a quadcopter controlled with an MPC based path follower and a sliding mode based trajectory tracking respectively. 

Objectives:
- Sliding Mode Control for a Quadcopter
- Model Predictive Control for the ground locomotion of a Multi-Limb Morphogenetic UAV 'MorphoGear'

Project Framework:
- The applied controllers were coded in python and the results were verified through graphic simulations shown in the results section.
- The controllers were then tested in a Unity Environment using ROS (Robot Operating Software) to visualize the motion of the robotic vehicles. 

Course: Advanced Control Methods, Skoltech, 2024

Team Members: 
- Muhammad Ahsan Mustafa
- Yasheerah Yaqoot
- Maria Makarova

Final Presentation: https://docs.google.com/presentation/d/1EtcCFMBNPaQxWpfTwcxuKm8Jpif2VDHfXrq9SbYpOp0/edit?usp=sharing



---

## Problem Statement
<!-- This section delves into the specifics of the challenge tackled during the project. It provides context, outlines the objectives, and discusses the significance of the problem. -->

The idea behind this project is the collaboration between two hetrogeneous vehicular robots, a UGV (Morphogear) and a UAV (quadcopter). The UGV has a landing pad attached on top of it where the UAV can land. Both the UGV and the UAV are autonomously controlled, hence they need robust controllers to perform well. As stated in the objectives, a sliding mode controller was applied for the quadcopter's flight which supersedes the traditional PID control of it and an MPC was applied on MorphoGear's canter gait ground locomotion to obtain optimised limb step lengths according to the provided path and not let it fall over. 

### Importance
Without a controller, once MorphoGear deviates from its actual path then it does not tend to come back. Moreover, without a controller it can also generate a fixed step trajectory. With the MPC, the step trajectory is optimised according to the given path and keeps MorphoGear from deviating from the trajectory.

To control the quadcopter, a sliding mode controller with a backstepping approach was implemented as in [^2]. This was done so both the UAV and the UGV could accurately track given paths that were to be followed. The accuracy in this setup is crucial to the landing of the quadcopter on MorphoGear's landing pad. 

![MorphoGear](https://github.com/YasheerahYaqoot/acm_project/blob/main/MorphoGear.jpg)

MorphoGear is a hexacopter with four morphogenetic limbs having 3-DoF for each limb as shown in the image above [^1]. For this project it was limited to the role of a UGV.
The Quadcopter algorithms for Sliding Mode Control were built with the help of [^2] paper.
<!-- ### Subsection (if any)
Subsections may be added to further break down the problem, provide background information, or elaborate on specific aspects that are crucial to understanding the project's scope. -->

---

## Results
### MPC Results
<!-- This is a comment -->
<!-- Detailed explanation of the findings, performance metrics, and outcomes of the project. This section may include graphs, tables, and other visual aids to support the results. -->

The following simulation shows an arbitrary trajectory which the morphogear followed. Here the varying steplengths needed according to the specific path can be seen.  
![Arbitrary Trajectory](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/72acc1fb-397f-47f9-8eb2-e71c54063f1a)

The following simulation shows how the legs of MorphoGear carry out a step generated from the MPC. 
![Limbs Simulation](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/cfd34b74-b26c-403f-9f66-7c85859b7bbe)

The following is an error plot of MorphoGear walking in a straight line with and without MPC obtained from Unity Environment. It can be seen that a closed-loop MPC is vital because in its absence, once MorphoGear deviates from the original path it does not tend to come back.  
![Error_plot](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/937174e5-9ada-4d1f-bbfc-f5da0adf3172) 

The error values for the plot above can be seen below.  
![error_values](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/8d485c47-4994-4b1c-be0f-f9c9c347173a)
### Sliding Mode Results
The results of the trajectory approximation, as well as error graphs and resulting control laws are presented in `SlidingMode/Main.ipynb` file. 
The optimization error for the flight path is 2.08. For landing, it is 21.94.


## Unity Visualization
In the Unity simulation shown below, it can be seen that the quadcopter flies to a specific point, Morphogear then traverses to that target point through canter gait ground locomotion, and then the quadrotor lands on MorphoGear's landing pad.  
![ACM Project GIF](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/c3952a5e-bcbe-4927-9d73-9e6026e2fdb0)


---
<!-- ### Subsection (if any)
Subsections may be used to organize results into categories, discuss different algorithms or methods used, or compare various scenarios within the project. -->

## Run the Project
### Running Sliding Mode Control
- Open the `SlidingMode/Main.ipynb` file.
- Run the code until the Unity part. There are two trajectories - for flying and landing. If you need to estimate your own trajectory - inherit the class `SlidingModeControl` and change three functions: `True_traj, Solve_derivatives and Loss`. All other parameters are easy to change too. See the example of `SlidingModeControl_Grounding` class.
- Paste the file `control.cs` on the prefab of the drone in Unity.
- Press Play and wait until there is a message with the IP address. Compare it with the IP in `SlidingMode/Main.ipynb` file in Unity part.
- When the Unity environment is ready - start sending the trajectory of the quadcopter.
### Running MPC
- Install dependencies: `pip install casadi`
- The file `Morphogear_MPC/Morphogear_MPC.py` is the main run file
- `Morphogear_MPC/Simulation_2D.py` is used to visualize 2D xy-plane movement.
- `Morphogear_MPC/Walking_Simulation_2D.py` is used to visualize 2D xz-plane legs simulation.
- The two visualization files are already imported in the main run file and need not to be run. (Although all 3 files are to be saved in the same directory)
- At the end of the main run file, you have to chose which visualization you want to see.
- `MPC_Results/mpc_vicon_data.txt`, `MPC_Results/non_mpc_vicon_data.txt`, `MPC_Results/planned_path_data.txt` contain the data points obtained through Unity Simulation for a straight line trajectory. This data is used to plot the error graph using `MPC_Results/plotting_simulation.py`.

  ---

## Bibliography
[^1]: M. Martynov, Z. Darush, A. Fedoseev, and D. Tsetserukou, “MorphoGear: An UAV with Multi-Limb Morphogenetic Gear for Rough-Terrain Locomotion,” in 2023 IEEE/ASME International Conference on Advanced Intelligent Mechatronics (AIM), Seattle, WA, USA: IEEE, Jun. 2023, pp. 11–16. doi: 10.1109/AIM46323.2023.10196115.
[^2]: Bouadi, Hakim & Bouchoucha, M. & Tadjine, M.. (2007). Sliding Mode Control based on Backstepping Approach for an UAV Type-Quadrotor. International Journal of Applied Mathematics and Computer Sciences. 4. 12-17. 
