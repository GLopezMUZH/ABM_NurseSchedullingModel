#%%
"""
    bowtievisualization is an OpenSource python package for the analysis of
    networkx networks under the bow-tie structure analysis
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.
"""
#%config IPCompleter.greedy=True

import networkx as nx
import numpy as np
import numpy.random as rnd
import collections
import math as m
#from prettytable import PrettyTable

import matplotlib.pylab as plt
#%matplotlib inline
#plt.style.use('ggplot')

#import warnings
#warnings.filterwarnings('ignore')

#import matplotlib.mlab as mlab
import time
from datetime import datetime


class Shift():
    def __init__(self, day, shift_num, num_nurses_needed):
        self.day = day
        self.shift_num = shift_num
        self.num_nurses_needed = num_nurses_needed
        self.nurses = []
        self.is_fulfilled = False
        
    def get_id_tuple(self):
        return (self.day, self.shift_num)

    
class Schedule():
    num_shifts_per_day = 3
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    def __init__(self, num_nurses_needed, is_random=False):
        self.num_nurses_needed = num_nurses_needed
        self.is_random = is_random
        self.schedule = []
        for day in self.days:
            for shift_num in range(self.num_shifts_per_day):
                num_needed = rnd.randint(self.num_nurses_needed + 1) if is_random else self.num_nurses_needed
                self.schedule.append(Shift(day, shift_num + 1, num_needed))
                
    def get_shift_coverage(self):
        total_shifts = 0
        filled_shifts = 0
        for shift in self.schedule:
            total_shifts += shift.num_nurses_needed
            filled_shifts += min(len(shift.nurses), shift.num_nurses_needed)
        return filled_shifts / total_shifts
    
    def print_filled_in_schedule(self, schedule_strs, title=''):
        t = PrettyTable([''] + self.days)
        t.align = 'l'
        for i in range(self.num_shifts_per_day):
            t.add_row([f'shift {i + 1}'] + schedule_strs[i::self.num_shifts_per_day])
        print(title)
        print(t)
                
    def print_schedule(self):
        schedule_strs = []
        for shift in self.schedule:
            schedule_strs.append( 
                f'need: {shift.num_nurses_needed}\n'
                f'nurses: {shift.nurses}'
            )
        self.print_filled_in_schedule(schedule_strs, title="Week's Schedule")
    
class Nurse():
    def __init__(self, id_name):
        self.id_name = id_name
        self.shift_preferences = []
        self.shifts = []
        
    def generate_shift_preferences(self, degree_of_agent_availability, works_weekends):
        schedule = Schedule(0)
        for shift in schedule.schedule:
            if not works_weekends and shift.day in schedule.days[-2:]:
                continue
            if rnd.uniform() < degree_of_agent_availability:
                self.shift_preferences.append((shift.day, shift.shift_num))
    
    def print_shift_preferences(self):
        schedule = Schedule(0)
        schedule_strs = []
        for shift in schedule.schedule:
            if shift.get_id_tuple() in self.shift_preferences:
                schedule_strs.append('x')
            else:
                schedule_strs.append(' ')
        schedule.print_filled_in_schedule(schedule_strs, title=f"Nurse {self.id_name}'s Preferences")
