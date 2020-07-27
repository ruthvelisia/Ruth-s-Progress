import pandas as pd
import os
import numpy as np
from multiprocessing import Process
        
class InitialDataConcurent:
    
    def LoadAllFile(self):
        self.threadsCount = 8
        
        p = Process(target=self.LoadStatusMaintenance)
        p.start()
        print("Cobas")
        self.LoadFlightSchedule()
        Process(target=self.LoadHangarData).start()
        
        Process(target=self.LoadAircraftStatusData).start()
        Process(target=self.LoadAircrafProfile).start()
        Process(target=self.LoadMaintenanceData).start()
        Process(target=self.LoadLastMaintenanceStatus).start()
        Process(target=self.LoadIntervalLimitation).start()
        Process(target=self.LoadMaintenanceInterval).start()
        self.IsProcessFinished = False
    
    def RemoveThread(self):
        self.threadsCount -= 1
        print(self.threadsCount)
        if(self.threadsCount == 0):
            self.IsProcessFinished = True
    
    def LoadFlightSchedule(self):
        file_names = os.listdir('Data/Schedule/')
        self.initial_flight_schedule_df = pd.DataFrame()
        for value in file_names:
            Process(target=self.AddNewSchedule, args=(value,)).start()
        #self.initial_flight_schedule_df = self.initial_flight_schedule_df.set_index('Registration')
        
        #'Wheels on date', 'Duration' dihilangkan dari drop 
        
    def AddNewSchedule(self, file_name):
        df = pd.read_excel('Data/Schedule/'+file_name, index_col=None, parse_dates=['Start Date', 'End Date'])
        self.initial_flight_schedule_df = pd.concat([self.initial_flight_schedule_df, df], sort=False)
        self.RemoveThread()
        
            
    def LoadStatusMaintenance(self):
        print("test")
        self.initial_maintenance_status_df = pd.read_excel("Data/Maintenance Status.xlsx", index_col=0)
        self.initial_maintenance_status_df['From'] = pd.to_datetime(self.initial_maintenance_status_df['From'].astype(str) + " " + self.initial_maintenance_status_df['Time'])
        self.initial_maintenance_status_df['To'] = pd.to_datetime(self.initial_maintenance_status_df['To'].astype(str) + " " + self.initial_maintenance_status_df['Time.1'])
        self.initial_maintenance_status_df = self.initial_maintenance_status_df.drop(['Time', 'Time.1'], axis = 1)
        
        self.RemoveThread()
        #self.initial_maintenance_status_df = self.initial_maintenance_status_df.set_index('Last Maintenance  Code')
        
    def LoadHangarData(self):
        self.hangar_profile_df = pd.read_excel("Data/Hangar Profile.xlsx", index_col='Workshop')
        #sizeColoumnIndex = self.hangar_profile_df.columns.get_loc("Size")
        #for index in range(len(self.hangar_profile_df.columns)-(sizeColoumnIndex+1)):
        #    currentIndex = sizeColoumnIndex + index + 1
        #    self.hangar_profile_df[self.hangar_profile_df.columns[currentIndex]] = self.hangar_profile_df[self.hangar_profile_df.columns[currentIndex]].astype('float64')  > 0
        
        slot_effective_df = pd.read_excel("Data/Hangar Profile.xlsx", sheet_name='Effective Slot', index_col='Workshop')
        slot_utilization_df = pd.read_excel("Data/Hangar Profile.xlsx", sheet_name='Slot Utilisation', index_col='Workshop')
        
        # so we want to make new column Slot Effective and Slot Utilization to hangar profile dataframe
        # Inside of it is dictionary of the value
        slot_effective_per_workshop = np.array([])
        slot_utilization_per_workshop = np.array([])
        slot_effective_col_names = slot_effective_df.columns
        slot_util_col_names = slot_utilization_df.columns
        for workshopCode in self.hangar_profile_df.index:
            workshop_slot_effective = {}
            workshop_slot_utilization = {}
            for slot_effective_col_name in slot_effective_col_names:
                workshop_slot_effective[slot_effective_col_name] = slot_effective_df.loc[workshopCode][slot_effective_col_name]
            for slot_util_col_name in slot_util_col_names:
                workshop_slot_utilization[slot_util_col_name] = slot_utilization_df.loc[workshopCode][slot_util_col_name]
            
            slot_effective_per_workshop = np.append(slot_effective_per_workshop, workshop_slot_effective)
            slot_utilization_per_workshop = np.append(slot_utilization_per_workshop, workshop_slot_utilization)
        
        self.hangar_profile_df['Slot Effective'] = slot_effective_per_workshop
        self.hangar_profile_df['Slot Utilization'] = slot_utilization_per_workshop
        
        self.RemoveThread()
        #print(self.hangar_profile_df.head())
        
    def LoadAircraftStatusData(self):
        self.aircraft_status_df = pd.read_excel("Data/Initial Aircraft Status.xlsx", index_col = 0, dtype={'Registration': str, 'Status as per 31 Dec 2018': str})
        self.aircraft_status_df = self.aircraft_status_df.drop(['Aicraft Type', 'Maintenance', 'Flying', 'Parking'], axis = 1)
        self.aircraft_status_df.rename(columns={'Status as per 31 Dec 2018' : 'Status'}, inplace=True)
        self.aircraft_status_df = self.aircraft_status_df.set_index('Registration')   
        
        self.RemoveThread()
        #print(self.aircraft_status_df.info())
        
    def LoadAircrafProfile(self):
        self.aircraft_profile_df = pd.read_excel("Data/Aircraft Profile.xlsx", index_col = 0, parse_dates=['Original C of A'])
        self.aircraft_profile_df = self.aircraft_profile_df.drop(['Remark', 'Delivery Date'], axis = 1)
        self.aircraft_profile_df.columns = ['Registration', 'Type', 'Company', 'Size', 'Original C of A', 'Avg FH', 'Avg FC']
        self.aircraft_profile_df = self.aircraft_profile_df.set_index('Registration')
        self.RemoveThread()
        #print(self.aircraft_profile_df)
        
        #I = ['PK-GLA', 'PK-GLE']
        #initial_FH = self.aircraft_profile_df['Initial FH']
        #FH = initial_FH + 3999
        #print(FH)
        
    def LoadMaintenanceData(self):
        self.maintenance_data_df = pd.read_excel("Data/Durasi/Duration ALL 20200704.xlsx", index_col = 0)
        self.maintenance_data_df.columns = ['Key', 'Type', 'MOP', 'Letter', 'Number', 'Duration']
        self.RemoveThread()
        #self.maintenance_data = self.maintenance_data.set_index('Key')
        #print(self.maintenance_data.info())
        #print(self.maintenance_data)
    
    def LoadLastMaintenanceStatus(self):
        self.last_maintenance_status_df = pd.read_excel("Data/Last Maintenance Status.xlsx", index_col=0)
        self.last_maintenance_status_df['Start date'] = pd.to_datetime(self.last_maintenance_status_df['Start date'].astype(str) + " " + self.last_maintenance_status_df['RevStrtTm'])
        self.last_maintenance_status_df['End date'] = pd.to_datetime(self.last_maintenance_status_df['End date'].astype(str) + " " + self.last_maintenance_status_df['RevEndTm'])
        self.last_maintenance_status_df = self.last_maintenance_status_df.drop(['Revision', 'Hangar'], axis = 1)
        self.RemoveThread()
        #self.last_maintenance_status_df = self.last_maintenance_status_df.set_index('Last Maintenance Code')
        #print(self.last_maintenance_status_df.head())
    
    def LoadIntervalLimitation(self):
        self.interval_limitation_df = pd.read_excel("Data/Interval Limitation.xlsx", index_col=0, na_values = '-')
        self.interval_limitation_df = self.interval_limitation_df.drop(['Interval FH', 'Interval FC', 'Interval FD'], axis = 1)
        self.RemoveThread()
        #self.interval_limitation_df = self.interval_limitation_df.set_index('Checkpoint')
        #print(self.interval_limitation_df.head())
        
        
    def LoadMaintenanceInterval(self):
        self.maintenance_interval_df = pd.read_excel("Data/Maintenance Interval.xlsx", index_col=0, na_values = '-')
        self.maintenance_interval_df = self.maintenance_interval_df.drop(['As of MPD', 'Issued Date', 'Remark'], axis = 1)
        self.maintenance_interval_df = self.maintenance_interval_df.set_index('Checkpoint')
        self.RemoveThread()
        #print(self.maintenance_interval_df.head())
        
        


