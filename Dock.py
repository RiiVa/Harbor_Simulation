# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:19:07 2019

@author: RiiVa
"""
import numpy as np


#Tamanos de los barcos
# 1 pequeno 2 mediano 3 grande

#Estados del carguero
tugstatus = {}
tugstatus['WAIT_PORT'] = 1 #espera en el puerto
tugstatus['WAIT_HARBOR'] = 2 #espera en el muelle
tugstatus['TO_PORT_ALONE' ] = 3 #regresa al puerto solo
tugstatus[ 'TO_PORT_'] = 4 #lleva un barco al puerto
tugstatus[ 'TO_HARBOR'] = 5 #lleva un barco al muelle

        
    
class Tug:
    
    def __init__(self):
        self.status = 1
        self.ship = None
        
    def move_ship(self, ship):
        self.ship = ship
    
    def get_ship(self):
        return self.ship
    
    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status
    
    def leave_ship(self):
        self.ship = None
        

class Dock_Harbor_Manager:

    
    def __init__(self, harbor_count):
        
        self.total = 0
        self.harbor = 0
        self.total_register = {}
    
        self.harbor_register = {}
    
        self.ship_port_waiting = []
        
        self.ship_harbor_waiting = []
        
        self.ship_loading = [None for x in range(harbor_count)]
    
    def get_ship_harbor(self):
        return self.ship_harbor_waiting[0]
    
    def register_ship_arrive(self, ship, time):
        self.total_register[ship] = (time, -1)
        self.total+=1
        
    def register_ship_leave(self, ship, time):
        self.total-=1
        #print(self.total)
        mytime,_ = self.total_register[ship]
        self.total_register[ship] = (mytime, time)
        
    def register_harbor_finish(self, ship, time):
        self.harbor += 1
        print("ship")
        self.harbor_register[ship] = (time, -1)
    
    def register_harbor_leave(self, ship, time):
        
        self.harbor-=1
        print(self.harbor)
        #print(ship)
        mytime,_ = self.harbor_register[ship]
        self.harbor_register[ship] = (mytime, time)

    def any_harbor_free(self):
        for x in self.ship_loading:
            if x is None:
                return True
        return False
    
    def enqueue_ship_harbor(self, ship):
        self.ship_harbor_waiting.append(ship)
    
    def enqueue_ship_port(self, ship):
        self.ship_port_waiting.append(ship)
    
    def dequeue_ship_port(self):
        #a = self.ship_port_waiting[0]
        return self.ship_port_waiting.pop(0)
        
    
    def dequeue_ship_harbor(self):
        #a = self.ship_harbor_waiting[0]
        return self.ship_harbor_waiting.pop(0)
        
    
    def ship_port_waiting_count(self):
        return len(self.ship_port_waiting)
    
    def ship_harbor_waiting_count(self):
        return len(self.ship_harbor_waiting)
    
    def any_ship_port_waiting(self):
        return self.ship_port_waiting_count() > 0
    
    def any_ship_harbor_waiting(self):
        return self.ship_harbor_waiting_count() > 0
    
    def enter_ship_harbor(self, ship):
        i = 0
        for x in self.ship_loading:
            if x is None:
                self.ship_loading[i] = ship
            i+=1
            return 0
        return -1
    def leave_ship_harbor(self, ship):
        i = 0
        for x in self.ship_loading:
            if x == ship:
                a = ship
                self.ship_loading[i] = None
                return a            
            i+=1
        return -1
    
    def mean_total(self):
        sum = 0.0
        i = 0
        
        for x in self.total_register.values():
            if x[1] > 0:
                i+=1
                sum += x[1]-x[0]
        #print(i)
        return sum/i
    
    def mean_harbor(self):
        sum =  0.0
        i = 0.0
        #print(i)
        for x in self.harbor_register.values():
            if x[1] > 0:
                i+=1.0
                sum += x[1] - x[0]
        if i == 0:
            return 0
        return sum/i

class Ship:
    
    def __init__(self):
        rd = np.random.uniform()
        if( 0 <= rd <= 0.25):
            self.size = 1
        else:
            if( 0.25 < rd <= 0.50):
                self.size = 2
            else:
                self.size = 3
                
    def get_size(self):
        return self.size
      