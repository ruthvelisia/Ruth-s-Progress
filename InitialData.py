import pandas as pd
import os

class InitialData:
    
    def LoadAllFile(self):
        self.LoadFlightSchedule()
        self.LoadHangarData()
        self.LoadStatusMaintenance()
        self.LoadAircraftStatusData()
        self.LoadAircrafProfile()
        self.LoadMaintenanceData()
        
    def LoadFlightSchedule(self):
        file_names = os.listdir('Data/Schedule/')
        self.initial_flight_schedule_df = pd.DataFrame()
        for value in file_names:
            df = pd.read_excel('Data/Schedule/'+value, index_col=None, parse_dates=['Start Date', 'End Date'])
            self.initial_flight_schedule_df = pd.concat([self.initial_flight_schedule_df, df])
        
        self.initial_flight_schedule_df = self.initial_flight_schedule_df.drop(['Wheels off date', 'Duration', 'Maint Station'], axis = 1)
        #print(self.initial_flight_schedule_df.info())
            
    def LoadStatusMaintenance(self):
        self.initial_maintenance_status_df = pd.read_excel("Data/Maintenance Status.xlsx", index_col=0)
        self.initial_maintenance_status_df['From'] = pd.to_datetime(self.initial_maintenance_status_df['From'].astype(str) + " " + self.initial_maintenance_status_df['Time'])
        self.initial_maintenance_status_df['To'] = pd.to_datetime(self.initial_maintenance_status_df['To'].astype(str) + " " + self.initial_maintenance_status_df['Time.1'])
        self.initial_maintenance_status_df = self.initial_maintenance_status_df.drop(['Time', 'Time.1'], axis = 1)
        
    def LoadHangarData(self):
        self.hangar_profile_df = pd.read_excel("Data/Hangar Profile.xlsx", index_col=0)
        sizeColoumnIndex = self.hangar_profile_df.columns.get_loc("Size")
        for index in range(len(self.hangar_profile_df.columns)-(sizeColoumnIndex+1)):
            currentIndex = sizeColoumnIndex + index + 1
            self.hangar_profile_df[self.hangar_profile_df.columns[currentIndex]] = self.hangar_profile_df[self.hangar_profile_df.columns[currentIndex]].astype('float64')  > 0
        #print(self.hangar_profile_df.head())
        
    def LoadAircraftStatusData(self):
        self.aircraft_status_df = pd.read_excel("Data/Initial Aircraft Status.xlsx", index_col = 0, dtype={'Registration': str, 'Status as per 31 Dec 2018': str})
        self.aircraft_status_df = self.aircraft_status_df.drop(['Aicraft Type', 'Maintenance', 'Flying', 'Parking', 'Remark', 'Date'], axis = 1)
        self.aircraft_status_df.rename(columns={'Status as per 31 Dec 2018' : 'Status'}, inplace=True)
        #print(self.aircraft_status_df.info())
        
    def LoadAircrafProfile(self):
        self.aircraft_profile_df = pd.read_excel("Data/Aircraft Profile.xlsx", index_col = 0)
        self.aircraft_profile_df = self.aircraft_profile_df.drop(['Original C of A', 'Delivery Date'], axis = 1)
        self.aircraft_profile_df.columns = ['Type', 'Company', 'Size', 'Registration', 'Avg FH', 'Avg FC']
        #print(self.aircraft_profile_df.info())
        
    def LoadMaintenanceData(self):
        self.maintenance_data = pd.read_excel("Data/Durasi/Duration ALL 20200704.xlsx", index_col = 0)
        self.maintenance_data.columns = ['Key', 'Type', 'MOP', 'Duration']
        self.maintenance_data['Duration'] = (self.maintenance_data['Duration'] * 3600 * 24).astype('float64') 
        #print(self.maintenance_data.info())
        

