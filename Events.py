# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 12:29:29 2019

@author: RiiVa
"""

import collections as collect

events = {}
#LLega un barco al puerto
events['ARRIVE'] = 1
#Termina de cargar el barco en el muelle
events['LOADING'] = 2
#el carguero viaja solo hasta el puerto
events['MOVE_ALONE'] = 3
#el carguero lleva un barco al puerto
events['TO_PORT'] = 4
#el carguero lleva un barco al muelle
events['TO_HARBOR'] = 5
#No ha pasado nada
events['NOT_EVENT'] = 6

class EventManager:
    
    
    def __init__(self):
        self.heap = []
        
    def add_events(self , event , time , ship = None):
        e = Event(event, time, ship)
        collect._heapq.heappush(self.heap,(e.get_time(),e))        
        
    def next_event(self):
        if len(self.heap) > 0:
            i,event = collect._heapq.heappop(self.heap)
            return event
        
        return Event(events['NOT_EVENT'], -1, None)
    
        
class Event:
    
    
    def __init__(self, itype , time , ship ):
        self.__itype__ = itype
        self.__time__ = time    
        self.__ship__ = ship  
    
    def get_type(self):
        return self.__itype__
    
    def get_time(self):
        return self.__time__
    
    def get_ship(self):
        return self.__ship__
    
    def ToCompare(self, event):
            return self.__time__ < event.get_time()

    