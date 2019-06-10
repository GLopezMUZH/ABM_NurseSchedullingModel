#%%
import os
print (os.getcwd())
path = r'C:\Users\glopez\uzh_stuff\MOEC0559AgentBasedModeling\ABM_NurseSchedullingModel'
os.chdir(path)

#%%
import abm_scheduling
from abm_scheduling import Schedule as Schedule
from abm_scheduling import Nurse as Nurse

# --example schedules--
schedule_fixed = Schedule(num_nurses_needed=3)
schedule_fixed.print_schedule()


# In[4]:
schedule_random = Schedule(num_nurses_needed=3, is_random=True)
schedule_random.print_schedule()


#%% Defined numbers
# Mo 1,2,3, Tu 1,2,3, We...
matrix_nurses_needed = [5,8,5, 4,7,4, 4,7,4, 4,7,5, 5,7,7, 6,7,8, 7,5,5]
schedule_random = Schedule(matrix_nurses_needed=matrix_nurses_needed, is_random=False)
schedule_random.print_schedule()

"""
-- NURSE GENERATION EXAMPLES --
"""
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
nurse.generate_shift_preferences(degree_of_agent_availability=0.78, works_weekends=False)
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

#%% Defined 1st and 2nd shift work days
# Mo 1,2,3, Tu 1,2,3, We...
matrix_nurse_availability = ['x','x','', 'x','x','',  'x','x','', 'x','x','', 'x','x','', '','','', '','','']
nurse = Nurse(id_name=5)
nurse.assign_shift_preferences(matrix_nurse_availability=matrix_nurse_availability, minimum_shifts=5, maximum_shifts=5)
nurse.print_shift_preferences()

#%%
# -- example agent satisfaction 
matrix_nurse_availability = ['x','x','', 'x','x','',  'x','x','', 'x','x','', 'x','x','', '','','', '','','']
nurse = Nurse(id_name=5)
nurse.assign_shift_preferences(matrix_nurse_availability=matrix_nurse_availability, minimum_shifts=5, maximum_shifts=5)
nurse.print_shift_preferences()
nurse.shifts.append(('Mo',1))#(shift.day, shift.shift_num)
nurse.shifts.append(('Mo',2))#(shift.day, shift.shift_num)
nurse.shifts.append(('Mo',3))#(shift.day, shift.shift_num)
nurse.print_assigned_shifts()
print("Nurse satisfaction, function: ", nurse.satisfaction_parameters.satisfaction_function, ": ", nurse.get_satisfaction())

#%%
