import urllib
import json
import socket
import os
import time
from datetime import *
import pandas as p
import numpy as np
import scipy as sp
from scipy.stats import norm
from scipy.stats import multivariate_normal
from scipy.stats import chi2
from scipy.stats import laplace
from scipy.stats import percentileofscore
from random import randint
        
class lin_reg:
    def __init__(self,x_data,y_data,y_int):

        if type(x_data) == list:
            self.m_x = np.matrix(pandas.concat(x_data, axis=1))
        else:
            self.m_x = np.matrix(x_data).reshape(len(x_data),1)

        self.m_y = np.matrix(y_data).reshape(len(y_data),1)

        self.y_int = y_int

        self.n = self.m_x.shape[0]

        if self.y_int == True:
            int_vector = np.ones((self.n,1))
            self.m_x = np.concatenate((int_vector, self.m_x), axis=1)
            self.k = self.m_x.shape[1]
        else:
            self.k = self.m_x.shape[1]

        self.last_x_value = self.m_x[self.n - 1]

        self.df = self.n - self.k

        self.m_x_t = self.m_x.T

        ##The first value in the matrix is B0(The Int), then B1, B2,...
        self.b_hats = (self.m_x_t * self.m_x).I * self.m_x_t * self.m_y

        self.y_hat = self.m_x * self.b_hats

        self.res_errors = self.m_y - self.y_hat
        self.SSR = np.sum(np.square(self.res_errors))

        self.mean_y = np.mean(self.m_y)

        self.SSE = np.sum(np.square(self.y_hat - self.mean_y))
        self.SST = np.sum(np.square(self.m_y - self.mean_y))

        self.R2 = 1 - (self.SSR / self.SST)

        self.R2_Adj = 1 - ((self.SSR/(self.n-1)) / (self.SST/self.df))

        self.MSE = np.sum(np.square(self.res_errors)) / self.df

        self.ME = np.sqrt(self.MSE)

        self.var_b_hat = (self.m_x_t * self.m_x).I
        
        self.SE_b_hats = np.diagonal(np.sqrt(self.MSE * self.var_b_hat))

    def sim(self, nsims):
        ##Number of Simulations to run
        self.nsims = nsims
            
        ##begin the iterations
        for n in range(0,self.nsims):
            
            ##Simulate the true standard error by using the residual error(ME)
            ##proportional to a chi-square distribution. Take a random draw.
            r_chi_var = float(chi2.rvs(self.df, size=1))
            sim_sigma = self.ME * np.sqrt(self.df / r_chi_var)
            sim_sigma2 = np.square(sim_sigma)

            ##Create MVN variable of the estimated betas based on
            ##the simulated true sigma
            sim_beta_mean = np.array(self.b_hats).reshape(self.k,)
            sim_beta_var = sim_sigma2 * self.var_b_hat
            sim_beta = multivariate_normal.rvs(sim_beta_mean, sim_beta_var)
            
            ##create an array of simulate B_Hats and Sigmas
            if n == 0:
                self.b_hat_sims = np.array(sim_beta)
                self.sigma_hat_sims = np.array(sim_sigma)
            else:
                self.b_hat_sims = np.append(self.b_hat_sims, sim_beta)
                self.sigma_hat_sims = np.append(self.sigma_hat_sims, sim_sigma)
                    
        ##Reshape the estimated Betas array for matrix multiplication.
        self.b_hat_sims = np.matrix(self.b_hat_sims.reshape(nsims, self.k))
        self.sigma_hat_sims = np.matrix(self.sigma_hat_sims.reshape(nsims, 1))

        ##Return a list with the first element a number-of-sims by k matrix of Betas.
        ##The second element is a number-of-sims by 1 matrix of estimated errors 
        return [self.b_hat_sims, self.sigma_hat_sims]

    def norm_pred_sim(self,nsims,pred_variables):
        ##Designed to use the "sim" function to predict confidence intervals
        self.pv = pred_variables
        array_list = []
        for pred_value in self.pv:
            ##Run the sim.
            sim_vals = self.sim(nsims)
            ##Get the estimated betas in a (k x nsims) matrix.
            betas = sim_vals[0].T
            ##Get the estimated sigmas in a (1 x nsims) matrix.
            sigma = sim_vals[1].T
            sigma = np.array(sigma).ravel()
            ##Get a point estimate for the current predictor variable.
            pred_value = np.matrix([1,pred_value]).ravel()
            point_est = np.array(pred_value * betas).ravel()
            ##Get Random Variables for pred_value.
            ran_vec = np.zeros(nsims)
            for loop in range(nsims):
                np.put(ran_vec,
                       loop,
                       norm.rvs(loc=point_est[loop],scale=sigma[loop]))
            ##Append random variables vector to list.
            array_list.append(ran_vec)
        ##Create one matrix from all vectors.
        result = np.vstack(array_list)
        return result

def log_norm_mc_chain(start,nsims,periods,loc,scale):
    ##Create a nsims number of Markov Chain for given periods, using a
    ##normal distribution of log values from some starting point.
    for sim in range(nsims):
        temp_vec = np.zeros(periods)
        temp_start = start
        array_list = []
        for period in range(periods):
            rv = norm.rvs(loc=loc,scale=scale)
            np.put(temp_vec,
                   period,
                   temp_start+rv)
            temp_start = temp_start+rv
        ##Append random variables vector to list.
        array_list.append(temp_vec)
    ##Create one matrix from all vectors
    result = np.vstack(array_list)
    return result
