# -*- coding: utf-8 -*-
"""JDA_test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mnl2Ay7JHwesMQuzqxD_pxDQbZ0VFPOh

# Часть 1. Работа с данными
"""

import pandas as pd

# Необходимо указать полный путь до csv-файла
df = pd.read_csv ("/content/Тестовое задание - tz_data.csv")
df

"""## Подготовка датасета"""

import numpy as np
df['area'].replace('', np.nan, inplace=True)
df.dropna(subset=['area'], inplace=True)

def conv_Ycoordinate(x):
  try:
    return float(x)
  except ValueError:
    return 0

def conv_countValue(x):
  try:
    return int(x)
  except ValueError:
    return 0

df.drop(['good (1)'], axis=1, inplace=True)
df.y = df.y.apply(conv_Ycoordinate)
df['count'] = df['count'].apply(conv_countValue)
# df['count'] = df['count'].apply(lambda x: int(x))

df.cluster = df.cluster.apply(lambda x: int(x))
df.cluster_name = df.cluster_name.apply(lambda x: str(x))

import random
# col = ['1', '2', '3', '4']
col = ['blue','orange','green','red',]

"""## Работа с датасетом"""

# Removing duplicates & adding "color" column
res = pd.DataFrame(columns=['area', 'cluster', 'cluster_name', 'keyword', 'count', 'x', 'y', 'color'])
count = 0

for area in df.area.unique():
  # print(area)

  cur = df.loc[df['area'] == area].drop_duplicates(subset=['keyword'], keep='last').reset_index(drop=True)
  # cur.drop(['index'], axis=1, inplace=True)
  cur['color'] = cur.cluster.apply(lambda x: col[int(x)])
  # print(cur.size)
  count+=len(cur)
  prev = cur

  # Вы можете раскомментировать следующую строку, чтобы цвета изменялись случайным образом
  # random.shuffle(col)

  res = pd.merge(res, cur, how='outer')
  # print(count)
res

# Sorting
res.sort_values(['area','cluster','cluster_name','count'], ascending=[True, True, True, False], inplace=True)
res.reset_index(inplace=True, drop=True)
res

"""# Часть 2. Построение графиков

Внимание, для корректной работы дальнейшего кода необходим модуль python-intervals! Вы можете его установить, введя в консоль: 

```
pip install python-intervals
```
"""

!pip install python-intervals
import intervals as I

from pandas.core.groupby.groupby import FrameOrSeries
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd 



SYMBOLS_FOR_CARRY = 15
ONE_LINE_SIZE = 0.4
INTERVAL_STEP = 0.1 # 0.35
BIAS = 0.1
TEXT_SIZE = 10
POINT_SIZE = 70

def plot_graph(name, t_x=1, t_y=-0.045, k1=-0.5, k2=-0.3, k3=-2.5, k4=1, k5=1, n=0):
  a4_dims = (11.7, 8.27)
  fig, ax = plt.subplots(figsize=a4_dims)
  plt.title('Диаграмма рассеяния для ' +  str(name), x= t_x , y= t_y) 
            # fontfamily = 'fantasy',
            # fontstyle  = 'oblique',
            # fontsize   = 10)


  # ax.spines["right"].set_visible(False)
  # ax.spines["top"].set_visible(False)
  # ax.spines["bottom"].set_visible(False)
  # ax.spines["left"].set_visible(False)

  ax.axis("off")

  # Scatterplot display
  sns.scatterplot(data = cur_df, x = "x", y = "y", hue="color", style="cluster_name", s = POINT_SIZE)
  ax.legend(loc="upper left", bbox_to_anchor=(1.25,0.31))


  # Text overlay processing
  bizy = I.empty()

  for line in range(0,cur_df.shape[0]-n):
    
    # Conditions for the current line
    text = cur_df.keyword[line]
    y_position = cur_df.y[line]
    carry_flag = False

    if len(text) > SYMBOLS_FOR_CARRY:
      if text[SYMBOLS_FOR_CARRY-1:].find(' ')>0:
        pos = text[SYMBOLS_FOR_CARRY-1:].find(' ')
        # print(pos)
        # print(text[:14+pos]+'\n'+text[15+pos:])
        text = text[:SYMBOLS_FOR_CARRY-1+pos]+'\n'+text[SYMBOLS_FOR_CARRY+pos:]
        y_position = y_position-ONE_LINE_SIZE
        carry_flag = True
        
    # print(line)
    # print(len(cur_df.keyword[line]))
    if cur_df.y[line] in bizy:
      plt.text(cur_df.x[line]+BIAS, y_position+k1*ONE_LINE_SIZE, text, horizontalalignment='left', size=TEXT_SIZE, color='black', weight='semibold')
      pass
    else:
      plt.text(cur_df.x[line]+BIAS, y_position+k2, text, horizontalalignment='left', size=TEXT_SIZE, color='black', weight='semibold')

    if carry_flag:
      bizy = bizy | I.open(cur_df.y[line]+k3*INTERVAL_STEP, cur_df.y[line]+k5*INTERVAL_STEP)
    else:
      bizy = bizy | I.open(cur_df.y[line]-k4*INTERVAL_STEP, cur_df.y[line]+k4*INTERVAL_STEP)


  if n == 0:
    plt.show()

"""## ar\vr"""

cur_df = res.loc[res['area'] == 'ar\\vr']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('ar\\vr', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## available"""

cur_df = res.loc[res['area'] == 'available']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('available', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## capability"""

cur_df = res.loc[res['area'] == 'capability']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('capability', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## dialog"""

cur_df = res.loc[res['area'] == 'dialog']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('dialog', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## eligibility"""

cur_df = res.loc[res['area'] == 'eligibility']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('eligibility', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## except"""

cur_df = res.loc[res['area'] == 'except']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('except', t_x=1, t_y=-0.045, k1=1, k2=+0, k3=-5.5, k5=5.5)

"""## greetings"""

cur_df = res.loc[res['area'] == 'greetings']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('greetings', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5, n=1)

# В данном случае расположение одной записи исправляем вручную
text = cur_df.keyword[14]
y_position = cur_df.y[14]
carry_flag = False

if len(text) > SYMBOLS_FOR_CARRY:
  if text[SYMBOLS_FOR_CARRY-1:].find(' ')>0:
    pos = text[SYMBOLS_FOR_CARRY-1:].find(' ')
    # print(pos)
    # print(text[:14+pos]+'\n'+text[15+pos:])
    text = text[:SYMBOLS_FOR_CARRY-1+pos]+'\n'+text[SYMBOLS_FOR_CARRY+pos:]
    y_position = y_position-ONE_LINE_SIZE
    carry_flag = True
    
plt.text(cur_df.x[14]+BIAS, y_position+ONE_LINE_SIZE, text, horizontalalignment='left', size=TEXT_SIZE, color='black', weight='semibold')
plt.show()

"""## housewives"""

cur_df = res.loc[res['area'] == 'housewives']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('housewives', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## lithuania"""

cur_df = res.loc[res['area'] == 'lithuania']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('lithuania', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5, k4=4)

"""## locator"""

cur_df = res.loc[res['area'] == 'locator']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('locator', t_x=1, t_y=-0.045, k1=1, k2=+0, k3=-2.5)

"""## personnel"""

cur_df = res.loc[res['area'] == 'personnel']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('personnel', t_x=1, t_y=-0.035, k1=-1, k2=+0, k3=-2.5)

"""## protein"""

cur_df = res.loc[res['area'] == 'protein']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('protein', t_x=1, t_y=-0.05, k1=-0.5, k2=+0, k3=-6.5)

"""## twisted"""

cur_df = res.loc[res['area'] == 'twisted']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('twisted', t_x=1, t_y=-0.045, k1=-1, k2=+0, k3=-2.5)

"""## winner"""

cur_df = res.loc[res['area'] == 'winner']
cur_df.reset_index(inplace=True, drop=True)
# cur_df

plot_graph('winner', t_x=1, t_y=-0.045, k1=-1, k2=+0.2, k3=-2.5)

"""## worlds"""

cur_df = res.loc[res['area'] == 'worlds']
cur_df.reset_index(inplace=True, drop=True)
cur_df

plot_graph('worlds', t_x=1, t_y=-0.045, k1=0.7, k2=-0.3, k3=-2.5, k4=3)

"""## End"""





