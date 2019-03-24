# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:13:33 2019

@author: RiiVa
"""

import numpy as np


class Math:
    
    
    def ExpDistribution(lamb):
        if lamb is 0:
            return 0
        ran = np.random.uniform
        return -(1/lamb)*np.log(ran)
        
            
    
    def NormalDistribution(mean,ro):
        
        ran1 = np.random.uniform
        
        ran2 = np.random.uniform
        
        z = np.sqrt(-2.0*np.log(ran1)) * np.cos(2.0*np.pi*ran2)
        
        return z*np.sqrt(ro)+mean
        
