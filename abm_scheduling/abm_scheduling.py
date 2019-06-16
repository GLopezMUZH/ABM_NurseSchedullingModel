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
import math
from prettytable import PrettyTable
from random import shuffle
import copy

import matplotlib.pylab as plt
from scipy.integrate import simps
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

class Utility_Function_Parameters():
    def __init__(self):
        self.utility_function = 'default'
        self.penalty_overbooking = 1000
        self.penalty_multiple_shifts_one_day = 1000
        self.penalty_max_continuous_days_working = 1000

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
                    num_needed = int(rnd.normal(self.num_nurses_needed + 1)) 
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
                f"({(len(shift.nurses) / max(shift.num_nurses_needed,1)):.3g})"
            )
        title = "Shift Coverage " + schedule_name
        self.print_filled_in_schedule(schedule_strs, title=title)


#%%
class Nurse():
    max_working_days = 6

    def __init__(self, id_name):
        """
        Generated with default Agent Satisfaction Parameters
        """
        self.id_name = id_name
        self.shift_preferences = []
        self.shifts = []
        self.degree_of_availability = 0
        self.minimum_shifts = 0
        self.maximum_shifts = 0
        # Agent_Satisfaction_Parameters()
        self.satisfaction_function = 'default'
        self.base_decrease_coverage_satisfaction = 0.8
        self.gain_over_increase_assignment = 0
        self.value_under_assignment = 1000
        self.value_over_assignment = 1000
        self.penalty_different_shifts_in_week = 700
        self.penalty_wrong_shift_assigment = 700

    
    def generate_shift_preferences(self, degree_of_agent_availability, works_weekends):
        schedule = Schedule(0)
        for shift in schedule.schedule:
            if not works_weekends and shift.day in schedule.days[-2:]:
                continue
            if rnd.uniform() < degree_of_agent_availability:
                self.shift_preferences.append((shift.day, shift.shift_num))
        self.degree_of_availability = degree_of_agent_availability
        self.minimum_shifts = min(round(self.degree_of_availability*21,0), self.max_working_days)
        self.maximum_shifts = min(round(self.degree_of_availability*21,0), self.max_working_days)
        self.gain_over_increase_assignment = 1000/self.minimum_shifts
        self.sensibility_to_increase_assignment = 7 - self.maximum_shifts #TODO tune


    def assign_shift_preferences(self, matrix_nurse_availability = [], minimum_shifts = 0, maximum_shifts = 0):
        schedule = Schedule(0)
        i = -1
        for shift in schedule.schedule:
            i += 1
            if matrix_nurse_availability[i] == 'x':
                self.shift_preferences.append((shift.day, shift.shift_num))
                self.degree_of_availability += 1/21
        self.minimum_shifts = min(round(self.degree_of_availability*21,0), self.max_working_days) if minimum_shifts == 0 else minimum_shifts
        self.maximum_shifts = min(round(self.degree_of_availability*21,0), self.max_working_days) if maximum_shifts == 0 else maximum_shifts
        self.gain_over_increase_assignment = 1000/(np.mean([self.minimum_shifts,self.maximum_shifts]))
        self.sensibility_to_increase_assignment = 7 - self.maximum_shifts #TODO tune

    def print_shift_preferences(self):
        schedule = Schedule(0)
        schedule_strs = []
        for shift in schedule.schedule:
            if shift.get_id_tuple() in self.shift_preferences:
                schedule_strs.append('x')
            else:
                schedule_strs.append(' ')
        title = f"Nurse {self.id_name}'s Preferences. Availability: " + f"({self.degree_of_availability:.3g})" + "Min/Max: " + str(self.minimum_shifts) +"/" +str(self.maximum_shifts) 
        schedule.print_filled_in_schedule(schedule_strs, title=title)

    def print_assigned_shifts(self):
        schedule = Schedule(0)
        schedule_strs = []
        for shift in schedule.schedule:
            if shift.get_id_tuple() in self.shifts:
                schedule_strs.append('1')
            else:
                schedule_strs.append(' ')
        schedule.print_filled_in_schedule(schedule_strs, title=f"Nurse {self.id_name}'s Assigned Shifts")
    
    def get_satisfaction(self):
        if self.satisfaction_function == 'default':
            return self.get_satisfaction_default_function()
        return 1

    def get_satisfaction_default_function(self):
        """
        Default function for agent satisfaction that accounts for:
        - coverage of minimum and maximum desired shift assignments, 
        - satisfaction for new shift assignment decreases incrementally as coverages approaches the maximum
        """
        # formula for satisfaction from shift assignment = 
        # base_decrease_coverage_satisfaction ^ (number_shifts - sensibility_to_increase_assignment)
        # x = assigned shifts
        s = lambda x: pow(self.base_decrease_coverage_satisfaction, (x - self.sensibility_to_increase_assignment))

        nr_shifts = len(self.shifts)
        cummulated_satisfaction_from_assigned_shifts = 0
        rate_under_assignment = (-1 + nr_shifts/self.minimum_shifts)
        rate_over_assignment = (self.maximum_shifts - nr_shifts)/self.maximum_shifts
        # matching_assigned_shifts = len(set(self.shifts).intersection(self.shift_preferences))
        # penalty when under assignment
        cummulated_satisfaction_from_assigned_shifts += self.value_under_assignment * min(0, rate_under_assignment)
        # penalty when over assignment
        cummulated_satisfaction_from_assigned_shifts += self.value_over_assignment * min(0, rate_over_assignment)
        # increase satisfaction on number of matching assigned shifts
        # we asume all assigned shifts here match because they are choosen only from their preferences
        if nr_shifts <=self.maximum_shifts: 
            x_vals = np.array(list(range(nr_shifts)))
            cummulated_satisfaction_from_assigned_shifts += self.gain_over_increase_assignment * sum(s(x_vals))
        
        return cummulated_satisfaction_from_assigned_shifts

    def get_satisfaction_shift_stability_function(self):
        """
        Function for agent satisfaction that accounts for:
        - coverage of minimum and maximum desired shift assignments, 
        - shift stability as in preferred constant shift number assignment during the week
        """
        # TODO
        productivity = len(self.shifts)
        return 1


class NSP_AB_Model_Run_Results():
    beta = 0
    p_to_accept_negative_change = 0
    best_schedule = []
    utility_each_timestep = []
    shift_coverage_each_timestep = []
    shift_coverage = 0
    utility = 0
    utility_function = ''
    total_agent_satisfaction = 0
    nurses = []


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

    def show_hypothetical_max_schedule(self, schedule, nurses):
        # show what all shift preferences look like in the schedule
        hypothetical_max_schedule = copy.deepcopy(schedule)
        for nurse in nurses:
            for shift in nurse.shift_preferences:
                hypothetical_max_schedule.add_nurse_to_shift(nurse, shift, False)
                
        hypothetical_max_schedule.print_schedule(schedule_name="Hypothetical Maximum")
        print('Crude hypothetical shift coverage:', hypothetical_max_schedule.get_shift_coverage())
        hypothetical_max_schedule.print_shift_coverage(schedule_name="Hypothetical Maximum")

    def get_utility(self, schedule: Schedule, nurses: [Nurse], utility_function_parameters: Utility_Function_Parameters, beta=0.9):
        if utility_function_parameters.utility_function == 'default':
            return self.get_utility_default(schedule = schedule, utility_function_parameters=utility_function_parameters, beta=beta)
        if utility_function_parameters.utility_function == 'agent_satisfaction':
            return self.get_utility_agent_satisfaction(schedule = schedule, nurses=nurses, utility_function_parameters=utility_function_parameters, beta=beta)

    def get_utility_default(self, schedule: Schedule, utility_function_parameters: Utility_Function_Parameters,  beta=0.9):
        """
        Default utility function for the Shift assignment considering:
        - negative penalty for overbooking on the shifts
        - negative penalty for assigning shifts on the same day of one agent
        - negative penalty for exeding the maximum continuous working days of one agent 
        Parameters
        ----------
        beta : input float (default: 0)
            Racionality of the agent to always choose only the best utility
        """
        utility = 0
        nurses_assigned_per_day = {day: [] for day in schedule.days}
        nurses_days_working = {}
        # evaluating shift capacity (no overbooking shifts)
        for shift in schedule.schedule:
            if len(shift.nurses) > shift.num_nurses_needed:
                utility -= utility_function_parameters.penalty_overbooking
            else:
                utility += len(shift.nurses) * 10
            nurses_assigned_per_day[shift.day] += shift.get_list_of_nurses_names()
        # evaluating if multiple shifts on the same day (employees can work max one shift per day)
        for day in nurses_assigned_per_day:
            counts = collections.Counter(nurses_assigned_per_day[day])
            for nurse in counts:
                if counts[nurse] > 1:
                    utility -= utility_function_parameters.penalty_multiple_shifts_one_day
                if nurse in nurses_days_working:
                    nurses_days_working[nurse].append(1)
                else:
                    nurses_days_working[nurse] = [1]
        # evaluating continuous days working (employees cannot work for more than 6 days continuously)
        for nurse in nurses_days_working:
            if len(nurses_days_working[nurse]) >= 7:
                utility -= utility_function_parameters.penalty_max_continuous_days_working
        utility *= beta
        return utility

    def get_utility_detect_overstaffing(self, utility_function_parameters: Utility_Function_Parameters,  beta=0.9):
        utility = 0
        return utility

    def get_utility_agent_satisfaction(self, schedule: Schedule, nurses: [Nurse], utility_function_parameters: Utility_Function_Parameters,  beta=0.9):
        """
        Utility function for the Shift assignment considering:
        - negative penalty for overbooking on the shifts
        - negative penalty for assigning shifts on the same day of one agent
        - negative penalty for exeding the maximum continuous working days of one agent 
        - negative/positive value for agent_satisfaction
        Parameters
        ----------
        beta : input float (default: 0)
            Racionality of the agent to always choose only the best utility
        """
        utility = 0
        nurses_assigned_per_day = {day: [] for day in schedule.days}
        nurses_days_working = {}
        # evaluating shift capacity (no overbooking shifts)
        for shift in schedule.schedule:
            if len(shift.nurses) > shift.num_nurses_needed:
                utility -= utility_function_parameters.penalty_overbooking
            else:
                utility += len(shift.nurses) * 10
            nurses_assigned_per_day[shift.day] += shift.get_list_of_nurses_names()
        # evaluating if multiple shifts on the same day (employees can work max one shift per day)
        for day in nurses_assigned_per_day:
            counts = collections.Counter(nurses_assigned_per_day[day])
            for nurse in counts:
                if counts[nurse] > 1:
                    utility -= utility_function_parameters.penalty_multiple_shifts_one_day
                if nurse in nurses_days_working:
                    nurses_days_working[nurse].append(1)
                else:
                    nurses_days_working[nurse] = [1]
        # evaluating continuous days working (employees cannot work for more than 6 days continuously)
        for nurse in nurses_days_working:
            if len(nurses_days_working[nurse]) >= 7:
                utility -= utility_function_parameters.penalty_max_continuous_days_working
        # evaluating nurse satisfaction
        for nurse in nurses:
            utility += nurse.get_satisfaction()/len(nurses)
        utility *= beta
        return utility


    def run(self, schedule_org: Schedule, nurses_org: [Nurse], utility_function_parameters: Utility_Function_Parameters, beta=0.9, p_to_accept_negative_change = .001, timesteps=10000, print_stats=True):
        best_utility = 0
        utility_each_timestep = []
        shift_coverage_each_timestep = []

        nurses = copy.deepcopy(nurses_org)
        schedule = copy.deepcopy(schedule_org)
        candidate_schedule = copy.deepcopy(schedule)
        best_schedule = copy.deepcopy(schedule)

        if utility_function_parameters is None:
            utility_function_parameters = Utility_Function_Parameters()

        # timestep is for each nurse, so total timesteps = x * num_nurses where x is range(x)
        for timestep in range(timesteps):
            shuffle(nurses)
            for nurse in nurses:
                schedule_utility = self.get_utility(schedule=schedule, nurses=nurses, beta=beta, utility_function_parameters=utility_function_parameters)
                utility_each_timestep.append(schedule_utility)
                shift_coverage_each_timestep.append(schedule.get_shift_coverage())
                # keep track of best utility
                if schedule_utility > best_utility:
                    best_schedule.schedule = copy.deepcopy(schedule.schedule)
                    best_utility = schedule_utility
                rnd_i = rnd.randint(len(nurse.shift_preferences))
                rnd_shift_pref = nurse.shift_preferences[rnd_i]
                was_in_shift = rnd_shift_pref in nurse.shifts
                # try adding/removing shift depending on whether the shift is assigned
                if not was_in_shift:
                    candidate_schedule.add_nurse_to_shift(nurse, rnd_shift_pref, False)
                else:
                    candidate_schedule.remove_nurse_from_shift(nurse, rnd_shift_pref, False)
                # if the change was better or randomly accept negative change, apply change to schedule
                if (self.get_utility(schedule=candidate_schedule, nurses=nurses, beta=beta, utility_function_parameters=utility_function_parameters) > schedule_utility) or (rnd.random_sample() < p_to_accept_negative_change):
                    if not was_in_shift:
                        schedule.add_nurse_to_shift(nurse, rnd_shift_pref, True)
                    else:
                        schedule.remove_nurse_from_shift(nurse, rnd_shift_pref, True)
                # if the change was worse, undo the change to the candidate schedule
                else:
                    if not was_in_shift:
                        candidate_schedule.remove_nurse_from_shift(nurse, rnd_shift_pref, False)
                    else:
                        candidate_schedule.add_nurse_to_shift(nurse, rnd_shift_pref, False)

        schedule_name = 'Best Schedule. Beta: ' + f"({beta:.2g})" + ',p: 'f"({p_to_accept_negative_change:.3g})"
        results = NSP_AB_Model_Run_Results()
        results.beta = beta
        results.p_to_accept_negative_change = p_to_accept_negative_change
        results.shift_coverage = best_schedule.get_shift_coverage()
        results.utility = self.get_utility(schedule=best_schedule, nurses=nurses, beta=beta, utility_function_parameters=utility_function_parameters)
        results.best_schedule = best_schedule
        results.utility_each_timestep = utility_each_timestep
        results.shift_coverage_each_timestep = shift_coverage_each_timestep
        results.total_agent_satisfaction = self.get_total_agent_satisfaction(nurses=nurses)
        results.nurses = nurses

        if print_stats:
            best_schedule.print_schedule(schedule_name=schedule_name)
            print('Solution shift coverage:', results.shift_coverage)
            print('Solution utility: ', results.utility)
            print('Agent satisfaction: ', results.total_agent_satisfaction)

        return results

    def get_total_agent_satisfaction(self, nurses: [Nurse]):
        total_satisfaction = 0
        for nurse in nurses:
            total_satisfaction += nurse.get_satisfaction()
        return total_satisfaction
        

    def print_nurse_productivity(self, nurses: [Nurse], schedule_name = ''):
        def getNurseId(item):
            return item.id_name

        nrs_str = ""
        nrs = sorted(nurses, key=getNurseId)
        print("Nurse productivity - ", schedule_name)
        for nurse in nrs:
            nrs_str = ""
            #TODO rpad idname to x characters
            nrs_str += "Nr: " + str(nurse.id_name) + ", \t"
            nrs_str += "assigned:" + str(len(nurse.shifts)) + ",\t"
            nrs_str += "min:" + "%.0f" % nurse.minimum_shifts + ",\t"
            nrs_str += "max: " + "%.0f" % nurse.maximum_shifts + ",\t"
            nrs_str += "deg.availab:" + "%.2f" % nurse.degree_of_availability + ",\t"
            nrs_str += "prod: " + "%.2f" % (len(nurse.shifts) / nurse.minimum_shifts) + ",\t"
            nrs_str += "satisf: " + "%.2f" % (nurse.get_satisfaction())
            print(nrs_str)


    
    def plot_utility_per_timestep(self, utility_each_timestep):
        plt.figure()
        plt.plot(utility_each_timestep, label = "utility")
        plt.title("Schedule utility of each timestep")
        plt.xlabel("timestep")
        plt.ylabel("utility")
        plt.legend()
        plt.show()

    def plot_shift_coverage_per_timestep(self,shift_coverage_each_timestep):
        plt.figure()
        plt.plot(shift_coverage_each_timestep, label = "shift coverage")
        plt.title("Shift coverage of each timestep")
        plt.xlabel("timestep")
        plt.ylabel("shift coverage")
        plt.legend()
        plt.show()