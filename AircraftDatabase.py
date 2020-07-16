import numpy as np
import pandas as pd
from Aircraft import *

class AircraftDatabase:
    def __init__(self, I, aircraft_profile_df):
        self.Aircrafts = {}
        self.I = I
        for i in I:
            self.Aircrafts[i] = Aircraft(i, aircraft_profile_df.loc[i]['Type'])
        
    def UpdatePerDayData(self, D, aircraft_profile_df, aircraft_status_df, initial_flight_schedule_df):
        #self.status_per_day_df = pd.DataFrame(columns=['Date', 'Registration', 'FH', 'FC', 'FD','Start Location', 'End Location', 'Stay Duration', 'Possible Maintenance Location'])

        #Initial FH/FC
        for i in self.I:
            self.Aircrafts[i].Sum_FH_Util = aircraft_status_df.loc[i]['Initial FH']
            self.Aircrafts[i].Sum_FC_Util = aircraft_status_df.loc[i]['Initial FC']

        #Scheduling
        for d in D:
            one_day_schedule = initial_flight_schedule_df[initial_flight_schedule_df['End Date'] == d]
            for i in self.I:
                schedule_aircraft_per_day = one_day_schedule[one_day_schedule['Registration'] == i]
                sum_schedule = schedule_aircraft_per_day.sum()
                self.Aircrafts[i].Sum_FH_Util += sum_schedule['Util FH']
                self.Aircrafts[i].Sum_FC_Util += sum_schedule['Util FC']
                self.Aircrafts[i].FH[d] = self.Aircrafts[i].Sum_FH_Util
                self.Aircrafts[i].FC[d] = self.Aircrafts[i].Sum_FC_Util
                self.Aircrafts[i].FD[d] = (pd.Timestamp(d) - aircraft_profile_df.loc[i]['Original C of A']).days
                
                if(len(schedule_aircraft_per_day.index) > 0): # Aircraft i has flight on day d
                    latest_schedule = schedule_aircraft_per_day.sort_values(by='Chox on time', ascending=False).iloc[0]
                    #if(len(schedule_aircraft_per_day.index) > 1):
                    #    print("Aircraft " + self.Aircrafts[i].i + " double flight on " + str(d) + " latest : " + str(latest_schedule['Chox on time']))
                    self.Aircrafts[i].start_time[d] = pd.to_datetime(str(latest_schedule['Start Date']) + " " + str(latest_schedule['Chox off time']))
                    self.Aircrafts[i].end_time[d] = pd.to_datetime(str(latest_schedule['End Date']) + " " + str(latest_schedule['Chox on time']))
                    self.Aircrafts[i].start_loc[d] = latest_schedule['Start Loc']
                    self.Aircrafts[i].end_loc[d] = latest_schedule['End Loc']
                    self.Aircrafts[i].stay_duration[d] = latest_schedule['Duration']
                    self.Aircrafts[i].possible_maint_loc[d] = latest_schedule['Maint Station']
                else: # Aircraft i doesn't have flight on day d
                    #print("Aircraft " + self.Aircrafts[i].i + " Doesn't fly on " + str(d))
                    self.Aircrafts[i].start_time[d] = np.nan
                    self.Aircrafts[i].end_time[d] = np.nan
                    self.Aircrafts[i].start_loc[d] = np.nan
                    self.Aircrafts[i].end_loc[d] = np.nan
                    self.Aircrafts[i].stay_duration[d] = np.nan
                    self.Aircrafts[i].possible_maint_loc[d] = np.nan
                #self.status_per_day_df = self.status_per_day_df.append({'Date': d, 'Registration': i, 'FH': self.Aircrafts[i].FH[d], 'FC': self.Aircrafts[i].FC[d], 'FD': self.Aircrafts[i].FD[d], 'Start Location': self.Aircrafts[i].start_loc[d], 'End Location': self.Aircrafts[i].end_loc[d], 'Stay Duration': self.Aircrafts[i].stay_duration[d], 'Possible Maintenance Location': self.Aircrafts[i].possible_maint_loc[d]}, ignore_index=True)
                
    def UpdateLimitMaintenanceData(self, K, aircraft_profile_df, interval_limitation_df):
        for i in self.I:
            aircraft_type = aircraft_profile_df.loc[i]['Type']
            filter_by_aircraft_type = interval_limitation_df[interval_limitation_df['Aircraft Type'] == aircraft_type]
            
            for k in K:
                #filter interval_limitation_df by current k
                filter_by_aircraftcheck = filter_by_aircraft_type[filter_by_aircraft_type['Check1'] == k] 
                if(len(filter_by_aircraftcheck.index) > 0): #if row > 0 then it's found
                    # Get first row with filter_by_aircraftcheck.iloc[0]
                    # [i][k] reads from registration i with check k
                    self.Aircrafts[i].limit_FH[k] = filter_by_aircraftcheck.iloc[0]['Limitation FH']
                    self.Aircrafts[i].limit_FC[k] = filter_by_aircraftcheck.iloc[0]['Limitation FC']
                    self.Aircrafts[i].limit_FD[k] = filter_by_aircraftcheck.iloc[0]['Limitation FD'] 
                else:
                    self.Aircrafts[i].limit_FH[k] = np.nan
                    self.Aircrafts[i].limit_FC[k] = np.nan
                    self.Aircrafts[i].limit_FD[k] = np.nan
                    
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
                    # Get first row with filter_by_aircraftcheck.iloc[0]
                    # [i][k] reads from registration i with check k
                    self.Aircrafts[i].interval_check_FH[k] = filter_by_aircraftcheck.iloc[0]['Value FH']
                    self.Aircrafts[i].interval_check_FC[k] = filter_by_aircraftcheck.iloc[0]['Value FC']
                    self.Aircrafts[i].interval_check_FD[k] = filter_by_aircraftcheck.iloc[0]['Value FD']
                else:
                    self.Aircrafts[i].interval_check_FH[k] = np.nan
                    self.Aircrafts[i].interval_check_FC[k] = np.nan
                    self.Aircrafts[i].interval_check_FD[k] = np.nan
    
    def UpdateLastMaintenance(self, K, last_maintenance_status_df):
        for i in self.I:
            for k in K:
                last_maintenance_df = last_maintenance_status_df[np.logical_and(last_maintenance_status_df['Registration'] == i, last_maintenance_status_df['Check1'] == k)]
                if(len(last_maintenance_df.index) > 0):
                    self.Aircrafts[i].last_maintenance_number[k] = last_maintenance_df.iloc[0]['Check2']
                else:
                    self.Aircrafts[i].last_maintenance_number[k] = np.nan