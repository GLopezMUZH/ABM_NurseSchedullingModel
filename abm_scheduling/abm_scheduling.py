#%%
"""
    abm_scheduling is an OpenSource python package for the analysis of
    the Nurse Scheduling Problem using an Agent Based Modeling approach
    based on 
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
from prettytable import PrettyTable
import copy

import matplotlib.pylab as plt
#%matplotlib inline
#plt.style.use('ggplot')

#import warnings
#warnings.filterwarnings('ignore')

#import matplotlib.mlab as mlab
import time
from datetime import datetime

#%%
class Shift():
    def __init__(self, day, shift_num, num_nurses_needed):
        self.day = day
        self.shift_num = shift_num
        self.num_nurses_needed = num_nurses_needed
        self.nurses = []
        
    def get_id_tuple(self):
        return (self.day, self.shift_num)
    
    def get_list_of_nurses_names(self):
        return [n.id_name for n in self.nurses]

#%%
class Schedule():
    num_shifts_per_day = 3
    days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'So']
    
    def __init__(self, num_nurses_needed = 1, matrix_nurses_needed = [], is_random=False):
        self.num_nurses_needed = num_nurses_needed
        self.is_random = is_random
        self.schedule = []
        i = 0
        for day in self.days:
            for shift_num in range(self.num_shifts_per_day):
                if is_random:
                    num_needed = rnd.randint(self.num_nurses_needed + 1) 
                elif len(matrix_nurses_needed) > 0: 
                    num_needed = matrix_nurses_needed[i]
                    i += 1
                else:
                    num_needed = self.num_nurses_needed
                
                self.schedule.append(Shift(day, shift_num + 1, num_needed))
                
    def get_shift_coverage(self):
        total_shifts = 0
        filled_shifts = 0
        for shift in self.schedule:
            total_shifts += shift.num_nurses_needed
            filled_shifts += min(len(shift.nurses), shift.num_nurses_needed)
        return filled_shifts / total_shifts
    
    def add_nurse_to_shift(self, nurse, shift_preference, add_to_nurse):
        idx_in_schedule = self.days.index(shift_preference[0]) * 3 + (shift_preference[1] - 1)
        self.schedule[idx_in_schedule].nurses.append(nurse)
        if add_to_nurse: nurse.shifts.append(shift_preference)
            
    def remove_nurse_from_shift(self, nurse, shift_preference, remove_from_nurse):
        idx_in_schedule = self.days.index(shift_preference[0]) * 3 + (shift_preference[1] - 1)
        for idx, n in enumerate(self.schedule[idx_in_schedule].nurses):
            if n.id_name == nurse.id_name:
                self.schedule[idx_in_schedule].nurses.pop(idx)
        if remove_from_nurse: nurse.shifts.remove(shift_preference)
        
    def get_utility(self, beta=1):
        utility = 0
        nurses_assigned_per_day = {day: [] for day in self.days}
        nurses_days_working = {}
        # evaluating shift capacity (no overbooking shifts)
        for shift in self.schedule:
            if len(shift.nurses) > shift.num_nurses_needed:
                utility -= 1000
            else:
                utility += len(shift.nurses) * 10
            nurses_assigned_per_day[shift.day] += shift.get_list_of_nurses_names()
        # evaluating if multiple shifts on the same day (employees can work max one shift per day)
        for day in nurses_assigned_per_day:
            counts = collections.Counter(nurses_assigned_per_day[day])
            for nurse in counts:
                if counts[nurse] > 1:
                    utility -= 1000
                if nurse in nurses_days_working:
                    nurses_days_working[nurse].append(1)
                else:
                    nurses_days_working[nurse] = [1]
        # evaluating continuous days working (employees cannot work for more than 6 days continuously)
        for nurse in nurses_days_working:
            if len(nurses_days_working[nurse]) >= 7:
                utility -= 1000
        utility *= beta
        return utility

    def print_filled_in_schedule(self, schedule_strs, title=''):
        t = PrettyTable([''] + self.days)
        t.align = 'l'
        for i in range(self.num_shifts_per_day):
            t.add_row([f'shift {i + 1}'] + schedule_strs[i::self.num_shifts_per_day])
        print(title)
        print(t)
                
    def print_schedule(self, schedule_name = ''):
        schedule_strs = []
        for shift in self.schedule:
            nurses_str = ''
            for idx, n in enumerate(shift.get_list_of_nurses_names()):
                if idx % 4 == 0:
                    nurses_str += '\n'
                nurses_str += str(n)
                if idx != len(shift.get_list_of_nurses_names()) - 1:
                    nurses_str += ','
            schedule_strs.append( 
                f"need: {shift.num_nurses_needed}\n"
                f"nurses: {nurses_str}"
            )
        title = "Week's Schedule " + schedule_name
        self.print_filled_in_schedule(schedule_strs, title=title)

    def print_shift_coverage(self, schedule_name = ''):
        schedule_strs = []
        for shift in self.schedule:
            #filled_shifts += min(len(shift.nurses), shift.num_nurses_needed)
            schedule_strs.append( 
                f"need: {shift.num_nurses_needed}\n"
                f"nurses: {len(shift.nurses)}\n"
                f"({(len(shift.nurses) / shift.num_nurses_needed):.3g})"
            )
        title = "Shift Coverage " + schedule_name
        self.print_filled_in_schedule(schedule_strs, title=title)


    """         
    def print_filled_in_schedule(self, schedule_strs, title=''):
        print(title)
        print(len(schedule_strs), schedule_strs)
        schedule_line = " \t "
        i = -2
        for col in range(len(self.days)):
            schedule_line += str(self.days[col]) +  "\t "
        print(schedule_line)

        for row in range(self.num_shifts_per_day):
            schedule_line = str(row) + "\t" 
            for col in range(len(self.days)):
                i += 2
                need_text = schedule_strs[i]
                scheduled_text = schedule_strs[i+1]
                #place = row*len(self.days) + col
                schedule_line += f'{need_text}'
                schedule_line += f'({scheduled_text})' + "\t"                
            print(schedule_line)
            print('{s:{c}^{n}}'.format(s='-',n=60,c='-'))


    def print_schedule(self):
        schedule_strs = []
        for shift in self.schedule:
            #print(shift.day, shift.shift_num)
            nurses_str = ''
            for idx, n in enumerate(shift.get_list_of_nurses_names()):
                if idx % 4 == 0:
                    nurses_str += ','
                nurses_str += str(n)
                if idx != len(shift.get_list_of_nurses_names()) - 1:
                    nurses_str += ','
            schedule_strs.append( 
                f"{shift.num_nurses_needed}"
            )
            schedule_strs.append( 
                f"{nurses_str}"
            )
        print(schedule_strs)
        self.print_filled_in_schedule(schedule_strs, title="Week's Schedule")
    """

#%%
class Nurse():
    def __init__(self, id_name):
        self.id_name = id_name
        self.shift_preferences = []
        self.shifts = []
        self.degree_of_availability = 0
    
    def generate_shift_preferences(self, degree_of_agent_availability, works_weekends):
        schedule = Schedule(0)
        for shift in schedule.schedule:
            if not works_weekends and shift.day in schedule.days[-2:]:
                continue
            if rnd.uniform() < degree_of_agent_availability:
                self.shift_preferences.append((shift.day, shift.shift_num))
                self.degree_of_availability += 1/21

    def assign_shift_preferences(self, matrix_nurse_availability = []):
        schedule = Schedule(0)
        i = -1
        for shift in schedule.schedule:
            i += 1
            if matrix_nurse_availability[i] == 'x':
                self.shift_preferences.append((shift.day, shift.shift_num))
                self.degree_of_availability += 1/21

    def print_shift_preferences(self):
        schedule = Schedule(0)
        schedule_strs = []
        for shift in schedule.schedule:
            if shift.get_id_tuple() in self.shift_preferences:
                schedule_strs.append('x')
            else:
                schedule_strs.append(' ')
        schedule.print_filled_in_schedule(schedule_strs, title=f"Nurse {self.id_name}'s Preferences")

    def get_productivity(self):
        return self.degree_of_availability

    """        
    def print_shift_preferences(self):
        schedule = Schedule(0)
        schedule_strs = []
        for shift in schedule.schedule:
            schedule_strs.append(' ') # empty field for the "needed nurses of the schedule"
            if shift.get_id_tuple() in self.shift_preferences:
                print(shift.get_id_tuple())
                schedule_strs.append('x')
            else:
                schedule_strs.append(' ')
        schedule.print_filled_in_schedule(schedule_strs, title=f"Nurse {self.id_name}'s Preferences")
    """



#%%
class NSP_AB_Model():
    def generate_nurses(self, num_nurses, degree_of_agent_availability, works_weekends):
        nurses = []
        for n in range(num_nurses):
            nurse = Nurse(id_name=n)
            nurse.generate_shift_preferences(degree_of_agent_availability, works_weekends)
            nurses.append(nurse)
        return nurses
    
    def generate_nurses_from_nurse_schedules(self, list_of_nurse_schedules):
        nurses = []
        i = -1
        for s in list_of_nurse_schedules:
            i += 1
            nurse = Nurse(id_name=i)
            nurse.assign_shift_preferences(s)
            nurses.append(nurse)
        return nurses

