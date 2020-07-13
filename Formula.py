import pandas as pd
import itertools as it
#import gurobipy as gp
#from gurobipy import *

class Formula:
    def CalculateUrgencyRate(FH, FC, current_date, last_maintenance_FH, last_main):
        return 0
    
    def IsTimeEnough(start_time, end_time, duration):
        difference = end_time - start_time
        total_seconds = difference.total_seconds()
        return duration <= total_seconds
 
    def FormulaRuth(aircraft_profile, all_schedule, hangar_profile, initial_aircraft_status, maintenance_data):
        #Create empty Model
        #m = Model()     
        
        #Load the data
        #dataframe only has 8341 rows x 6 columns
        
        
        #Define sets and indexes
        #index: aircraft
        aircraft = aircraft_profile['Registration']
        #index: aircraft type
        aircraft_type = aircraft_profile['Type']
        #index: hangar
        hangar = hangar_profile['Unique Code']
        hangar_type = hangar_profile['Workshop Type']
        #index: maintenance check: dict_type_checks
        unique_aircraft_types = aircraft_profile['Type'].unique()
        dict_type_checks = {}
        hasil = Aircraft.Checks('type apa')
        for unique_aircraft_type in unique_aircraft_types:
            aircraft_type_checks_df = maintenance_data[maintenance_data['Type'] == unique_aircraft_type]
            all_aircraft_maintenance_unique_letters = aircraft_type_checks_df['Letter'].unique()
            aircraft_check_codes = []
            for all_aircraft_maintenance_unique_letter in all_aircraft_maintenance_unique_letters:
                aircraft_check_codes.append(unique_aircraft_type + "_" + all_aircraft_maintenance_unique_letter)
            dict_type_checks[unique_aircraft_type] = aircraft_check_codes
        #print(dict_type_checks)
        #index: cities, outstations (initial)
        
    
 
 
 
 #       print(hangar.head())       
        
        
        
        
        
        #Preprocessing
        #fh_init = maintdata['Initial FH']
        
        
        #name of routes
        
        #for i in aircraft, 
        #time
        
        #Define parameters
        
        
        
        #Define decision variables
        #The variable template: addVar (lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS, name="", column=None )
        #x = [[model.add_var(name="x({} ,{})".format(j, t), var_type=BINARY) for t in T] for j in J]
      #  y_iabr = m.addVar(vtype=GRB.BINARY, name="y_start_to_end") 
        #jelasin i,a,b,r
    #    y_ibcr = m.addVar(vtype=GRB.BINARY, name='y_end_to_start') 
        #jelasin i,b,c,r
    #    w_ik = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='w_usage_rate') 
        #jelasin i,k
     #   x_ikdb = m.addVar(vtype=GRB.BINARY, name="x_premature_requirement")
        #jelasin i,k,d,b
      #  gam_ikdb = m.addVar(vtype=GRB.BINARY, name="gam_all_check")
        #jelasin i,k,d,b
      #  o_khdb = m.addVar(vtype=GRB.BINARY, name="o_hangar_check")
        #jelasin k,h,d,b
      #  n_kid = m.addVar(vtype=GRB.BINARY, name="n_grounded")
        #jelasin k,i,d
      #  dy_kid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="dy_total_day")
        #jelasin k,i,d
    #    fh_kid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="fh_total_fh")
        #jelasin k,i,d
     #   fc_kid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="fh_total_fc")
        #jelasin k,i,d
     #   e_kdyid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="e_extra_day")
        #jelasin k,dy,i,d
     #   e_kfhid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="e_extra_fh")
        #jelasin k,fh,i,d
    #    e_kfcid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="e_extra_fc")
        #jelasin k,fc,i,d
   #     teta_kid = m.addVar(lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name="teta_tolerance_rate")
        #jelasin k,i,d
        
    #    latest = GetLatestCheck("G330_C_Check")
        
        
        #Set objective function
        
        
        #Create linear expressions and use them to create constraints
        
        
        #Call optimize()

        def GetLatestCheck(code_check):
            return 0