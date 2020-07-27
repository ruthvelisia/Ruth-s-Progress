# -*- coding: utf-8 -*-

import numpy as np

class AircraftDailyData:
    def __init__(self):        
        self.FH = np.nan
        self.FC =  np.nan
        self.FD =  np.nan
        self.start_time = np.datetime64('NaT')
        self.end_time = np.datetime64('NaT')
        self.start_loc = np.nan
        self.end_loc = np.nan
        self.stay_duration = np.nan
        self.possible_maint_loc = np.nan