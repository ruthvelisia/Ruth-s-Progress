# -*- coding: utf-8 -*-

class Workshop:
    def __init__(self, code, station_type, city, total_slot, towing_time, check_probs, effective_slot):
        self.code = code
        self.type = station_type
        self.city = city
        self.effective_slot = effective_slot
        self.towing_time = towing_time
        self.total_slot = total_slot
        self.check_probs = check_probs
        self.used_slot = 0