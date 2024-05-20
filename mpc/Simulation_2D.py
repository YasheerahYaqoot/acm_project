import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def simulation_2D(X_Robot, Y_Robot, U_Robot, tempstate, trajectory_option, figure_number, Repeat):
    x_traj = 0
    y_traj = 0
    xpoints = []
    ypoints = []
    xpoints.append(x_traj)
    ypoints.append(y_traj)
    
    for control, state in zip(U_Robot, tempstate):
        if state[0] or state[2]:
            x_traj = x_traj +  control*np.cos(np.deg2rad(45))
            y_traj = y_traj +  control*np.sin(np.deg2rad(45))
            xpoints.append(x_traj)
            ypoints.append(y_traj)
            x_traj = x_traj +  control*np.cos(np.deg2rad(45))
            y_traj = y_traj -  control*np.sin(np.deg2rad(45))
            xpoints.append(x_traj)
            ypoints.append(y_traj)
        elif state[1] or state[3]:
            x_traj = x_traj +  control*np.sin(np.deg2rad(45))
            y_traj = y_traj +  control*np.cos(np.deg2rad(45))
            xpoints.append(x_traj)
            ypoints.append(y_traj)
            x_traj = x_traj -  control*np.sin(np.deg2rad(45))
            y_traj = y_traj +  control*np.cos(np.deg2rad(45))
            xpoints.append(x_traj)
            ypoints.append(y_traj)
    
    new_array_x = []
    new_array_y = []
    
    for i in range(len(xpoints) - 1):
        new_values = np.linspace(xpoints[i], xpoints[i + 1], 3)
        new_array_x.extend(new_values[:-1]) 
    new_array_x.append(xpoints[-1])

    for i in range(len(ypoints) - 1):
        new_values = np.linspace(ypoints[i], ypoints[i + 1], 3)
        new_array_y.extend(new_values[:-1])
    new_array_y.append(ypoints[-1])
    
    fig1 = plt.figure(figure_number)
    
    def update_plot(i):
        plt.clf()
        
        plt.plot(X_Robot, Y_Robot, label='True trajectory')
        plt.plot(new_array_x[:i+1], new_array_y[:i+1], label='MorphoGear trajectory')
        
        if trajectory_option == 1:
            plt.scatter(new_array_x[i], new_array_y[i], marker='o', color='red', s=6000)
            plt.title('Following Straight Trajectory')
            plt.xlim([-10, xpoints[-1]+30])
            plt.ylim([-15, ypoints[-1]+30])
        elif trajectory_option == 2:
            plt.scatter(new_array_x[i], new_array_y[i], marker='o', color='red', s=6000)
            plt.title('Following Arbitrary Trajectory 1')
            plt.xlim([-5, xpoints[-1]+10])
            plt.ylim([-5, ypoints[-1]+10])
        elif trajectory_option == 3:
            plt.scatter(new_array_x[i], new_array_y[i], marker='o', color='red', s=6000)
            plt.title('Following Arbitrary Trajectory 2')
            plt.xlim([-45, 45])
            plt.ylim([-45, 45])
        elif trajectory_option == 4:
            plt.scatter(new_array_x[i], new_array_y[i], marker='o', color='red')
            plt.title('Following A* Trajectory')
            plt.xlim([-10, 900])
            plt.ylim([-10, 900])
            
        plt.xlabel('X (centimeters)')
        plt.ylabel('Y (centimeters)')
        plt.legend()
        plt.grid()
        plt.gca().set_aspect('equal', adjustable='box')
        
    ani = FuncAnimation(fig1, update_plot, frames=len(new_array_x), interval=1, repeat=Repeat)
    plt.show()
    return ani
    
