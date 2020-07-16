# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from Maintenance import *

class MaintenanceDatabase:
    def __init__(self, T, K):
        #t type
        #k letter
        self.T = T
        self.K = K
        self.maintenance = {}
        for t in T:
            self.maintenance[t] = {}
            for k in K:
                self.maintenance[t][k] = Maintenance(t,k)
                
    def UpdateMaintenanceDuration(self, maintenance_data_df):
        for t in self.T:
            for k in self.K:
                checks_by_t_and_k = maintenance_data_df[np.logical_and(maintenance_data_df['Type'] == t, maintenance_data_df['Letter'] == k)]
                if(len(checks_by_t_and_k) == 0):
                    self.maintenance[t][k].durations = np.nan
                else:
                    for index, row in checks_by_t_and_k.iterrows():
                        self.maintenance[t][k].durations[row['Number']] = row['Duration']
        

    def LastMaintenance (self, I, T, K): #last_maintenance_status_df, MOP
        self.MOP = {} #awal MOP semua aircraft
        #MOP[I] = str(K) + last_maintenance_status_df('Number') --> last MOP[i]
        #Hasilnya jadi bentuk tabel dengan kolom seperti:
        #1. aircraft
        #2. aircraft type
        #3. Last MOP A 
        #4. Last MOP C
        #5. Last MOP D (Hanya A330: Jika aircraft type tidak pakai D, masukkan nilai nan)
        #6. Last MOP 2Y (Hanya ATR: Jika aircraft type tidak pakai 2Y, masukkan nilai nan)
        #7. Last MOP 4000FC (Hanya NG: Jika aircraft type tidak pakai 4000FC, masukkan nilai nan)
        #8. Last MOP 8C (Hanya A330?: Jika aircraft type tidak pakai 8C, masukkan nilai nan)
        #9. FH awal --> masukkan nilai FH di initial FH (initial aircraft status)
        #10. FC awal --> masukkan nilai FC di initial FC (initial aircraft status)
        #11. FD awal --> masukkan tanggal 31 Desember 2018
        #define urgency_rate_var (variabel ada di MIP Gurobi) di sini:
            #12. masukkan kolom initial_urgency_rate_var A[I] = 0 (atau nan jika tidak pakai) (initial)
            #13. masukkan kolom initial_urgency_rate_var C[I] = 0 (atau nan jika tidak pakai)(initial)
            #14. masukkan kolom initial_urgency_rate_var D[I] = 0 (atau nan jika tidak pakai)(initial)
            #15. masukkan kolom initial_urgency_rate_var 2Y[I] = 0 (atau nan jika tidak pakai)(initial)
            #16. masukkan kolom initial_urgency_rate_var 4000FC[I] = 0 (atau nan jika tidak pakai)(initial)
            #17. masukkan kolom initial_urgency_rate_var 8C[I] = 0 (atau nan jika tidak pakai)(initial)
        
    
    def UpdateMOP(self, I): #flight_schedule_df, FH[i][d], FC[i][d], FD[i][d], interval[FH][FC] 
        pass
        #self.MOP =
        #masukkan 17 kolom di atas untuk update-an
        #Untuk kolom nomor 9, 10, 11: FH, FC, FD akan diupdate sesuai scheduling
        #Untuk updatean kolom nomor 12, 13, 14, 15, 16, 17: urgency_rate_var nanti aja hitungannya
        
    def Penalty (self,I, K, D): 
        pass
        ##PR: grounded_penalty = pg = Biaya penalty = biaya operasional 1 hari / biaya per FH untuk pengerjaan maintenance 
        #PR2: Atau pg = Big M 
        ##tolerance_penalty = pa = biaya administratif (ex: 3 million IDR/ biaya per FH untuk pengerjaan maintenance)
        
    
    
