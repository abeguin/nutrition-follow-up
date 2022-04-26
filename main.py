import numpy as np
import matplotlib.pyplot as pp
import pandas as pd
import seaborn

follow_up = pd.read_csv('data/follow_up.csv')

data_mean = follow_up.groupby('Week').mean()
x = data_mean.index
calories_in = data_mean['Calorie in'].astype(int)
calories_out = data_mean['Calorie out'].astype(int)
goal = calories_out.sub(500)

df = pd.DataFrame({
    'Week': data_mean.index,
    'Calorie in': calories_in,
    'Calorie out': calories_out,
    'Adjusted goal': goal,
    'Estimated goal': [1637]*len(x)
})

ax = df.plot(x='Week', y=['Calorie in', 'Calorie out'], kind='bar')
df.plot(x='Week', y=['Adjusted goal', 'Estimated goal'], kind='line', ax=ax)
#df.plot(x='Week', y='Estimated goal', kind='line', ax=ax)
#
# fig, ax = pp.subplots(figsize=(20, 10))
# x_ticks = np.arange(len(x))
# width = 0.35
# offset = 0.05
# bar_calories_in = ax.bar(x_ticks - offset - width / 2, calories_in, width + 2 * offset, label='Calories In')
# bar_calories_out = ax.bar(x_ticks + offset + width / 2, calories_out, width + 2 * offset, label='Calories Out')
# line_goal = ax.line(goal, label='Adjusted goal')
#
# ax.set_label('Calories')
# ax.set_title('Mean calories in & out')
# ax.set_xticks(x_ticks)
# ax.set_xticklabels(x)
#
#
# def compute_labels(rects):
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')
#
#
# compute_labels(bar_calories_in)
# compute_labels(bar_calories_out)
#
# pp.axhline(1637, color='red', ls='dotted', label='Estimated goal')
# pp.legend()

pp.savefig('follow_up.png', bbox_inches="tight", dpi=300)
pp.show()
