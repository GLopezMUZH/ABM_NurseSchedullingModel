#!/usr/bin/env python
# coding: utf-8

# ### Agent-Based Modelling - FS19
# # ABM Final - Gabriela Lopez & Luca Weibel
# 
# 

# Here are the libraries / configurations used.

# In[1]:
import os
print (os.getcwd())
path = r'C:\Users\glopez\uzh_stuff\MOEC0559AgentBasedModeling\ABM_NurseSchedullingModel'
os.chdir(path)

#%%
#get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')
import importlib
import abm_scheduling
from abm_scheduling import Schedule as Schedule
from abm_scheduling import Nurse as Nurse


#%%
importlib.reload(abm_scheduling)

#%% Initializations
p_to_accept_negative_change = .001

# Situation definition
matrix_nurses_needed = [5,8,5, 4,7,4, 4,7,4, 4,7,5, 5,7,7, 6,7,8, 7,5,5]
matrix_nurse_availability_type1 = ['x','x','', 'x','x','',  'x','x','', 'x','x','', 'x','x','', '','','', '','','']
matrix_nurse_availability_type2 = ['x','x','x', 'x','x','x',  'x','x','x', 'x','x','x', 'x','x','x', '','','', '','','']

# Create Schedule
#schedule_random = Schedule(matrix_nurses_needed=matrix_nurses_needed, is_random=False)
schedule = Schedule(num_nurses_needed=3)

# Create model and nurses
model = abm_scheduling.NSP_AB_Model()
#nurses = model.generate_nurses(10, 0.5, True)
list_nurse_schedules = []
list_nurse_schedules.append(matrix_nurse_availability_type1)
list_nurse_schedules.append(matrix_nurse_availability_type1)
list_nurse_schedules.append(matrix_nurse_availability_type1)
list_nurse_schedules.append(matrix_nurse_availability_type1)
list_nurse_schedules.append(matrix_nurse_availability_type1)
list_nurse_schedules.append(matrix_nurse_availability_type2)
list_nurse_schedules.append(matrix_nurse_availability_type2)
list_nurse_schedules.append(matrix_nurse_availability_type2)
list_nurse_schedules.append(matrix_nurse_availability_type2)
list_nurse_schedules.append(matrix_nurse_availability_type2)
nurses = model.generate_nurses_from_nurse_schedules(list_nurse_schedules)
schedule.print_schedule(schedule_name="Intial Situation")


#%%
model.show_hypothetical_max_schedule(schedule=schedule, nurses=nurses)

#%%
best_schedule, utility_each_timestep, shift_coverage_each_timestep = model.run(schedule=schedule, nurses=nurses, p_to_accept_negative_change=p_to_accept_negative_change)

#%%
model.plot_utility_per_timestep(utility_each_timestep)
model.plot_shift_coverage_per_timestep(shift_coverage_each_timestep)

    