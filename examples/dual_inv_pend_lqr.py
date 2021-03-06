import numpy as np
import gym
from dual_inverted_pendulum_env import DualInvertedPendulumEnv
from scipy.linalg import solve_continuous_are as riccati

import autograd.numpy as anp
from autograd import jacobian

import time

def lqr(A, B, Q, R, N=None):
    # Solve Algebraic Riccati Equation
    P = riccati(A, B, Q, R, e=N)
    R_inv = np.linalg.inv(R)
    if N:
        K = np.dot(R_inv, np.dot(B.T, P) + N.T)
    else:
        K = np.dot(R_inv, np.dot(B.T, P))
    return K


env = DualInvertedPendulumEnv()
state = env.reset()

done = False

fixed_point = anp.array([0., np.pi, np.pi, 0., 0., 0., 0.])
f0, A, B = env._linearize(fixed_point)

# create cost matrices for LQR
Q = np.array([
             [1, 0, 0, 0, 0, 0], 
             [0, 1, 0, 0, 0, 0], 
             [0, 0, 1, 0, 0, 0], 
             [0, 0, 0, 100, 0, 0],
             [0, 0, 0, 0, 100, 0],
             [0, 0, 0, 0, 0, 10],
             ])
R = np.array([[0.001]])

# # Compute gain matrix K
K = lqr(A,B,Q,R)

while not done:
  env.render()
  action = -np.matmul(K, state - fixed_point[:-1])
  action = action[0]
  state, reward, done, info = env.step(action)



