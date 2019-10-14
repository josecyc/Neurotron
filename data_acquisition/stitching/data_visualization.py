#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
pd.set_option('display.max_columns', 500)


# In[2]:


df = pd.read_csv("datasets/data_90644_1561101188.22012.csv")


# In[3]:


df.head()


# In[4]:


emg_df = df.loc[:, 'ch1':'ch8']
leap_df = df.loc[:, 'Wrist x':]


# In[5]:


leap_df.head()


# In[6]:


pred_df = pd.read_csv("predictions/pred_001.csv")


# In[7]:


pred_df


# In[8]:


samples = 10000
start = np.random.randint(0, len(leap_df) - samples)
#start = 0


# In[9]:


plot_df = leap_df.loc[start:start + samples, 'Wrist x':'Pinky Tip z']
#pred_plot_df = pred_df.loc[start:start + samples, 'Wrist x':'Pinky Tip z']
pred_plot_df = pred_df[start:start + samples]


# In[10]:


plot_df.head()


# In[11]:


pred_plot_df.describe()


# In[12]:


def mod_dataframe(df):
    wrist = df.loc[:, :'Wrist z']
    bones = df.loc[:, 'Thumb Proximal x':]
    names = ['thumb x', 'thumb y', 'thumb z',
             'index x', 'index y', 'index z',
             'middle x', 'middle y', 'middle z',
             'ring x', 'ring y', 'ring z',
             'pinky x', 'pinky y', 'pinky z']
    j = 0
    first = True
    for i in range(0, 60, 12):
        wrist.columns = names[j:j+3]
        proximal = bones.loc[:, bones.columns[i]:bones.columns[i+2]]
        intermediate = bones.loc[:, bones.columns[i+3]:bones.columns[i+5]]
        distal = bones.loc[:, bones.columns[i+6]:bones.columns[i+8]]
        tip = bones.loc[:, bones.columns[i+9]:bones.columns[i+11]]
        proximal.columns = names[j:j+3]
        intermediate.columns = names[j:j+3]
        distal.columns = names[j:j+3]
        tip.columns = names[j:j+3]
        unit = pd.concat([wrist, proximal, intermediate, distal, tip], axis=0)
        j += 3
        if (first):
            res = unit
            first = False
        else:
            res = pd.concat([res, unit], axis=1)
    return (res)


# In[13]:


mod_df = mod_dataframe(plot_df[:1])
pred_mod_df = mod_dataframe(pred_plot_df[:1])


# In[14]:


mod_df


# In[15]:


pred_mod_df


# In[16]:


(mod_df - pred_mod_df).describe()


# In[17]:


def update(num):
    mod_df = mod_dataframe(plot_df[num:num+1])
    pred_mod_df = mod_dataframe(pred_plot_df[num:num+1])
    columns = mod_df.columns
    j = 0

    for i in range(0, 15, 3):
        a = mod_df[columns[i]].values
        b = mod_df[columns[i+1]].values
        c = mod_df[columns[i+2]].values
        pred_a = pred_mod_df[columns[i]].values
        pred_b = pred_mod_df[columns[i+1]].values
        pred_c = pred_mod_df[columns[i+2]].values
        #preds and labels:
#         line[j].set_data(a, b)
#         line[j].set_3d_properties(c)
        pred_line[j].set_data(pred_a, pred_b)
        pred_line[j].set_3d_properties(pred_c)
        title.set_text('3D Hand Model, iteration = {}'.format(num))
        j += 1
    
#     wrist.set_data(a[0], b[0])
#     wrist.set_3d_properties(c[0])
    pred_wrist.set_data(pred_a[0], pred_b[0])
    pred_wrist.set_3d_properties(pred_c[0])
    #preds and labels
    return (line[0], line[1], line[2], line[3], line[4], wrist, title,
            pred_line[0], pred_line[1], pred_line[2], pred_line[3], pred_line[4], pred_wrist, title)
    # preds only uncomment this:
    #return (pred_line[0], pred_line[1], pred_line[2], pred_line[3], pred_line[4], pred_wrist, title)


# In[18]:


#get_ipython().run_line_magic('matplotlib', 'notebook')

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
colors = ['g', 'r', 'c', 'm', 'k']
title = ax.set_title('3D Hand Model')


mod_df = mod_dataframe(plot_df[:1])
pred_mod_df = mod_dataframe(pred_plot_df[:1])
columns = mod_df.columns
j = 0
line = []
pred_line = []
for i in range(0, 15, 3):
    a = mod_df[columns[i]].values
    b = mod_df[columns[i+1]].values
    c = mod_df[columns[i+2]].values
    pred_a = pred_mod_df[columns[i]].values
    pred_b = pred_mod_df[columns[i+1]].values
    pred_c = pred_mod_df[columns[i+2]].values
    #add labels
#     l, = ax.plot(a, b, c, 'ro-', color=colors[j], marker="o", ms=15, lw=3)
    pred_l, = ax.plot(pred_a, pred_b, pred_c, 'ro-', color=colors[j], alpha=0.2, marker="o", ms=15, lw=3)
    #add labels
#     line.append(l)
    pred_line.append(pred_l)
    j += 1

# wrist, = ax.plot(a, b, c, 'ro-', color='y', marker="o", ms=15, lw=3)
pred_wrist, = ax.plot(pred_a, pred_b, pred_c, 'ro-', color='y', alpha=0.2, marker="o", ms=15, lw=3)
ani = FuncAnimation(fig, update, samples, interval=1, blit=True)
#ax.legend(['Thumb', 'Index', 'Middle', 'Ring', 'Pinky', 'Wrist'])
plt.show()


# In[19]:


# %matplotlib notebook
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
# colors = ['g', 'r', 'c', 'm', 'k']
# # alphas = [1, 0.7, 0.5, 0.3]

# for i in range(samples):
#     mod_df = mod_dataframe(plot_df[i:i+1])
#     columns = mod_df.columns
#     j = 0
#     for i in range(0, 15, 3):
#         a = mod_df[columns[i]].values
#         b = mod_df[columns[i+1]].values
#         c = mod_df[columns[i+2]].values
#         ax.scatter(a, b, c, color=colors[j], s=100)
#         ax.plot(a, b, c, color=colors[j])
#         j += 1

# #animation = FuncAnimation(fig, update, interval=200)
# plt.show()


# In[20]:


# def iterate_dataframe(plot_df):
#     for col in plot_df:
#         yield plot_df[col].values


# In[21]:


# %matplotlib notebook
# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
# generator = iterate_dataframe(plot_df)
# ax.scatter(next(generator), next(generator), next(generator), color='b')
# colors = ['g', 'r', 'c', 'm', 'k']
# alphas = [1, 0.7, 0.5, 0.3]
# k = 0
# j = -1
# for i in range(20):
#     if (i % 4 == 0):
#         k = 0
#         j += 1
#     a = next(generator)
#     b = next(generator)
#     c = next(generator)
#     ax.scatter(a, b, c, color=colors[j], alpha=alphas[k])
#     ax.plot(a, b, c, color=colors[j])
#     plt.pause(0.05)
#     k += 1

# ax.legend(['Wrist ', 'Thumb Proximal', 'Thumb Intermediate', 'Thumb Distal', 'Thumb Tip',
#            'Index Proximal', 'Index Intermediate', 'Index Distal', 'Index Tip',
#            'Middle Proximal', 'Middle Intermediate', 'Middle Distal', 'Middle Tip',
#            'Ring Proximal', 'Ring Intermediate', 'Ring Distal', 'Ring Tip',
#            'Pinky Proximal', 'Pinky Intermediate', 'Pinky Distal', 'Pinky Tip'])
# plt.show()


# In[ ]:




