# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import gurobipy as gp

class Formula:
             
    def ViolationObjFunction(m, violation_var, I, K, D):
        violation_var={} #creates an empty dictionary
        m.setObjective(sum(violation_var[i, k, d], GRB.MINIMIZE)
 #       for i in range(len(I)):
  #          for k in range(len(K)):
 #               for d in D:
 #                   m.setObjective(sum(violation_var[i][k][d]), GRB.MINIMIZE)                                          

#    def RoutingVariable(m, routing_var, D, I, F, G, aircraft_database):
 #       for i in I:
    #        for d in D:
  #              #hasSchedule = not pd.isnull(aircraft_database.Aircrafts[i].end_time[d])
   #             if(hasSchedule):
   #                 for a,b in zip(F,G):
  #                     m.addConstr(routing_var[i][d][a][b] == 1, "node")
        
 #   def RoutingVariable(m, routing_var, D, I, F, G, aircraft_database):
  #      for i in I:
   #         for d in D:
    #                for a,b in zip(F,G):
     #                  m.addConstr(routing_var[i][d][a][b] == 1, "node")
     
     class Formula:
             
    def ViolationObjFunction(m, violation_var, I, K, D):
        violation_var={} #creates an empty dictionary
        m.setObjective(sum(violation_var[i, k, d], GRB.MINIMIZE)
