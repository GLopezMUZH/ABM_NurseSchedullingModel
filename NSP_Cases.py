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
import numpy.random as rnd
import importlib
import abm_scheduling
from prettytable import PrettyTable
from abm_scheduling import Schedule as Schedule
from abm_scheduling import Nurse as Nurse


#%%
importlib.reload(abm_scheduling)


#%%
# --example schedules--
schedule_fixed = Schedule(num_nurses_needed=3)
schedule_fixed.print_schedule()


# In[4]:
schedule_random = Schedule(num_nurses_needed=3, is_random=True)
schedule_random.print_schedule()


#%%
# --example nurses--
# full time, no weekends
nurse = Nurse(id_name=0)
nurse.generate_shift_preferences(degree_of_agent_availability=1, works_weekends=False)
nurse.print_shift_preferences()

#%%
# full time, weekends
nurse = Nurse(id_name=1)
nurse.generate_shift_preferences(degree_of_agent_availability=1, works_weekends=True)
nurse.print_shift_preferences()

# part time, no weekends
nurse = Nurse(id_name=2)
nurse.generate_shift_preferences(degree_of_agent_availability=0.5, works_weekends=False)
nurse.print_shift_preferences()

# part time, weekends
nurse = Nurse(id_name=3)
nurse.generate_shift_preferences(degree_of_agent_availability=0.5, works_weekends=True)
nurse.print_shift_preferences()

# --example generating nurses--
# generate 10 nurses that work 50% and on weekends
nurses = []
num_nurses = 10
for n in range(num_nurses):
    nurse = Nurse(id_name=n)
    nurse.generate_shift_preferences(degree_of_agent_availability=0.5, works_weekends=True)
    nurses.append(nurse)
