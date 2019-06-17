## For lecture paper
**Case. Nurse availability levels - number of nurses**

Situation: 
- Shift requirements normal distribution around 5 nurses/shift
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage, Agent Satisfaction and Productivity over Nurse availability starting from 0 nurses until coverage reaches a stable 1.0 using both default and agent_satisfaction utility functions

**Case. Nurse availability levels - degree of availability**

Situation: 
- Shift requirements normal distribution around 5 nurses/shift
- p_to_accept_negative_change=.001

Task:
- Evaluate Shift Coverage over degree of availability for 25 nurses starting from availability of 20% up to 100% using both default and agent_satisfaction utility functions

**Case. Impact of p_negative**

Situation: 
- 70% agent availability on weekdays and weekends

Task:
- Evaluate Shift Coverage over p_negative: [.001, .0025, .005, .0075, .01, .02, .03, .05, .1, .2]
- Evaluate Agent Satisfaction over p_negative: [.001, .0025, .005, .0075, .01, .02, .03, .05, .1, .2]

**Case. Impact of Agent Availability homogeneity **

Situation: 
- Shift requirements fix to 5 nurses/shift

Parameters
- p_to_accept_negative_change=.001
- Type of availability:
    - type 1: only first shift 
    - type 2 only third shift 
    - type 3 1st and 2nd shifts 
    - type 4 2nd and 3rd shifts
    - type 5 work only weekends all shifts possible

Task:
- Evaluate emerging parameters over number of nurses by generating a nurse with a random type of availability in each step, both utility functions
