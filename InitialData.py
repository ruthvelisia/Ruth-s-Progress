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
            self.initial_flight_schedule_df = pd.concat([self.initial_flight_schedule_df, df], sort=False)
        self.initial_flight_schedule_df = self.initial_flight_schedule_df.drop(['Maint Station'], axis = 1) 
        self.initial_flight_schedule_df = self.initial_flight_schedule_df.set_index('Registration')
        
        #'Wheels on date', 'Duration' dihilangkan dari drop out
            
    def LoadStatusMaintenance(self):
        self.initial_maintenance_status_df = pd.read_excel("Data/Maintenance Status.xlsx", index_col=0)
        self.initial_maintenance_status_df['From'] = pd.to_datetime(self.initial_maintenance_status_df['From'].astype(str) + " " + self.initial_maintenance_status_df['Time'])
        self.initial_maintenance_status_df['To'] = pd.to_datetime(self.initial_maintenance_status_df['To'].astype(str) + " " + self.initial_maintenance_status_df['Time.1'])
        self.initial_maintenance_status_df = self.initial_maintenance_status_df.drop(['Time', 'Time.1'], axis = 1)
        self.initial_maintenance_status_df = self.initial_maintenance_status_df.set_index('Last Maintenance  Code')
        
    def LoadHangarData(self):
        self.hangar_profile_df = pd.read_excel("Data/Hangar Profile.xlsx", index_col=0)
        sizeColoumnIndex = self.hangar_profile_df.columns.get_loc("Size")
        for index in range(len(self.hangar_profile_df.columns)-(sizeColoumnIndex+1)):
            currentIndex = sizeColoumnIndex + index + 1
            self.hangar_profile_df[self.hangar_profile_df.columns[currentIndex]] = self.hangar_profile_df[self.hangar_profile_df.columns[currentIndex]].astype('float64')  > 0
        #print(self.hangar_profile_df.head())
        
    def LoadAircraftStatusData(self):
        self.aircraft_status_df = pd.read_excel("Data/Initial Aircraft Status.xlsx", index_col = 0, dtype={'Registration': str, 'Status as per 31 Dec 2018': str})
        self.aircraft_status_df = self.aircraft_status_df.drop(['Aicraft Type', 'Maintenance', 'Flying', 'Parking'], axis = 1)
        self.aircraft_status_df.rename(columns={'Status as per 31 Dec 2018' : 'Status'}, inplace=True)
        self.aircraft_status_df = self.aircraft_status_df.set_index('Registration')        
        #print(self.aircraft_status_df.info())
        
    def LoadAircrafProfile(self):
        self.aircraft_profile_df = pd.read_excel("Data/Aircraft Profile.xlsx", index_col = 0, parse_dates=['Original C of A'])
        self.aircraft_profile_df = self.aircraft_profile_df.drop(['Remark', 'Delivery Date'], axis = 1)
        self.aircraft_profile_df.columns = ['Type', 'Company', 'Size', 'Registration', 'Original C of A', 'Avg FH', 'Avg FC']
        self.aircraft_profile_df = self.aircraft_profile_df.set_index('Registration')
        #print(self.aircraft_profile_df)
        
        #I = ['PK-GLA', 'PK-GLE']
        #initial_FH = self.aircraft_profile_df['Initial FH']
        #FH = initial_FH + 3999
        #print(FH)
        
    def LoadMaintenanceData(self):
        self.maintenance_data = pd.read_excel("Data/Durasi/Duration ALL 20200704.xlsx", index_col = 0)
        self.maintenance_data.columns = ['Key', 'Type', 'MOP', 'Letter', 'Number', 'Duration']
        self.maintenance_data['Duration'] = (self.maintenance_data['Duration'] * 3600 * 24).astype('float64') 
        self.maintenance_data = self.maintenance_data.set_index('Key')
        #ASK: Gimana caranya buat index dari 3 kolom? kok dicoba ('Type', 'Letter', 'Number') hasilnya berbeda dgn 'Key' --> labelnya berbeda, ada nomor 1, 2, 3... sedangkan di key ga ada 
        #print(self.maintenance_data.info())
        #print(self.maintenance_data)
    
    #def LoadLastMaintenanceStatus(self):
        self.last_maintenance_status_df = pd.read_excel("Data/Initial Data.xlsx", sheet_name="4. LastMaint", index_col=0)
        self.last_maintenance_status_df['Start date'] = pd.to_datetime(self.last_maintenance_status_df['Start date'].astype(str) + " " + self.last_maintenance_status_df['RevStrtTm'])
        self.last_maintenance_status_df['End date'] = pd.to_datetime(self.last_maintenance_status_df['End date'].astype(str) + " " + self.last_maintenance_status_df['RevEndTm'])
        self.last_maintenance_status_df = self.last_maintenance_status_df.drop(['Revision', 'Hangar', 'RevStrtTm', 'C of A', 'FH', 'FC', 'Interval FH', 'Interval FC', 'A-FH', 'A-FC', 'MAX', 'Previous Description', 'FINAL A'], axis = 1)
        self.last_maintenance_status_df = self.last_maintenance_status_df.set_index('Last Maintenance Code')
        #print(self.last_maintenance_status_df.head())
    
    def LoadIntervalLimitation(self):
        self.interval_limitation_df = pd.read_excel("Data/Initial Data.xlsx", sheetname="5. Limitation", index_col=0)
        self.interval_limitation_df = self.interval_limitation_df.drop['Interval FH', 'Interval DY', 'Interval FC']
        self.interval_limitation_df = self.interval_limitation_df.set_index('Checkpoint')
        #print(self.interval_limitation_df.head())
        
        
    #def LoadMaintenanceInterval(self):    
    
        
    
    #def LoadTowingTime(self):
        
    
        
    #def LoadSlotUtilization(self):
        


