## For software testing
### Border cases:
- No shift requirements, no nurses available
- Open shift requirements, no nurses available
- No shift requirements, some nurses available

### Normal cases:
- Open shift requirements on weekends, no nurses available on weekends

## For lecture paper
**1. Impact of Beta**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S

Task:
- Evaluate Shift Coverage over Beta: [0.1,0.9]
- Evaluate Agent Satisfaction over Beta: [0.1,0.9] using default function and shift stability function

**2. Impact of Agent satisfaction sensibility on under-assignment**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- Beta = 0.8

Task:
- Evaluate Shift Coverage over Agent satisfaction penalty for under-assignment
- Evaluate Agent Satisfaction over Agent satisfaction penalty for under-assignment using default function and shift stability function

**3. Impact of Agent satisfaction sensibility on shift stability (different_shifts_in_week)**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- Beta = 0.8

Task:
- Evaluate Shift Coverage over Agent satisfaction penalty for shift stability
- Evaluate Agent Satisfaction over Agent satisfaction penalty for shift stability using shift stability function

**4. Utility function that maximizes uniform shift assignment distribition to agents**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- Beta = 0.8

Task:
- Evaluate Shift Coverage over ??
- Evaluate Agent Satisfaction over ??


**5. Utility function that reduces overstaffing of agents**

Situation: 
- 70% more agent availability on week days as weekends
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- Beta = 0.8
- Maximal number of nurses required in one shift = 7

Task:
- Evaluate Shift Coverage over Number of Nurses
- Evaluate Agent Satisfaction over Number of Nurses using default function and shift stability function

Expected results:
- Several nurses will have a very low degree of satisfaction (the over-staffed)

**6. Impact of Agent Availability(fragmentation) on Shift Coverage**

Situation: 
- Shift requirements higher on Friday 3rd Shift (3S), Saturday 1S and 3S, Sunday 3S
- Beta = 0.8

Task:
- Evaluate Shift Coverage over Agent Availability using Utility function for Uniform distribution of workload and Utility function to detect Overstaffing
- Evaluate Agent Satisfaction over Agent satisfaction penalty for under-assignment using default function and shift stability function

Parameters:
- Number of nurses = 2xMaxShift requirements (0.3 nurses won't work on weekends)
- Nurses availability [1.0, 0.4] 

