import casadi as ca
import numpy as np
from Simulation_2D import simulation_2D
from Walking_Simulation_2D import simulation_legs_2D

# -------------------Initialization
Ts = 0.2     # Sampling time
N = 10       # Prediction horizon (Prediction time is N x Ts)
tolerance = 2

X_Robot = list()
Y_Robot = list()
U_Robot = list()
tempstate = list()

Along_positive_X = False
Along_positive_Y = False
Along_negative_X = False
Along_negative_Y = False

# -------------------MorphoGear Data
theta = 45*np.pi/180      # Angle between each leg
lf = 15.4                 # length of femur
lt = 20.6                 # length of tibia
base_dia = 10             # base diameter
base_thickness = 5        # base thickness
robot_height = -31        # robot height
Morphogear_data = np.array([theta, lf, lt, base_dia, base_thickness, robot_height])

# -------------------Step length constraint
step_length_max = np.sqrt(((lf + lt)**2) - robot_height**2) - 0.9
step_length_min = -(np.sqrt(((lf + lt)**2) - robot_height**2) - 0.9)

# -------------------Defining states
x = ca.SX.sym('x')
y = ca.SX.sym('y')

states = ca.vertcat(
                    x,
                    y
                    )

n_states = states.numel()

# -------------------Defining control action
a = ca.SX.sym('a')

controls = ca.vertcat(a)

n_controls = controls.numel()

# -------------------Defining trajectories
def xy_trajectories(option):
    if option == 1:
        #--------------------Option 1 - Straight Trajectory Points
        x_values = [0, 100]
        y_values = [0, 0]
    elif option == 2:
        #--------------------Option 2 - Arbitrary Trajectory Points 1
        x_values = [0, 16, 16, 30, 30]
        y_values = [0, 0, 38, 38, 45]
    elif option == 3:
        #--------------------Option 3 - Arbitrary Trajectory Points 2
        x_values = [0, 15, 15, -15, -15, 15]
        y_values = [0, 0, 35, 35, -35, -35]
    return x_values, y_values

trajectory_option = 3  ###-----INPUT TRAJECTORY NUMBER FROM 1 TO 3 TO BE TESTED-----###
x_values, y_values = xy_trajectories(trajectory_option)

# -------------------Initial State
x_initial = x_values[0]; y_initial = y_values[0]

for index, (x_0, y_0) in enumerate(zip(x_values, y_values)):
    
    if index == (len(x_values)-1):
        break
    
    # -------------------Target State
    x_target = x_values[index+1]; y_target = y_values[index+1]

    dx = x_target - x_initial
    dy = y_target - y_initial
    
    # -------------------Defining non-linear mapping function
    if abs(dy) > tolerance and abs(dx) <= tolerance:
        # -------------------Defining RHS Along Y-Axis
        RHS_y = ca.vertcat(
                          a*np.sin(theta) - a*np.sin(theta), 
                          a*np.cos(theta) + a*np.cos(theta)
                          )
        f = ca.Function('f', [states, controls], [RHS_y])
        if dy>0:
            Along_positive_Y = True
        elif dy<0:
            Along_negative_Y = True
    elif abs(dx) > tolerance and abs(dy) <= tolerance:
        # -------------------Defining RHS Along X-Axis
        RHS_x = ca.vertcat(
                          a*np.cos(theta) + a*np.cos(theta),
                          a*np.sin(theta) - a*np.sin(theta)
                          )
        f = ca.Function('f', [states, controls], [RHS_x])
        if dx>0:
            Along_positive_X = True
        elif dx<0:
            Along_negative_X = True
    
    # -------------------Control at each step of prediction horizon
    U = ca.SX.sym('U', n_controls, N) # rows = number of control inputs & columns = N

    # -------------------Initial state at every time step with the last two as reference states 
    P = ca.SX.sym('P', n_states+n_states) 

    # -------------------Prediction at each step of prediction horizon
    X = ca.SX.sym('X', n_states, (N+1))  # rows = number of states & columns = N+1

    # -------------------Initializing states
    X[:,0] = P[0:n_states]
    
    # -------------------Filling up states over the prediciton horizon
    for i in range(N):
        st = X[:, i]
        con = U[:, i]
        f_value = f(st, con)
        st_next = st + f_value
        X[:, i+1] = st_next

    obj = 0     # objective function
    g = []      # constraint vector 

    # -------------------Weight matrix Q
    Qx = 3
    Qy = 3
    Q = ca.diagcat(Qx, Qy)

    # -------------------Weight matrix R
    R1 = 0.2
    R = ca.diagcat(R1)

    # -------------------Cost function
    for i in range(N):
        st = X[:, i]
        con = U[:, i]
        obj = obj + (st-P[n_states:2*n_states]).T@Q@(st-P[n_states:2*n_states]) + con.T@R@con 
        
    # -------------------State constraints
    for i in range(N+1):
        g.append(X[0, i])
        g.append(X[1, i])
        
    lbg = -ca.inf
    ubg = ca.inf

    # -------------------Optimization variables
    opt_variables = ca.reshape(U, -1, 1)

    # -------------------Defining non-linear problem
    nlp_prob = {
                'f': obj,
                'x': opt_variables,
                'g': ca.vcat(g),
                'p': P
                }

    # -------------------Defining casadi optimization parameters
    solver_opts = {
                   'ipopt': {
                             'max_iter': 200,
                             'print_level': 0,
                             'acceptable_tol': 1e-8,
                             'acceptable_obj_change_tol': 1e-6
                             },
                   'print_time': 0
                   }

    # -------------------Defining solver
    solver = ca.nlpsol('solver', 'ipopt', nlp_prob, solver_opts)

    # -------------------Defining input constraints
    lbx = []
    ubx = []
    for _ in range(N):
        lbx.append(step_length_min)
        ubx.append(step_length_max)

    # -------------------Defining constraints structure for MPC
    args = {
            'x0': [],    
            'lbg': lbg,  
            'ubg': ubg,
            'lbx': lbx,
            'ubx': ubx,
            'p': []
            }

    # -------------------Defining initial values
    t0 = 0
    x0 = np.array([x_initial, y_initial]).reshape(-1, 1)
    u0 = np.zeros((N,n_controls))
    sim_time = 20

    # -------------------Defining final (reference) values
    xs = np.array([x_target, y_target]).reshape(-1, 1)

    # -------------------Running MPC
    def shift_movement(T, t0, x0, u, f):
        f_value = f(x0, u[:, 0])
        st = x0 + f_value
        t = t0 + T
        u_end = ca.horzcat(u[:, 1:], u[:, -1])
        return t, st, u_end.T

    def DM2Arr(dm):
        return np.array(dm.full())
    
    xx = []
    t = []

    xx.append(x0)
    t.append(t0)

    mpciter = 0
    xxl = []
    u_cl = []

    while (np.linalg.norm((x0-xs),2)) > tolerance and mpciter < sim_time/Ts:
        args['p'] = ca.vertcat(
                                x0,    # current state
                                xs     # target state
                                )
        args['x0'] = ca.vertcat(
                                ca.reshape(u0, n_controls*N, 1)
                                )

        sol = solver(
                      x0=args['x0'],
                      lbx=args['lbx'],
                      ubx=args['ubx'],
                      lbg=args['lbg'],
                      ubg=args['ubg'],
                      p=args['p']
                      )
        
        u_sol = ca.reshape(sol['x'], n_controls, N) 
        u_cl.append(DM2Arr(u_sol[:,0]))
        t.append(t0)
        t0, x0, u0 = shift_movement(Ts, t0, x0, u_sol, f) # To propogate the system forward
        x0 = ca.reshape(x0, -1, 1)
        xx.append(DM2Arr(x0))
        mpciter = mpciter + 1
    
    # print('-------states-------')
    for state in xx:
        X_Robot.append(state[0,0])
        Y_Robot.append(state[1,0])
    
    # print('-------control-------')
    for control in u_cl:
        U_Robot.append(control[0][0])
        tempstate.append([Along_positive_X, Along_positive_Y, Along_negative_X, Along_negative_Y])
        
    x_initial = xx[-1][0,0]
    y_initial = xx[-1][1,0]
    
    Along_positive_X = False
    Along_positive_Y = False
    Along_negative_X = False
    Along_negative_Y = False
    

# -------------------Generating Morphogear steps after obtaining optimised step lengths

def limb_association(xb1, xb2, zb1, zb2, xt1, xt2, zt1, zt2, limb, direction):
    #--------------------Positive X Direction
    if direction[0]:
        if limb == 'FL': #1
            x_values = np.concatenate((xb1[::-1], xt2[::-1], xt1[::-1], xb2[::-1]))
            z_values = np.concatenate((zb1[::-1], zt2[::-1], zt1[::-1], zb2[::-1]))
        elif limb == 'BR': #2
            x_values = np.concatenate((xb2, xt1, xt2, xb1))
            z_values = np.concatenate((zb2, zt1, zt2, zb1))
        elif limb == 'FR': #3
            x_values = np.concatenate((xt1[::-1], xb2[::-1], xb1[::-1], xt2[::-1]))
            z_values = np.concatenate((zt1[::-1], zb2[::-1], zb1[::-1], zt2[::-1]))
        elif limb == 'BL': #4
            x_values = np.concatenate((xt2, xb1, xb2, xt1))
            z_values = np.concatenate((zt2, zb1, zb2, zt1))
    #--------------------Positive Y Direction
    if direction[1]:
        if limb == 'FL':
            x_values = np.concatenate((xb1[::-1], xt2[::-1], xt1[::-1], xb2[::-1]))
            z_values = np.concatenate((zb1[::-1], zt2[::-1], zt1[::-1], zb2[::-1]))
        elif limb == 'BR':
            x_values = np.concatenate((xb2, xt1, xt2, xb1))
            z_values = np.concatenate((zb2, zt1, zt2, zb1))
        elif limb == 'FR':
            x_values = np.concatenate((xt2, xb1, xb2, xt1))
            z_values = np.concatenate((zt2, zb1, zb2, zt1))
        elif limb == 'BL':
            x_values = np.concatenate((xt1[::-1], xb2[::-1], xb1[::-1], xt2[::-1]))
            z_values = np.concatenate((zt1[::-1], zb2[::-1], zb1[::-1], zt2[::-1]))
    #--------------------Negative X Direction
    elif direction[2]:
        if limb == 'FL':
            x_values = np.concatenate((xb2, xt1, xt2, xb1))
            z_values = np.concatenate((zb2, zt1, zt2, zb1))
        elif limb == 'BR':
            x_values = np.concatenate((xb1[::-1], xt2[::-1], xt1[::-1], xb2[::-1]))
            z_values = np.concatenate((zb1[::-1], zt2[::-1], zt1[::-1], zb2[::-1]))
        elif limb == 'FR': 
            x_values = np.concatenate((xt2, xb1, xb2, xt1))
            z_values = np.concatenate((zt2, zb1, zb2, zt1))
        elif limb == 'BL':
            x_values = np.concatenate((xt1[::-1], xb2[::-1], xb1[::-1], xt2[::-1]))
            z_values = np.concatenate((zt1[::-1], zb2[::-1], zb1[::-1], zt2[::-1]))
    #--------------------Negative Y Direction
    elif direction[3]:
        if limb == 'FL':
            x_values = np.concatenate((xb2, xt1, xt2, xb1))
            z_values = np.concatenate((zb2, zt1, zt2, zb1))
        elif limb == 'BR':
            x_values = np.concatenate((xb1[::-1], xt2[::-1], xt1[::-1], xb2[::-1]))
            z_values = np.concatenate((zb1[::-1], zt2[::-1], zt1[::-1], zb2[::-1]))
        elif limb == 'FR':
            x_values = np.concatenate((xt1[::-1], xb2[::-1], xb1[::-1], xt2[::-1]))
            z_values = np.concatenate((zt1[::-1], zb2[::-1], zb1[::-1], zt2[::-1]))
        elif limb == 'BL':
            x_values = np.concatenate((xt2, xb1, xb2, xt1))
            z_values = np.concatenate((zt2, zb1, zb2, zt1))
    return x_values, z_values

def step_trajectory_generation(step_length, robot_height, limb, direction):
    if limb == 'FR' or limb == 'FL':
        x_b = np.linspace(0, step_length_max, 100)
        z_b = robot_height*np.ones_like(x_b)   
        theta = np.linspace(0, np.pi, 100)  
        r = np.linspace(0, step_length_max, 100)           
        x_t = r * np.cos(theta) + step_length_max
        z_t= robot_height + (r * np.sin(theta))
    elif limb == 'BR' or limb == 'BL':
        x_b = np.linspace(0, -step_length_max, 100)  
        z_b = robot_height*np.ones_like(x_b)   
        theta = np.linspace(0, np.pi, 100)  
        r = np.linspace(0, step_length_max, 100)           
        x_t = -(r * np.cos(theta) + step_length_max)
        z_t= robot_height + (r * np.sin(theta))
    
    scale_factor = step_length / step_length_max  
    scaling_point = x_b[50]  

    x_b = scaling_point + scale_factor * (x_b - scaling_point)
    z_b = robot_height + scale_factor * (z_b - robot_height)

    x_t = scaling_point + scale_factor * (x_t - scaling_point)
    z_t = robot_height + scale_factor * (z_t - robot_height)
    
    xb1 = x_b[:50]
    xb2 = x_b[50:]
    zb1 = z_b[:50]
    zb2 = z_b[50:]
    xt1 = x_t[:50]
    xt2 = x_t[50:]
    zt1 = z_t[:50]
    zt2 = z_t[50:]
    
    x_values, z_values = limb_association(xb1, xb2, zb1, zb2, xt1, xt2, zt1, zt2, limb, direction)
    return x_values, z_values

def inverse_kinematics(x, z, limb, lf, lt):
    cos_theta2 = ((x**2) + (z**2) - (lf**2) - (lt**2)) / (2*lf*lt)
    if limb == 'FR' or limb == 'FL':
        theta2 = -np.arccos(cos_theta2)
        theta1 = np.arctan2(z, x) - np.arctan2(lt * np.sin(theta2), lf + lt * np.cos(theta2))
    elif limb =='BR' or limb == 'BL':
        theta2 = np.arccos(cos_theta2)
        theta1 = np.arctan2(z, x) - np.arctan2(lt * np.sin(theta2), lf + lt * np.cos(theta2))
    return theta1, theta2

def angle_calculation(U_Robot, tempstate):
    U_Robot = np.abs(U_Robot)
    
    t1_FL = list(); t2_FL = list()
    t1_BR = list(); t2_BR = list()
    t1_FR = list(); t2_FR = list()
    t1_BL = list(); t2_BL = list()
    
    step = list()
    
    for step_length, direction in zip(U_Robot, tempstate):
        x_traj_FL, z_traj_FL = step_trajectory_generation(step_length, robot_height, 'FL', direction)
        x_traj_BR, z_traj_BR = step_trajectory_generation(step_length, robot_height, 'BR', direction)
        x_traj_FR, z_traj_FR = step_trajectory_generation(step_length, robot_height, 'FR', direction)
        x_traj_BL, z_traj_BL = step_trajectory_generation(step_length, robot_height, 'BL', direction)
        
        for x,z in zip(x_traj_FL, z_traj_FL):
            theta1, theta2 = inverse_kinematics(x, z, 'FL', lf, lt)
            t1_FL.append(theta1)
            t2_FL.append(theta2)
            
        for x,z in zip(x_traj_BR, z_traj_BR):
            theta1, theta2 = inverse_kinematics(x, z, 'BR', lf, lt)
            t1_BR.append(theta1)
            t2_BR.append(theta2)
            
        for x,z in zip(x_traj_FR, z_traj_FR):
            theta1, theta2 = inverse_kinematics(x, z, 'FR', lf, lt)
            t1_FR.append(theta1)
            t2_FR.append(theta2)
            
        for x,z in zip(x_traj_BL, z_traj_BL):
            theta1, theta2 = inverse_kinematics(x, z, 'BL', lf, lt)
            t1_BL.append(theta1)
            t2_BL.append(theta2)
            step.append(step_length)
            
    return t1_FL, t2_FL, t1_BR, t2_BR, t1_FR, t2_FR, t1_BL, t2_BL, step

t1_FL, t2_FL, t1_BR, t2_BR, t1_FR, t2_FR, t1_BL, t2_BL, step = angle_calculation(U_Robot, tempstate)


# -------------------Visualizing Plots
### Only 1 simulation can be simulated at a time. Uncomment either one plot while running code 

# -------------------Plot 1: 2D top view of motion in xy-plane
ani_2D = simulation_2D(X_Robot, Y_Robot, U_Robot, tempstate, trajectory_option, Repeat=True)

# -------------------Plot 2: 2D side view of motion in zx-plane (movement of legs)
# legs_2D = simulation_legs_2D(Morphogear_data, t1_FL, t2_FL, t1_BR, t2_BR, t1_FR, t2_FR, t1_BL, t2_BL, step, Repeat=True)
