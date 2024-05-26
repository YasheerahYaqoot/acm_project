#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

def non_mpc_vicon_data():
    file_path = "/home/yasheerah/morphogear/catkin_ws/src/pathfinding/scripts/simulation_data/non_mpc_vicon_data.txt"
    with open(file_path, 'r') as f:
        raw_data = f.readlines()

    data = [[float(x) for x in line.strip().split(', ')] for line in raw_data]

    vx = []
    vy = []
    vz = []

    for line in data:
        vx.append(line[0])
        vy.append(line[1])
        vz.append(line[2])

    return vx, vy, vz

def mpc_vicon_data():
    file_path = "/home/yasheerah/morphogear/catkin_ws/src/pathfinding/scripts/simulation_data/mpc_vicon_data.txt"
    with open(file_path, 'r') as f:
        raw_data = f.readlines()

    data = [[float(x) for x in line.strip().split(', ')] for line in raw_data]

    vx_mpc = []
    vy_mpc = []
    vz_mpc = []

    for line in data:
        vx_mpc.append(line[0])
        vy_mpc.append(line[1])
        vz_mpc.append(line[2])

    return vx_mpc, vy_mpc, vz_mpc

def planned_path_data():
    file_path = "/home/yasheerah/morphogear/catkin_ws/src/pathfinding/scripts/simulation_data/planned_path_data.txt"
    with open(file_path, 'r') as f:
        raw_data = f.readlines()

    data = [[float(x) for x in line.strip().split(', ')] for line in raw_data]

    vx_p = []
    vy_p = []
    vz_p = []

    for line in data:
        vx_p.append(line[0])
        vy_p.append(line[1])
        vz_p.append(line[2])

    return vx_p, vy_p, vz_p

def simulation_2D(vx, vy, vx_mpc, vy_mpc , vx_p, vy_p):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(vx_p, vy_p, linewidth=2.5, label='Planned Trajectory')
    ax.plot(vx, vy, label='Morphogear Trajectory without MPC')
    ax.plot(vx_mpc, vy_mpc, label='Morphogear Trajectory with MPC')
    upper_bound = [val+0.11 for val in vy_p]
    lower_bound = [val-0.11 for val in vy_p]
    ax.plot(vx_p, upper_bound, linewidth=2.5, label='Upper Bound')
    ax.plot(vx_p, lower_bound, linewidth=2.5, label='Lower Bound')
    ax.grid()
    ax.set_xlabel('X (m)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Y (m)', fontsize=10, fontweight='bold')
    ax.set_xlim([-0.25, 4])
    ax.set_ylim([-0.25, 0.4])
    ax.tick_params(axis='both', which='major', labelsize=10, width=2, length=6, labelcolor='black')
    for axis in [ax.xaxis, ax.yaxis]:
        for tick in axis.get_major_ticks():
            tick.label.set_fontsize(10)
            tick.label.set_fontweight('bold')
    ax.legend(loc='upper left', bbox_to_anchor=(0.03, 1))
    plt.show()

def simulation_2D_MPC(vx_mpc, vy_mpc , vx_p, vy_p):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(vx_p, vy_p, label='Planned Trajectory')
    ax.plot(vx_mpc, vy_mpc, label='Morphogear Trajectory with MPC')
    ax.grid()
    ax.set_xlabel('X (m)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Y (m)', fontsize=10, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=10, width=2, length=6, labelcolor='black')
    for axis in [ax.xaxis, ax.yaxis]:
        for tick in axis.get_major_ticks():
            tick.label.set_fontsize(10)
            tick.label.set_fontweight('bold')
    ax.legend(loc='upper left', bbox_to_anchor=(0.03, 1))
    plt.show()

def simulation_3D(vx_mpc, vy_mpc ,vz_mpc, vx_p, vy_p, vz_p):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(vx_p, vy_p, vz_p, label='Planned Trajectory')
    ax.plot(vx_mpc, vy_mpc, vz_mpc, label='Morphogear Trajectory')
    ax.grid()
    ax.set_xlabel('X (m)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Y (m)', fontsize=10, fontweight='bold')
    ax.set_zlabel('Z (m)', fontsize=10, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=10, width=2, length=6, labelcolor='black')
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        for tick in axis.get_major_ticks():
            tick.label.set_fontsize(10)
            tick.label.set_fontweight('bold')
    ax.legend(loc='upper left', bbox_to_anchor=(0.15, 0.8))
    plt.show()

def error(vx, vy, x, y):
    vp = []
    for val1, val2 in zip(vx,vy):
        vp.append((val1, val2))
    n = len(vp)
    y_new = np.linspace(y[0], y[1], n)
    x_new = np.linspace(x[0], x[1], n)
    mp = []
    for val1, val2 in zip(x_new, y_new):
        mp.append((val1, val2))
    bound = 0.118
    squared_error = []
    max_error = []
    for actual, desired in zip(vp, mp):
        e_y = 0
        if actual[1] > desired[1]+bound:
            e_y = actual[1] - (desired[1]+bound)
        elif actual[1] < desired[1]-bound:
            e_y = actual[1] - (desired[1]-bound)
        if e_y != 0:
            squared_error.append(e_y**2)
            max_error.append(e_y)
    if squared_error:
        rmse = np.sqrt(np.mean(squared_error))
        me = max(max_error)
    print('RMSE: ', rmse*100, 'cm')
    print('Max Error: ', me*100, 'cm')

 

if __name__ == '__main__':
    vx, vy, vz = non_mpc_vicon_data()
    vx_mpc, vy_mpc, vz_mpc = mpc_vicon_data()
    vx_p, vy_p, vz_p = planned_path_data()
    simulation_2D(vx, vy, vx_mpc, vy_mpc , vx_p, vy_p)
    # simulation_2D_MPC(vx_mpc, vy_mpc , vx_p, vy_p)
    # simulation_3D(vx_mpc, vy_mpc ,vz_mpc, vx_p, vy_p, vz_p)
    print('---For Non-MPC trajectory---')
    error(vx, vy, vx_p, vy_p)
    print('-----For MPC trajectory-----')
    error(vx_mpc, vy_mpc, vx_p, vy_p)


