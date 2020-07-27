import numpy as np
import pandas as pd
from Aircraft import *
import math

class AircraftDatabase:
    def __init__(self, I, aircraft_profile_df):
        self.Aircrafts = {}
        self.I = I
        for i in I:
            self.Aircrafts[i] = Aircraft(i, aircraft_profile_df.loc[i]['Type'])
        
    def UpdatePerDayData(self, D, aircraft_profile_df, aircraft_status_df, initial_flight_schedule_df):
        #self.status_per_day_df = pd.DataFrame(columns=['Date', 'Registration', 'FH', 'FC', 'FD','Start Location', 'End Location', 'Stay Duration', 'Possible Maintenance Location'])
        
        Sum_FH_Util = {}
        Sum_FC_Util = {}
        #Initial FH/FC
        for i in self.I:
            self.Aircrafts[i].Initial_FH = aircraft_status_df.loc[i]['Initial FH']
            self.Aircrafts[i].Initial_FC = aircraft_status_df.loc[i]['Initial FC']
            self.Aircrafts[i].Original_C_A = aircraft_profile_df.loc[i]['Original C of A']
            self.Aircrafts[i].Initial_FD = (pd.Timestamp(D[0]) -  self.Aircrafts[i].Original_C_A).days
            
            Sum_FH_Util[i] = aircraft_status_df.loc[i]['Initial FH']
            Sum_FC_Util[i] = aircraft_status_df.loc[i]['Initial FC']
            self.Aircrafts[i].Status = aircraft_status_df.loc[i]['Status']
            
        #Scheduling
        for d in D:
            one_day_schedule = initial_flight_schedule_df[initial_flight_schedule_df['End Date'] == d]
            for i in self.I:
                schedule_aircraft_per_day = one_day_schedule[one_day_schedule['Registration'] == i]
                sum_schedule = schedule_aircraft_per_day.sum()
                Sum_FH_Util[i] += sum_schedule['Util FH']
                Sum_FC_Util[i] += sum_schedule['Util FC']
                
                # Get aircraft data daily data on d of aircraft i
                aircraft_daily_data = self.Aircrafts[i].GetDailydata(d)
                aircraft_daily_data.FH = Sum_FH_Util[i]
                aircraft_daily_data.FC = Sum_FC_Util[i]
                aircraft_daily_data.FD = (pd.Timestamp(d) - aircraft_profile_df.loc[i]['Original C of A']).days
                
                if(len(schedule_aircraft_per_day.index) > 0): # Aircraft i has flight on day d
                    latest_schedule = schedule_aircraft_per_day.sort_values(by='Chox on time', ascending=False).iloc[0]
                    aircraft_daily_data = self.Aircrafts[i].GetDailydata(d)
                    aircraft_daily_data.start_time = pd.to_datetime(str(latest_schedule['Start Date']) + " " + str(latest_schedule['Chox off time']))
                    aircraft_daily_data.end_time = pd.to_datetime(str(latest_schedule['End Date']) + " " + str(latest_schedule['Chox on time']))
                    aircraft_daily_data.start_loc = latest_schedule['Start Loc']
                    aircraft_daily_data.end_loc = latest_schedule['End Loc']
                    aircraft_daily_data.stay_duration = latest_schedule['Duration']
                    aircraft_daily_data.possible_maint_loc = latest_schedule['Maint Station']
                
                
    def UpdateLimitMaintenanceData(self, K, aircraft_profile_df, interval_limitation_df):
        for i in self.I:
            aircraft_type = aircraft_profile_df.loc[i]['Type']
            filter_by_aircraft_type = interval_limitation_df[interval_limitation_df['Aircraft Type'] == aircraft_type]
            
            for k in K:
                #filter interval_limitation_df by current k
                filter_by_aircraftcheck = filter_by_aircraft_type[filter_by_aircraft_type['Check1'] == k]
                aircraft_maintenance_data = self.Aircrafts[i].GetMaintenanceData(k)
                if(len(filter_by_aircraftcheck.index) > 0): #if row > 0 then it's found
                    # Get first row with filter_by_aircraftcheck.iloc[0]
                    # [i][k] reads from registration i with check k
                    aircraft_maintenance_data.limit_FH = filter_by_aircraftcheck.iloc[0]['Limitation FH']
                    aircraft_maintenance_data.limit_FC = filter_by_aircraftcheck.iloc[0]['Limitation FC']
                    aircraft_maintenance_data.limit_FD = filter_by_aircraftcheck.iloc[0]['Limitation FD'] 
                    
    def UpdateAverageUtilizationData(self, aircraft_profile_df):
        for i in self.I:
            self.Aircrafts[i].avg_utilization_FH = aircraft_profile_df.loc[i]['Avg FH']
            self.Aircrafts[i].avg_utilization_FC = aircraft_profile_df.loc[i]['Avg FC']

    def UpdateIntervalCheckData(self, K, aircraft_profile_df, maintenance_interval_df):
        for i in self.I:
            aircraft_type = aircraft_profile_df.loc[i]['Type']
            filter_by_aircraft_type = maintenance_interval_df[maintenance_interval_df['Aircraft Type'] == aircraft_type]
            
            for k in K:
                #filter interval_limitation_df by current k
                filter_by_aircraftcheck = filter_by_aircraft_type[filter_by_aircraft_type['Check1'] == k]
                if(len(filter_by_aircraftcheck.index) > 0): #if row > 0 then it's found
                    aircraft_maintenance_data = self.Aircrafts[i].GetMaintenanceData(k)
                    # Get first row with filter_by_aircraftcheck.iloc[0]
                    # [i][k] reads from registration i with check k
                    aircraft_maintenance_data.interval_check_FH = filter_by_aircraftcheck.iloc[0]['Value FH']
                    aircraft_maintenance_data.interval_check_FC = filter_by_aircraftcheck.iloc[0]['Value FC']
                    aircraft_maintenance_data.interval_check_FD = filter_by_aircraftcheck.iloc[0]['Value FD']
    
    def UpdateLastMaintenance(self, K, last_maintenance_status_df):
        for i in self.I:
            for k in K:
                last_maintenance_df = last_maintenance_status_df[np.logical_and(last_maintenance_status_df['Registration'] == i, last_maintenance_status_df['Check1'] == k)]
                if(len(last_maintenance_df.index) > 0):
                    aircraft_maintenance_data = self.Aircrafts[i].GetMaintenanceData(k)
                    row = last_maintenance_df.iloc[0]
                    
                    aircraft_maintenance_data.last_maintenance_number = row['Check2']
                    aircraft_maintenance_data.last_maintenance_fh = row['Last_FH']
                    aircraft_maintenance_data.last_maintenance_fc = row['Last_FC']
                    aircraft_maintenance_data.last_maintenance_fc = (pd.Timestamp(row['Start date']) - self.Aircrafts[i].Original_C_A).days
    
    def CalculateUrgencyRate(self, i, k, d):
        return self.CalculateUrgencyRate(i, k, d, self.Aircrafts[i].last_maintenance_number[k])
        
    def CalculateUrgencyRate(self, i, k, d, number):
        maintenance_data = self.GetAircraftMaintenanceData(i,k)
        is_aircraft_has_check_k = np.isnan(maintenance_data.interval_check_FH) & np.isnan(maintenance_data.interval_check_FC) & np.isnan(maintenance_data.interval_check_FD)
                
        if(is_aircraft_has_check_k):
            #print("Pesawat " + i + " Check "+ k)
            urgency_rates = list()
            aircraft_daily_data = self.Aircrafts[i].GetDailydata(d)
            urgency_rates.append(AircraftDatabase.CalculateUrgency(maintenance_data.interval_check_FH, aircraft_daily_data.FH, number, maintenance_data.limit_FH))
            urgency_rates.append(AircraftDatabase.CalculateUrgency(maintenance_data.interval_check_FC, aircraft_daily_data.FC, number, maintenance_data.limit_FC))
            urgency_rates.append(AircraftDatabase.CalculateUrgency(maintenance_data.interval_check_FD, aircraft_daily_data.FD, number, maintenance_data.limit_FD))
                        
            max_divisor = 0
            max_urgency = 0
            max_index = 0
                        
            for index, urgency_rate in enumerate(urgency_rates):
                if(urgency_rate[1] > max_divisor):
                    max_urgency = urgency_rate[0]
                    max_divisor = urgency_rate[1]
                    max_index = index
                elif(urgency_rate[1] == max_divisor and  max_urgency < urgency_rate[0]):
                    max_urgency = urgency_rate[0]
                    max_divisor = urgency_rate[1]
                    max_index = index
                    
            #[Value urgency rate, last maintenance number of k, limit value]
            return [urgency_rates[max_index][0], urgency_rates[max_index][1], urgency_rates[max_index][2]]
        else:
            return [np.nan, np.nan, np.nan]
    
    def CalculateUrgency(interval_check, time, limit):
        if(not np.isnan(interval_check)):
            divisor = math.floor(time / interval_check)
            last_divisor = divisor * interval_check
            result = (time - last_divisor) / interval_check
            #print("Divisor : " + str(divisor) + ", time : " + str(time) + ", interval check : " + str(interval_check) + ", result: " + str(result))
            return [result, divisor, limit]
        else:
            return [0, 0, limit]
        
    def CalculateUrgency(interval_check, time, last_check, limit):
        if(not np.isnan(interval_check)):
            last_divisor = last_check * interval_check
            result = (time - last_divisor) / interval_check
            #print("Divisor : " + str(divisor) + ", time : " + str(time) + ", interval check : " + str(interval_check) + ", result: " + str(result))
            return [result, last_check, limit/interval_check]
        else:
            return [0, 0, 0]
    
    def GetAircraft(i):
        return aircraft_database.Aircrafts[i]
    
    def GetAircraftDailyData(self, i, d):
        return aircraft_database.Aircrafts[i].GetDailydata(d)
    
    def GetAircraftMaintenanceData(self, i, k):
        return aircraft_database.Aircrafts[i].GetAircraftMaintenanceData(k)
    