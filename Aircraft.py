# -*- coding: utf-8 -*-
import pandas as pd

class Aircraft:
    
    def __init__(self, i, t):
        self.i = i
        self.t = t
        self.Sum_FH_Util = 0
        self.Sum_FC_Util = 0
        self.FH = {}
        self.FC = {}
        self.FD = {}
        self.start_time = {}
        self.end_time = {}
        self.start_loc = {}
        self.end_loc = {}
        self.stay_duration = {}
        self.possible_maint_loc = {}
        self.limit_FH = {}
        self.limit_FC = {}
        self.limit_FD = {}
        self.avg_utilization_FH = {}
        self.avg_utilization_FC = {}
        self.interval_check_FH = {}
        self.interval_check_FC = {}
        self.interval_check_FD = {}
        self.last_maintenance_number = {}