## For lecture paper
**0. Nurse availability levels**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements normal distribution around 5 nurses/shift
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage over Nurse availability starting from 0 to 5times shift requirements

**1. Impact of p_negative**

Situation: 
- 70% agent availability on weekdays and weekends

Task:
- Evaluate Shift Coverage over p_negative: [.001, .0025, .005, .0075, .01, .02, .03, .05, .1, .2]
- Evaluate Agent Satisfaction over p_negative: [.001, .0025, .005, .0075, .01, .02, .03, .05, .1, .2]

**2. Impact of Agent satisfaction sensibility on under-assignment**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements normal distribution around 5 nurses/shift
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage over Agent satisfaction penalty for under-assignment
- Evaluate Agent Satisfaction over Agent satisfaction penalty for under-assignment using default function and shift stability function

**3. Impact of Agent satisfaction sensibility on shift stability (different_shifts_in_week)**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage over Agent satisfaction penalty for shift stability
- Evaluate Agent Satisfaction over Agent satisfaction penalty for shift stability using shift stability function

**4. Utility function that maximizes uniform shift assignment distribition to agents**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage over ??
- Evaluate Agent Satisfaction over ??


**5. Utility function that reduces overstaffing of agents**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- p_to_accept_negative_change=.001
- Maximal number of nurses required in one shift = 7

Task:
- Evaluate Shift Coverage over Number of Nurses
- Evaluate Agent Satisfaction over Number of Nurses using default function and shift stability function

Expected results:
- Several nurses will have a very low degree of satisfaction (the over-staffed)

**6. Impact of Agent Availability(fragmentation) on Shift Coverage**

Situation: 
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage over Agent Availability using Utility function for Uniform distribution of workload and Utility function to detect Overstaffing
- Evaluate Agent Satisfaction over Agent satisfaction penalty for under-assignment using default function and shift stability function

Parameters:
- Number of nurses = 2xMaxShift requirements (0.3 nurses won't work on weekends)
- Nurses availability [1.0, 0.4] 

