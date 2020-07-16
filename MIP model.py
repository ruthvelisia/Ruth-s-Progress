import pandas as pd
import itertools as it
import gurobipy as gp
from gurobipy import Model
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

    
def FormulaRuth(aircraft_profile, all_schedule, effective_slot, hangar_profile, initial_aircraft_status, interval_limitation, last_maintenance_status, maintenance_data, maintenance_interval, maintenance_status_31_Dec, towing_time):
     
    #Define index
    #i = index of aircraft registration
    #d = index of calendar day
    #t = index of aircraft_profile
    #city = index of city
    #h = index of hangar
    #k = index of maintenance type check
    #intv = index of interval type
    #d = index of calendar day
    #tk = index of aircraft type and maintenance type
    
    #Define sets
    I = aircraft_profile['Registration'] #set of aircraft registration
    N = len(aircraft_profile['Registration']) #number of aircraft fleet
    T = aircraft_profile['Type'].unique() #set of aircraft types
    dict_type_checks = {}
    hasil = Aircraft.Checks('type apa')
    for unique_aircraft_type in t:
        aircraft_type_checks_df = maintenance_data_df[maintenance_data_df['Type'] == unique_aircraft_type]
        all_aircraft_maintenance_unique_letters = aircraft_type_checks_df['Letter'].unique()
        aircraft_check_codes = []
        for all_aircraft_maintenance_unique_letter in all_aircraft_maintenance_unique_letters:
            aircraft_check_codes.append(unique_aircraft_type + "_" + all_aircraft_maintenance_unique_letter)
            dict_type_checks[unique_aircraft_type] = aircraft_check_codes
    CITY = hangar_profile['City'].unique() #set of city
    H = hangar_profile['Hangar Code']  #set of hangar code
    K = initial_data.maintenance_data_df['Letter'].unique() #set of maintenance type check
    INTV =  ['FH', 'FC', 'DY'] #set of interval types
    D = initial_data.initial_flight_schedule_df['End Date'].unique() #set of calendar day indicator
    F = all_schedule['Start Loc'] #set of node a
    G = all_schedule['End Loc'] #set of node b
    nc = sum(len(F) + len(G)) #set of nodes a and b


