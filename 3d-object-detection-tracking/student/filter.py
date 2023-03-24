# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        pass

    def F(self):
        ############
        # TODO Step 1: implement and return system matrix F
        ############

        return np.array([
            [1, 0, 0, params.dt, 0, 0],
            [0, 1, 0, 0, params.dt, 0],
            [0, 0, 1, 0, 0, params.dt],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # TODO Step 1: implement and return process noise covariance Q
        ############
        dt = params.dt
        q = params.q

        qt = dt * q
        qt2 = (dt ** 2) / 2. * q
        qt3 = (dt ** 3) / 3. * q

        return np.array([
            [qt3, 0, 0, qt2, 0, 0],
            [0, qt3, 0, 0, qt2, 0],
            [0, 0, qt3, 0, 0, qt2],
            [qt2, 0, 0, qt, 0, 0],
            [0, qt2, 0, 0, qt, 0],
            [0, 0, qt2, 0, 0, qt]
        ])
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # TODO Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############

        F = self.F()
        Q = self.Q()
        x = track.x
        P = track.P

        xtp = F @ x
        Ptp = F @ P @ F.T + Q
        
        track.set_x(xtp)
        track.set_P(Ptp)
        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # TODO Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        xtp = track.x
        Ptp = track.P

        H = meas.sensor.get_H(xtp)
        gamma = self.gamma(track, meas)
        S = self.S(track, meas, H)

        K = Ptp @ H.T @ np.linalg.inv(S)

        xt = xtp + K @ gamma
        Pt = (np.eye(params.dim_state) - K @ H) @ Ptp
        
        track.set_x(xt)
        track.set_P(Pt)
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # TODO Step 1: calculate and return residual gamma
        ############

        z = meas.z
        sensor = meas.sensor
        
        return z - sensor.get_hx(track.x)
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # TODO Step 1: calculate and return covariance of residual S
        ############

        return H @ track.P @ H.T + meas.R
        
        ############
        # END student code
        ############ 