# Control of Multi-Agent Environment

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Results](#results)
- [Run the Project](#run-the-project)
- [Other Section](#other-section)
- [Bibliography](#bibliography)

---

## Overview
This section provides a brief introduction to the project conducted as part of the Advanced Control Methods course at Skoltech in 2024. It includes the fundamental objectives of the project, information about the team members, and a link to the final presentation.

- Course: Advanced Control Methods, Skoltech, 2024
- Team Members: Muhammad Ahsan Mustafa, Yasheerah Yaqoot, Maria Makarova
- Final Presentation: https://docs.google.com/presentation/d/1EtcCFMBNPaQxWpfTwcxuKm8Jpif2VDHfXrq9SbYpOp0/edit?usp=sharing

Objectives:
- Sliding Mode Control for a Quadcopter
- Model Predictive Control for the ground locomotion of a Multi-Limb Morphogenetic UAV 'MorphoGear'

The applied controllers were coded in python and the results were verified through graphic simulations shown in the results section. After that, the controllers were tested in a Unity Environment using ROS (Robot Operating Software) to visualize the motion of the robotic vehicles. 

---

## Problem Statement
<!-- This section delves into the specifics of the challenge tackled during the project. It provides context, outlines the objectives, and discusses the significance of the problem. -->

The idea behind this project is the collaboration between two hetrogeneous vehicular robots, a UGV (Morphogear) and a UAV (quadcopter). The UGV has a landing pad attached on top of it where the UAV can land. Both the UGV and the UAV are autonomously controlled, hence they need robust cobntrollers to perform well. As stated in the objectives, a sliding mode controller was applied for the quadcopter's flight which supersedes the traditional PID control of it and an MPC was applied on MorphoGear's canter gait ground locomotion for to obtain optimised limb step lengths according to the provided path and not let it fall over. This was done so both the UAV and the UGV could accurately track given paths that were to be followed. The accuracy in this setup is crucial to the landing of the quadcopter on MorphoGear's landing pad.

![MorphoGear](https://github.com/YasheerahYaqoot/acm_project/blob/main/MorphoGear.jpg)

MorphoGear is a hexacopter with four morphogenetic limbs having 3-DoF for each limb as shown in the image above [^1]. For this project it was limited to the role of a UGV.

<!-- ### Subsection (if any)
Subsections may be added to further break down the problem, provide background information, or elaborate on specific aspects that are crucial to understanding the project's scope. -->

---

## Results
### Sliding Mode Results
### MPC Results
<!-- This is a comment -->
<!-- Detailed explanation of the findings, performance metrics, and outcomes of the project. This section may include graphs, tables, and other visual aids to support the results. -->

The following simulation shows an arbitrary trajectory which the morphogear followed. Here the varying steplengths needed according to the specific path can be seen.  
![Arbitrary Trajectory](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/72acc1fb-397f-47f9-8eb2-e71c54063f1a)

The following simulation shows how the legs of MorphoGear carry out a step generated from the MPC  
![Limbs Simulation](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/cfd34b74-b26c-403f-9f66-7c85859b7bbe)



## Unity Visualization
In the Unity simulation shown below, it can be seen that the quadcopter flies to a specific point, Morphogear then traverses to that target point through canter gait ground locomotion, and then the quadrotor lands on MorphoGear's landing pad.  
![ACMProject-ezgif com-resize (1)](https://github.com/YasheerahYaqoot/acm_project/assets/140263131/249e84a4-3856-424f-8c10-e02e8c4cdd96)

---
<!-- ### Subsection (if any)
Subsections may be used to organize results into categories, discuss different algorithms or methods used, or compare various scenarios within the project. -->

## Run the Project
### Running Sliding Mode Control
### Running MPC
- Install dependencies: `pip install casadi`
- The file `Morphogear_MPC.py` is the main run file
- `Simulation_2D.py` is used to visualize 2D xy-plane movement.
- `Walking_Simulation_2D.py` is used to visualize 2D xz-plane legs simulation.
- The two visualization files are already imported in the main run file and need not to be run. (Although all 3 files are to be saved in the same directory)
- At the end of the main run file, you have to chose which visualization you want to see.

  ---

## Bibliography
[^1]: M. Martynov, Z. Darush, A. Fedoseev, and D. Tsetserukou, “MorphoGear: An UAV with Multi-Limb Morphogenetic Gear for Rough-Terrain Locomotion,” in 2023 IEEE/ASME International Conference on Advanced Intelligent Mechatronics (AIM), Seattle, WA, USA: IEEE, Jun. 2023, pp. 11–16. doi: 10.1109/AIM46323.2023.10196115.
