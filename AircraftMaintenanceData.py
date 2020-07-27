# -*- coding: utf-8 -*-
import numpy as np

class AircraftMaintenanceData:
    def __init__(self):
        self.limit_FH = np.nan
        self.limit_FC = np.nan
        self.limit_FD = np.nan
        self.interval_check_FH = np.nan
        self.interval_check_FC = np.nan
        self.interval_check_FD = np.nan
        self.last_maintenance_number = -1
        self.last_maintenance_fh = np.nan
        self.last_maintenance_fc = np.nan
        self.last_maintenance_fd = np.nan
        
