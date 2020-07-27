# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from AircraftMaintenanceData import *
from AircraftDailyData import *

class Aircraft:
    
    def __init__(self, i, t):
        self.i = i
        self.t = t
        self.Original_C_A = np.nan
        self.Initial_FH = 0
        self.Initial_FC = 0
        self.Initial_FD = 0
        self.avg_utilization_FH = 0
        self.avg_utilization_FC = 0
        self.daily_data = {} # by d
        self.maintenance_data = {} #by k
        
    def IsHasCheck(self, k):
        return self.last_maintenance_number[k] == -1
    
    def GetMaintenanceData(self, k):
        if(not k in self.maintenance_data):
            self.maintenance_data[k] = AircraftMaintenanceData()
        return self.maintenance_data[k]
    
    def GetDailydata(self, d):
        if(not d in self.daily_data):
            self.daily_data[d] = AircraftDailyData()
        return self.daily_data[d]