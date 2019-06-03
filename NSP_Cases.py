#!/usr/bin/env python
# coding: utf-8

# ### Agent-Based Modelling - FS19
# # ABM Final - Gabriela Lopez & Luca Weibel
# 
# 

# Here are the libraries / configurations used.

# In[1]:


#get_ipython().run_line_magic('config', 'IPCompleter.greedy=True')

import importlib
import abm_scheduling as sch

#from prettytable import PrettyTable


# In[2]:


importlib.reload(sch)


# In[3]:


# --example schedules--
schedule_fixed = sch.Schedule(num_nurses_needed=3)
schedule_fixed.print_schedule()


# In[4]:


schedule_random = sch.Schedule(num_nurses_needed=3, is_random=True)
schedule_random.print_schedule()


# In[ ]:


# --example nurses--
# full time, no weekends
nurse = Nurse(id_name=0)
nurse.generate_shift_preferences(degree_of_agent_availability=1, works_weekends=False)
nurse.print_shift_preferences()

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


# In[ ]:





# In[ ]:





# # ---- FOR REFERENCE ---- 

# # S07 Exercises - Luca Weibel
# 
# 

# ### Exercise 7.1: Forest fire model

# #### Task
# Here we compute the production (average number of trees before after each summer, i.e. after each
# fire phase) as a function of $g$ considering both Moore (8-neighborhood) and Von Neumann (4-neighborhood).
# 
# The system parameters are system size $L=20,40$ (where forest is of size $L$x$L$), $f=0.001$, and total time steps $t_{max}=1000$.

# In[ ]:


L_s = [20, 40]
f = 0.001
t_max = 1000
growth_rates = [g for g in range(0, 101, 10)]
methods = ['Von Neumann', 'Moore']
reps = 5

for method in methods:
    for L in L_s:
        # Von Neumann - generates 4-neighborhood
        net = nx.grid_2d_graph(L, L, periodic=False)
        net = nx.convert_node_labels_to_integers(net)
        if method == 'Moore':
            # add aditional edges
            for node in net.nodes():
                x = node % L
                y = node // L
                # top right
                if x + 1 < L and y - 1 >= 0:
                    net.add_edge(node, node - L + 1)
                # bottom right
                if x + 1 < L and y + 1 < L:
                    net.add_edge(node, node + L + 1)
                # bottom left
                if x - 1 >= 0 and y + 1 < L:
                    net.add_edge(node, node + L - 1)
                # top left
                if x - 1 >= 0 and y - 1 >= 0:
                    net.add_edge(node, node - L - 1)
        avg_num_trees_before_each_summer = []
        for g in growth_rates:
            all_reps = []
            for rep in range(reps):
                forest = [0] * (L * L)
                num_trees_before_each_summer = []
                for t in range(t_max):
                    num_trees_before_each_summer.append(forest.count(1))
                    for i in range(len(forest)):
                        # growth phase
                        if forest[i] == 0:
                            forest[i] = int(rnd.uniform() < (g * 0.01))
                        # fire phase - init
                        if forest[i] == 1:
                            forest[i] = int(rnd.uniform() < f) + 1
                    # fire phase - burn
                    burning_trees = [idx for idx, tree in enumerate(forest) if tree == 2]
                    for burning_tree in burning_trees:
                        burning_tree_neighbors = [_ for _ in net.neighbors(burning_tree)]
                        for neighbor in burning_tree_neighbors:
                            if forest[neighbor] == 1:
                                forest[neighbor] = 2
                                if neighbor not in burning_trees:
                                    burning_trees.append(neighbor)               
                    for burnt_tree in burning_trees:
                        forest[burnt_tree] = 0
                all_reps.append(np.mean(num_trees_before_each_summer))
            avg_num_trees_before_each_summer.append(np.mean(all_reps))

        plt.figure()
        plt.plot(growth_rates, avg_num_trees_before_each_summer, label = "Production")
        plt.title(f'Production as a function of g with {method} neighborhood, L={L}, f={f}, t_max={t_max}, and repetitions={reps}')
        plt.xlabel("Growth Rate (%)")
        plt.ylabel("Production (trees)")
        plt.legend()
        plt.show()


# ### Exercise 7.2: Sand Pile Model

# #### Task
# Here we plot the theoretical and experimental (10,000 trials) avalanche (number of topples caused) distribution with $T=2$ and $k=1$ for different network size $N$. Then we plot the experimental (10,000 trials) avalanche (number of topples caused) distribution with $T=6$ and $k=1$ for different network size $N$. We remove the 0 avalanches count in order to more easily analyze the distributions.
# 
# The system parameters are number of agents $N=10,20,50,100$.

# In[ ]:


N_s = [10, 20, 50, 100]
T = 2
k = 1
Ai = 1

for N in N_s:
    agents = [Ai] * N
    topples_caused = []
    theoretical_topples_caused = []
    for trails in range(10000):
        # add a grain to one agent randomly selected
        rnd_i = rnd.randint(N)
        # calculate theoretical topples
        d = min(rnd_i, N - rnd_i)
        M = 0
        if agents[rnd_i] >= T - 1:
            for i in range(rnd_i, N):
                if agents[i] >= T - 1:
                    M += 1
                else:
                    break
            for i in range(rnd_i - 1, -1, -1):
                if agents[i] >= T - 1:
                    M += 1
                else:
                    break
        theoretical_topples_caused.append(max(0, d * (M - d + 1)))
        # add grain
        agents[rnd_i] += 1
        # check and possibly initiate topples
        overflowed = [idx for idx, a in enumerate(agents) if a >= T]
        # calculate experimental topples
        topples = 0
        while(len(overflowed) > 0):
            for o_i in overflowed:
                topples += 1
                agents[o_i] -= 2 * k
                for k_i in range(1, k+1):
                    if (o_i + k_i) < N:
                        agents[o_i + k_i] += 1
                    if (o_i - k_i) >= 0:
                        agents[o_i - k_i] += 1
            overflowed = [idx for idx, a in enumerate(agents) if a >= T]
        topples_caused.append(topples)
            
    data = collections.Counter(topples_caused)
    data[0] = 0
    plt.figure()
    plt.bar([key for key in data], [data[key] for key in data])
    plt.title(f'Experimental distribution of avalanches (10000 trials) with N={N} T={T} k={k}')
    plt.xlabel("Number of topples caused")
    plt.show()
    t_data = collections.Counter(theoretical_topples_caused)
    t_data[0] = 0
    plt.figure()
    plt.bar([key for key in t_data], [t_data[key] for key in t_data], color='red')
    plt.title(f'Theoretical distribution of avalanches (10000 trials) with N={N} T={T} k={k}')
    plt.xlabel("Number of topples caused")
    plt.show()


# In[ ]:


N_s = [10, 20, 50, 100]
T = 6
k = 1
Ai = 0

for N in N_s:
    agents = [Ai] * N
    topples_caused = []
    for trails in range(10000):
        # add a grain to one agent randomly selected
        rnd_i = rnd.randint(N)
        agents[rnd_i] += 1
        # check and possibly initiate topples
        overflowed = [idx for idx, a in enumerate(agents) if a >= T]
        topples = 0
        while(len(overflowed) > 0):
            for o_i in overflowed:
                topples += 1
                agents[o_i] -= 2 * k
                for k_i in range(1, k+1):
                    if (o_i + k_i) < N:
                        agents[o_i + k_i] += 1
                    if (o_i - k_i) >= 0:
                        agents[o_i - k_i] += 1
            overflowed = [idx for idx, a in enumerate(agents) if a >= T]
        topples_caused.append(topples)
            
    data = collections.Counter(topples_caused)
    data[0] = 0
    plt.figure()
    plt.bar([key for key in data], [data[key] for key in data])
    plt.title(f'Experimental distribution of avalanches (10000 trials) with N={N} T={T} k={k}')
    plt.xlabel("Number of topples caused")
    plt.show()

