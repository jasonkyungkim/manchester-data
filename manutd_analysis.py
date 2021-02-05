#!/usr/bin/env python
# coding: utf-8

# # Manchester United Analysis
# by Jason Kim

# In[119]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('display.max_rows', None)
import plotly.offline as py
import plotly.graph_objects as go
import plotly.express as px
from IPython.display import HTML,display,display_html
import random


# In[103]:


def hide_toggle(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'Toggle show/hide'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current, 
        toggle_text=toggle_text
    )

    return HTML(html)

hide_toggle()


# In[139]:


df = pd.read_csv(r'C:\Users\Chongkyung\Documents\github\fifa_analysis\FIFA-21 Complete.csv',sep=';', index_col='player_id')

# in the FIFA21 player database, the team names had a space at the end: truncated.
df['team'] = df['team'].str.rstrip()

hide_toggle()


# ### Let's look at the raw FIFA stats first and see how Manchester United compares to other clubs in the world and especially their PL rivals.

# ## Intro: Basic comparisons between top European teams

# In[127]:


team_stat = df.groupby(['team'])['overall'].mean().sort_values(ascending=False)
team_stat.head(15).to_frame().style.background_gradient(cmap="magma")


# ### Manchester United ranks 15th in the world, by mean FIFA21 overall stats;
# ### Man City and Liverpool are the only PL clubs with higher mean overall stats
# 

# In[133]:


best_itw=df.loc[df['overall'] > 84 ].sort_values(by = ['overall'],ascending=False)
best_itw['team'].value_counts().head(15).to_frame().style.background_gradient(cmap="twilight")


# ### It is commonly accepted by FIFA fans that world class players have at least a 85 overall rating.  By this popular metric, Manchester United has only 3 world class players, less than Man City's 11, Liverpool's 10, and even Tottenham's 5.

# ## A Look inside Average League Positions for the past decade

# In[21]:


# Average Position Analysis
# Data pulled from Wikipedia
# (not many sites and data sources keep track of teams' mid-season league positions)
links = ["https://en.wikipedia.org/wiki/2009%E2%80%9310_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2010%E2%80%9311_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2011%E2%80%9312_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2012%E2%80%9313_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2013%E2%80%9314_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2014%E2%80%9315_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2015%E2%80%9316_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2016%E2%80%9317_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2017%E2%80%9318_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2018%E2%80%9319_Manchester_United_F.C._season","https://en.wikipedia.org/wiki/2019%E2%80%9320_Manchester_United_F.C._season"]
league_pos = []

def league_pos_extractor(link,league):
    manu_df = pd.read_html(link)
    if len(manu_df[4]) ==38:
        positions = manu_df[4].iloc[:,-1].values.tolist()
    elif link == "https://en.wikipedia.org/wiki/2018%E2%80%9319_Manchester_United_F.C._season":
        positions = manu_df[3].iloc[:,-2].values.tolist()
    else:
        positions = manu_df[3].iloc[:,-1].values.tolist()
    league.append(positions)

for link in links:
    league_pos_extractor(link,league_pos)
agg_lg_pos = pd.DataFrame(league_pos)

df2 = agg_lg_pos.T
df2.columns = ["09/10","10/11","11/12","12/13","13/14","14/15","15/16","16/17","17/18","18/19","19/20"]

for col in df2:
    if col == "15/16":
        df2[col] = df2[col].str[0]
    else:
        df2[col] = df2[col].str[:-2]
    df2[col] = pd.to_numeric(df2[col])

df2.index = range(1,39)

avg_pos = []

for col in df2:
    avg_pos.append((np.mean(df2[col])))

hide_toggle()


# In[44]:


pd.options.plotting.backend = "plotly"

fig = df2.plot(labels = dict(index="Gameweek",value="League Position",variable="season",line_shape="hv"))
fig['layout']['yaxis']['autorange'] = "reversed"

fig.show(include_plotlyjs=False,output_type='div')


# In[37]:


years = df2.columns

# fig2 = go.Figure(data=[go.Table(header=dict(values=['Season','Average Position', 'Final Position']),
#                  cells=dict(values=[df2.columns,avg_pos, [2,1,2,1,7,4,5,6,2,6,3]]))
#                      ])

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=years, y=avg_pos,
                    mode='lines+markers',
                    name='Avg Position'))
fig2.add_trace(go.Scatter(x=years, y= [2,1,2,1,7,4,5,6,2,6,3],
                    mode='lines+markers',
                    name='Result Position'))
fig2['layout']['yaxis']['autorange'] = "reversed"

fig2.show()


# ### We can see that since the 09/10 season, the team usually finishes at the position that it stays near for the entire season. The over-performance of 19/20 season, from an average to 6.2 to 3, can be attributed to Bruno Fernandes
# ##### (Bruno Fernandes, a Portuguese International, arrived at Manchester United on January 29th, 2020, basically in the middle of the 19/20 season. His influence was nothing short of amazing; Manchester United went undefeated for the remainder of the season (14 games), and to this day, Manchester United only lost 3 Premier League games.)

# ### As of today, 1/15/2021, Manchester United are 17 games in and has averaged about 10th place.
# ### It is not surprising nor offensive when rival fans doubt Manchester United's long-term success.
# ### If Manchester United wins ALL of the remaining 21 games
# #### 1. the team will have averaged about 5th place and
# #### 2. also win the league (as it stands, no team can overthrow United from 1st place)
# 
# ### At least for the past decade, no Manchester United side has had that big of a (mid-season) turnaround, bar the 19/20 season, so it remains questionable that Manchester United can mount as PL champions, although it seems like United may comfrotably title challengers and a top 4 side.

# ## A look inside FIFA ratings (compared to top flight PL teams)
# 
# 
# 
# #### In recent history, ever since Manchester United last won the PL, four different teams have been crowned champions: Liverpool, Chelsea, Man City, and Leicester City
# 
# #### How did we compare to these teams? Let's see.

# In[45]:


pl_champs = ['Liverpool','Chelsea','Manchester City','Leicester City', 'Manchester United']


# In[67]:


ratings = [[],[],[],[],[]]

df15 = pd.read_csv(r'C:\Users\Chongkyung\Documents\GitHub\fifa_analysis\fifa21\fifa15_20\players_15.csv')
df16 = pd.read_csv(r'C:\Users\Chongkyung\Documents\GitHub\fifa_analysis\fifa21\fifa15_20\players_16.csv')
df17 = pd.read_csv(r'C:\Users\Chongkyung\Documents\GitHub\fifa_analysis\fifa21\fifa15_20\players_17.csv')
df18 = pd.read_csv(r'C:\Users\Chongkyung\Documents\GitHub\fifa_analysis\fifa21\fifa15_20\players_18.csv')
df19 = pd.read_csv(r'C:\Users\Chongkyung\Documents\GitHub\fifa_analysis\fifa21\fifa15_20\players_19.csv')
df20 = pd.read_csv(r'C:\Users\Chongkyung\Documents\GitHub\fifa_analysis\fifa21\fifa15_20\players_20.csv')

def champ_mean(plchamps,df,lists):
    for champ,i in zip(plchamps,range(5)):
        lists[i].append(df.loc[df['club'] == champ ]['overall'].mean())

dfs = [df15,df16,df17,df18,df19,df20]

for df in dfs:
    champ_mean(pl_champs,df,ratings)
    
hide_toggle()


# In[66]:


fig3 = go.Figure()

x = years[5:]

for i in range(5):
    fig3.add_trace(go.Scatter(x=x, y=ratings[i], name=pl_champs[i],
                    line_shape='linear'))
fig3.update_traces(hoverinfo='text+name', mode='lines+markers')
fig3.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))


# ### In the 16/17 season, Manchester United had by far the highest rated team in the PL and yet they finished 6th in the league. Let's look at how the squad actually compared to the top 3 teams that season.

# In[145]:


def display_side_by_side(*args):
    html_str=''
    for df in args:
        html_str+=df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)
    
hide_toggle()


# In[143]:


mu_16_17=df17.loc[df17['club']=="Manchester United"].sort_values(by = ['overall'],ascending=False)
mu_16_17 = mu_16_17[['short_name','overall']].style.background_gradient(cmap="Reds").set_table_attributes("style='display:inline'").set_caption('16/17 Man Utd (6th) ')


mc_16_17=df17.loc[df17['club']=="Manchester City"].sort_values(by = ['overall'],ascending=False)
mc_16_17 = mc_16_17[['short_name','overall']].style.background_gradient(cmap="cool").set_table_attributes("style='display:inline'").set_caption('Man City (3rd)')

cfc_16_17=df17.loc[df17['club']=="Chelsea"].sort_values(by = ['overall'],ascending=False)
cfc_16_17 = cfc_16_17[['short_name','overall']].style.background_gradient(cmap="Blues").set_table_attributes("style='display:inline'").set_caption('Chelsea (1st)')

spurs_16_17=df17.loc[df17['club']=="Tottenham Hotspur"].sort_values(by = ['overall'],ascending=False)
spurs_16_17 = spurs_16_17[['short_name','overall']].style.background_gradient(cmap="gray").set_table_attributes("style='display:inline'").set_caption('Spurs (2nd)')

hide_toggle()


# In[144]:


display_html(mu_16_17._repr_html_()+cfc_16_17._repr_html_()+spurs_16_17._repr_html_()+mc_16_17._repr_html_(),raw=True)


# In[ ]:




