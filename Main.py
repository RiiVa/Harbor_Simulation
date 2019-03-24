# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 16:54:00 2019

@author: RiiVa
"""
from Math import Math
from Events import EventManager
from Dock import Tug,Ship,Dock_Harbor_Manager
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
class Main:
    
    def __init__(self, harbor_size):
        self.math = Math()
        self.events_iter = EventManager()
        self.dock_manager = Dock_Harbor_Manager(3)
        self.tug = Tug()
        
        
        
    def run(self):
        
        currentT = 0
        finalT = 5000000.0
        self.events_iter.add_events(events['ARRIVE'], self.math.ExpDistribution(8.0))
        i = 0
        while currentT < finalT:
            
            event = self.events_iter.next_event()
            #print(event.get_type())
            currentT = event.get_time()
            
            #Arriba un carguero al puerto
            if event.get_type() is 1:
                ship = Ship()
                self.dock_manager.register_ship_arrive(ship, currentT)
                print("En el puerto un barco de tamano ", ship.size, "Time :", currentT)
                if self.tug.get_status() is 1:
                    print("Llevando el barco para el muelle", "Time :", currentT)
                    self.tug.move_ship(ship)    
                    self.tug.set_status(5)
                    self.events_iter.add_events(events['TO_HARBOR'] , currentT + self.math.ExpDistribution(2.0) ,ship)
                    
                    
                else:
                    print("el remolcador esta ocupado, llevar el barco a la cola" , "Time :", currentT)
                    self.dock_manager.enqueue_ship_port(ship)
               
                self.events_iter.add_events(events['ARRIVE'], currentT +  self.math.ExpDistribution(8.0))
                continue; 
            
            #Un carguero termina de cargar
            if event.get_type() is 2:
                ship_finish = event.get_ship()
               # i+=1
                print("El carguero termino de cargar" , "Time :", currentT)
                if self.tug.get_status() is 2:
                    #sacando carguero de la lista de muelles 
                #    i-=1 
                    
                    print("el carguero es llevado al puerto" , "Time :", currentT)
                    self.tug.move_ship(ship)
                    self.tug.set_status(4) 
                    self.events_iter.add_events(events['TO_PORT'], currentT +  self.math.ExpDistribution(1))
                
                
                
                else:
                    #El carguero se pone en la cola del muelle
                    print("El carguero se pone en la cola del muelle", "Time :", currentT)
                    self.dock_manager.register_harbor_finish(ship_finish, currentT)
                    self.dock_manager.enqueue_ship_harbor(ship_finish)
                continue;
            #el remolcador regresa solo para el puerto
            if event.get_type() is 3:
                
                if self.dock_manager.any_ship_port_waiting():
                    
                    print("Sacando barco de la cola del puerto", "Time :", currentT)
                    ship = self.dock_manager.dequeue_ship_port()
                    self.tug.move_ship(ship)
                    self.tug.set_status(5)
                    
                    self.events_iter.add_events(events['TO_HARBOR'], currentT + self.math.ExpDistribution(2), ship)
                    
                    
                    
                else:
                    print("El remolcador se pone en modo espera", "Time :", currentT)
                    self.tug.set_status(1)
                continue;
            #el remolcador lleva un carguero al puerto
            if event.get_type() is 4:
                self.dock_manager.register_ship_leave(self.tug.get_ship(), currentT)
                print("sacar el carguero de la cola del puerto", "Time :", currentT)
                
                if self.dock_manager.any_ship_port_waiting():
                    ship = self.dock_manager.dequeue_ship_port()
                    self.tug.move_ship(ship)
                    self.tug.set_status(5)
                    print("Llevando el carguero para el muelle", "Time :", currentT)
                    self.events_iter.add_events(events['TO_HARBOR'],currentT + self.math.ExpDistribution(2), ship)
                else:
                    #deja el carguero y se pone a esperar
                    print("El remolcador de pone en espera en el puerto" , "Time :", currentT)
                    self.tug.leave_ship()
                    self.tug.set_status(1)
                
                continue;
            #el remolcador lleva un carguero al muelle
            if event.get_type() is 5:
                
                print("El remolcador traer un carguero al muelle")
                ship_harbor = self.tug.get_ship()
                self.dock_manager.enter_ship_harbor(ship_harbor)
                
                
                if self.dock_manager.any_ship_harbor_waiting():
                    print("El remolcador se lleva un barco al puerto", "Time :", currentT)
                    ship = self.dock_manager.dequeue_ship_harbor()
                    self.tug.move_ship(ship)
                    self.dock_manager.register_harbor_leave(ship, currentT)
                    
                    self.tug.set_status(4)
                    self.events_iter.add_events(events['TO_PORT'],currentT + self.math.ExpDistribution(1))
                elif self.dock_manager.any_harbor_free():
                    #el remolcador se va para el puerto solo
                    print("El remolcador se dirige al puerto solo")
                    self.tug.set_status(3)
                    self.tug.leave_ship()
                    self.events_iter.add_events(events['MOVE_ALONE'], currentT + self.math.ExpDistribution(0.25))
                else:
                    #se pone a esperar q halla un hueco libre
                    #print("ENTROOOOOOOOOOOOOOO")
                    #if self.dock_manager.any_harbor_free() :
                    #    i+=1
                    print("El remolcador se pone en espera en el muelle")
                    self.tug.leave_ship()
                    self.tug.set_status(2)
                
                #Caso ahora para generar el tiemppo de carga del barco
                if ship_harbor.get_size() is 1:
                    self.events_iter.add_events(events['LOADING'], currentT + self.math.NormalDistribution(9,1), ship_harbor)
                    continue;
                if ship_harbor.get_size() is 2:
                    self.events_iter.add_events(events['LOADING'], currentT + self.math.NormalDistribution(12,2), ship_harbor)    
                    continue;
                if ship_harbor.get_size() is 3:
                    self.events_iter.add_events(events['LOADING'], currentT + self.math.NormalDistribution(18,3), ship_harbor)
                    continue;
                continue;
        print(i)
        return self.dock_manager.mean_total()    
a = Main(3)
print(a.run(), "horas")