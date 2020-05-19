import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
df = pd.read_csv(r'C:\Users\Kshitij\Desktop\owid-covid-data-17may.csv',usecols=['location','date','total_cases'])
df1=df.loc[df['location'].isin(['India','China','Iran','France','Turkey','Germany','Brazil','Italy','United Kingdom','Russia','United States'])]
grouped = df1.groupby(['location','date'])
df1_confirmed = grouped.sum().reset_index().sort_values(['date'],ascending=True)
df11_confirmed=df1_confirmed.head(12)
print(df1_confirmed)

#Initial Bar Chart Of Max cases stored in df11_confirmed
fig, ax = plt.subplots(figsize=(15, 8))
ax.barh(df1_confirmed['location'], df1_confirmed['total_cases'])
plt.xlabel('Number of Confirmed Cases')
plt.ylabel('location')
dff=df11_confirmed[::-1]
fig, ax = plt.subplots(figsize=(15, 8))
ax.barh(dff['location'], dff['total_cases'])
plt.xlabel('Number of Confirmed Cases')
plt.ylabel('location')

#Code for individual colors for each country using dictionary
from random import randint
import random
c_code = []
random.seed(1000)
for i in range(len(df1_confirmed.location.unique())):
    c_code.append('#%06X' % randint(0, 0xFFFFFF))

colors = dict(zip(df1_confirmed.location.unique(), c_code))

#First step
fig, ax = plt.subplots(figsize=(15, 8))

#Pass colors values to `color=`
ax.barh(dff['location'], dff['total_cases'], color=[colors[x] for x in dff['location']])

#Iterating over the values to plot labels and values
for i, (value, name) in enumerate(zip(dff['total_cases'], dff['location'])):
    ax.text(value,i      ,name,ha='right')
    ax.text(value,i-0.25 ,value,ha='right')

#Add year right middle portion of canvas
ax.text(1, 0.4, "17/05/2020", transform=ax.transAxes, size=25, ha='right')

#Main Function Code
fig, ax = plt.subplots(figsize=(15, 8))
def draw_racechart(date,case="total_cases"):
    dff= (df1_confirmed[df1_confirmed['date'].eq(date)].sort_values(by=case,ascending=False).head(10))[::-1]
    ax.clear()
    ax.barh(dff['location'], dff[case], color=["#fa4848","#f29538","#f5d64c","#CB6262","#D39B5F","#4ab6f0","#9CF710","#e3a1ff","#D0F710","#f7b77c"][::-1])
    dx = dff[case].max() / 200
    for i, (value, name) in enumerate(zip(dff[case], dff['location'])):
        ax.text(value-dx, i,     name,           size=14, weight=600, ha='right', va='bottom')
        ax.text(value-dx, i-.25, value, size=10, color='#17202A', ha='right', va='baseline')

    #Adding more styles
    ax.text(1, 0.4, date, transform=ax.transAxes, color='#777777', size=30, ha='right', weight=800)
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#bf1d25', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='--')
    ax.set_axisbelow(True)
    ax.text(0, 1.08, 'Top 10 Countries with maximum confirmed COVID-19 cases from 31/Dec/2019 to 17/May/2020',
            transform=ax.transAxes, size=18, weight=300, ha='left')
    ax.text(1, 0, 'By Kshitij Jain', transform=ax.transAxes,
            size=10,weight=70, ha='right',color='#030101',
            bbox=dict(facecolor='white', alpha=1.0, edgecolor='red'))
    plt.box(False)

draw_racechart("2020-05-17")

#Animation
from matplotlib import animation as Anim
from IPython.display import HTML
fig,ax = plt.subplots(figsize=(16,10)) #Set figure for plot
animator = Anim.FuncAnimation(fig,draw_racechart,frames=df1_confirmed.date.unique(),interval=2000) #Building animation
HTML(animator.to_jshtml())
plt.show()