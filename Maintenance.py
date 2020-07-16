# -*- coding: utf-8 -*-
class Maintenance:
    def __init__(self, t, k):#maintenance_data_df, 
        self.t = t
        self.k = k
        self.durations = {}
        self.penalty_tolerance = 0
        self.penalty_grounded_per_day = 0
