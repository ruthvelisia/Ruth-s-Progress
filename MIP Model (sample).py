import pandas as pd
import itertools as it
import datetime
from datetime import date
from datetime import timedelta
import calendar
import numpy as np
from InitialData import *
from AircraftDatabase import *
from HangarDatabase import *
from Workshop import *
from MaintenanceDatabase import *

initial_data = InitialData()
initial_data.LoadAllFile()

#I = initial_data.aircraft_profile_df.index.values
I = ['PK-GLA', 'PK-GMN', 'PK-GAK']
T = initial_data.aircraft_profile_df['Type'].unique()
K = initial_data.maintenance_data_df['Letter'].unique()
D = initial_data.initial_flight_schedule_df['End Date'].unique() #calendar day indicator
CITY = initial_data.hangar_profile_df['City'].unique()
H = initial_data.hangar_profile_df.index.values

aircraft_database = AircraftDatabase(I, initial_data.aircraft_profile_df)
aircraft_database.UpdatePerDayData(D, initial_data.aircraft_profile_df, initial_data.aircraft_status_df, initial_data.initial_flight_schedule_df)
aircraft_database.UpdateLimitMaintenanceData(K, initial_data.aircraft_profile_df, initial_data.interval_limitation_df)
aircraft_database.UpdateAverageUtilizationData(initial_data.aircraft_profile_df)
aircraft_database.UpdateIntervalCheckData(K, initial_data.aircraft_profile_df, initial_data.maintenance_interval_df)    
aircraft_database.UpdateLastMaintenance(K, initial_data.last_maintenance_status_df)

hangar_database = HangarDatabase(H,CITY, initial_data.hangar_profile_df)
hangar_database.UpdateUsedSlot(initial_data.initial_maintenance_status_df)

maintenance_database = MaintenanceDatabase(T, K)
maintenance_database.UpdateMaintenanceDuration(initial_data.maintenance_data_df)

#for workshop in hangar_database.Workshops['CGK']:
#    print(workshop.towing_time)