import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
    
def simulation_legs_2D(Morphogear_data, t1_FL, t2_FL, t1_BR, t2_BR, t1_FR, t2_FR, t1_BL, t2_BL, step):
    theta = Morphogear_data[0]
    lf = Morphogear_data[1]  
    lt = Morphogear_data[2]
    base_dia = Morphogear_data[3]
    base_thickness = Morphogear_data[4]
    robot_height = Morphogear_data[5]
    step_length_max = np.sqrt(((lf + lt)**2) - robot_height**2) - 0.9
    
    def base(base_dia, base_thickness):
        x_coords = [base_dia, -base_dia, -base_dia, base_dia, base_dia]
        y_coords = [0, 0, base_thickness, base_thickness, 0]
        plt.plot(x_coords, y_coords, color='black', linewidth=2)
        
    def limb_position(theta1, theta2, limb):
        if limb == 'FR' or limb == 'FL':
            femur_end_x = lf * np.cos(theta1) + base_dia
            femur_end_z = lf * np.sin(theta1)
            tibia_end_x = femur_end_x + lt * np.cos(theta1 + theta2)
            tibia_end_z = femur_end_z + lt * np.sin(theta1 + theta2)
        elif limb == 'BR' or limb == 'BL':
            femur_end_x = lf * np.cos(theta1) - base_dia
            femur_end_z = lf * np.sin(theta1)
            tibia_end_x = femur_end_x + lt * np.cos(theta1 + theta2)
            tibia_end_z = femur_end_z + lt * np.sin(theta1 + theta2)
        return femur_end_x, femur_end_z, tibia_end_x, tibia_end_z

    def step_trajectory_forward_plot(base_dia, sl):
        x_b = np.linspace(0, step_length_max, 100) + base_dia
        z_b = robot_height*np.ones_like(x_b)   
        theta = np.linspace(0, np.pi, 100)  
        r = np.linspace(0, step_length_max, 100)           
        x_t = r * np.cos(theta) + step_length_max + base_dia
        z_t= robot_height + (r * np.sin(theta))
        
        scale_factor = sl / step_length_max  
        scaling_point = x_b[50]  
        x_b = scaling_point + scale_factor * (x_b - scaling_point)
        z_b = robot_height + scale_factor * (z_b - robot_height)
        x_t = scaling_point + scale_factor * (x_t - scaling_point)
        z_t = robot_height + scale_factor * (z_t - robot_height)
        
        x_values = np.concatenate((x_b, x_t))
        z_values = np.concatenate((z_b, z_t))
        return x_values, z_values 
        
    def step_trajectory_backward_plot(base_dia, sl):
        x_b = np.linspace(0, -step_length_max, 100) - base_dia
        z_b = robot_height*np.ones_like(x_b)   
        theta = np.linspace(0, np.pi, 100)  
        r = np.linspace(0, step_length_max, 100)           
        x_t = -(r * np.cos(theta) + step_length_max) - base_dia
        z_t= robot_height + (r * np.sin(theta))
        
        scale_factor = sl / step_length_max  
        scaling_point = x_b[50]  
        x_b = scaling_point + scale_factor * (x_b - scaling_point)
        z_b = robot_height + scale_factor * (z_b - robot_height)
        x_t = scaling_point + scale_factor * (x_t - scaling_point)
        z_t = robot_height + scale_factor * (z_t - robot_height)
        
        x_values = np.concatenate((x_t, x_b))
        z_values = np.concatenate((z_t, z_b))
        return x_values, z_values 
    
    # Initialize plot
    fig, ax = plt.subplots()
    ax.set_xlim(-lf - lt - base_dia, lf + lt + base_dia)
    ax.set_ylim(-lf - lt - 0.5, 15)
    ax.set_aspect('equal')
    line_FL, = ax.plot([], [], 'o-', lw=2, label='Front Left', color='green')
    line_BR, = ax.plot([], [], 'o-', lw=2, label='Back Right', color='blue')
    line_FR, = ax.plot([], [], 'o-', lw=2, label='Front Right', color='red')
    line_BL, = ax.plot([], [], 'o-', lw=2, label='Back Left', color='purple')
    FTraj, = ax.plot([], [], lw=2, color='black')
    BTraj, = ax.plot([], [], lw=2, color='black')
    
    Femur_FL = list(); Tibia_FL = list()
    Femur_BR = list(); Tibia_BR = list()
    Femur_FR = list(); Tibia_FR = list()
    Femur_BL = list(); Tibia_BL = list()
    
    for t1, t2 in zip(t1_FL, t2_FL):
        femur_end_x, femur_end_z, tibia_end_x, tibia_end_z = limb_position(t1, t2, 'FL')
        Femur_FL.append(np.array([femur_end_x, femur_end_z]))
        Tibia_FL.append(np.array([tibia_end_x, tibia_end_z]))
        
    for t1, t2 in zip(t1_BR, t2_BR):
        femur_end_x, femur_end_z, tibia_end_x, tibia_end_z = limb_position(t1, t2, 'BR')
        Femur_BR.append(np.array([femur_end_x, femur_end_z]))
        Tibia_BR.append(np.array([tibia_end_x, tibia_end_z]))
        
    for t1, t2 in zip(t1_FR, t2_FR):
        femur_end_x, femur_end_z, tibia_end_x, tibia_end_z = limb_position(t1, t2, 'FR')
        Femur_FR.append(np.array([femur_end_x, femur_end_z]))
        Tibia_FR.append(np.array([tibia_end_x, tibia_end_z]))
        
    for t1, t2 in zip(t1_BL, t2_BL):
        femur_end_x, femur_end_z, tibia_end_x, tibia_end_z = limb_position(t1, t2, 'BL')
        Femur_BL.append(np.array([femur_end_x, femur_end_z]))
        Tibia_BL.append(np.array([tibia_end_x, tibia_end_z]))
    
    count = len(step)
        
    def update(frame, base_dia, base_thickness, Femur_FL, Tibia_FL, Femur_BR, Tibia_BR, Femur_FR, Tibia_FR, Femur_BL, Tibia_BL, step):
        # Plotting Base
        base(base_dia, base_thickness)
        
        # Plotting Foreward Left Limb
        line_FL.set_data([base_dia, Femur_FL[frame][0], Tibia_FL[frame][0]], [0, Femur_FL[frame][1], Tibia_FL[frame][1]])
        
        # Plotting Backward Right Limb
        line_BR.set_data([-base_dia, Femur_BR[frame][0], Tibia_BR[frame][0]], [0, Femur_BR[frame][1], Tibia_BR[frame][1]])
        
        # Plotting Foreward Right Limb
        line_FR.set_data([base_dia, Femur_FR[frame][0], Tibia_FR[frame][0]], [0, Femur_FR[frame][1], Tibia_FR[frame][1]])
        
        # Plotting Backward Left Limb
        line_BL.set_data([-base_dia, Femur_BL[frame][0], Tibia_BL[frame][0]], [0, Femur_BL[frame][1], Tibia_BL[frame][1]])
        
        # Plotting Right Side Trajectories
        x_values, z_values = step_trajectory_forward_plot(base_dia, step[frame])
        FTraj.set_data(x_values, z_values)
        
        # Plotting Left Side Trajectories
        x_values, z_values = step_trajectory_backward_plot(base_dia, step[frame])
        BTraj.set_data(x_values, z_values)
        
        plt.xlabel('X (centimeters)')
        plt.ylabel('Z (centimeters)')
        plt.title('Leg Motion Simulation')
        plt.legend()
        plt.grid(True)
        
        return line_FL, line_BR, line_FR, line_BL, FTraj, BTraj
    
    ani = FuncAnimation(fig, update, frames=range(count), fargs=(base_dia, base_thickness,
                  Femur_FL, Tibia_FL, Femur_BR, Tibia_BR, Femur_FR, Tibia_FR, Femur_BL, Tibia_BL, step),
                        interval=15, blit=True, repeat=True)
    return ani