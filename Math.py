# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:13:33 2019

@author: RiiVa
"""

import numpy as np


class Math:
    
    
    def ExpDistribution(self,lamb):
        if lamb is 0:
            return 0
        ran = np.random.uniform()
        
        np.log(ran)
        #print(-(1/lamb) * np.log(ran))
        return -(lamb) * np.log(ran)
        
            
    
    def NormalDistribution(self,mean,ro):
        
        ran1 = np.random.uniform()
        
        ran2 = np.random.uniform()
        
        z = np.sqrt(-2.0 * np.log(ran1)) * np.cos(2.0 * np.pi * ran2)
        
        return z*np.sqrt(ro)+mean
        
