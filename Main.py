# -*- coding: utf-8 -*-
from InitialData import *
from Hangar import *

initial_data = InitialData()
initial_data.LoadAllFile()

hangars = Hangar(initial_data.hangar_profile_df)
for index, row in initial_data.initial_maintenance_status_df.iterrows():
    hangars.ForceMaintenance(row['Workshop'], row['Registration'], row['Aircraft Check'], row['From'], row['To'])