import matplotlib.pyplot as pp
import pandas as pd


def round_to_5(x):
    return 5 * round(x / 5)


PARAM_WEIGHT = 66

# Estimated body fat percentage
PARAM_BODY_FAT = 0.17

# x1.1 : peu ou pas d’exercice/sport (E/S)
# x1.2 : E/S 1-2 fois par semaine
# x1.35 : E/S 3-5 fois par semaine
# x1.45 : E/S 6-7 fois par semaine
# x1.6-1.8 : E/S 6-7 fois par semaine & travail physique
PARAM_ACTIVITY_FACTOR = 1.35

# Deficit percentage
# Recommended between 10 and 25%
# The higher it is, the higher should the protein factor be
PARAM_DEFICIT = 0.2

# Between 1.5 and 2.3
# the leaner you are and the higher the deficit is
# the higher this factor should be
PARAM_PROTEIN_FACTOR = 2.3

# At least 0.7, to stay healthy
PARAM_LIPID_FACTOR = 1.5
PARAM_MIN_LIPID_FACTOR = 0.7

CAL_PER_PROTEIN_GRAM = 4
CAL_PER_LIPID_GRAM = 9
CAL_PER_CARBOHYDRATE_GRAM = 4

DAILY_MAINTENANCE = round_to_5((370 + 21.6 * (1 - PARAM_BODY_FAT) * PARAM_WEIGHT) * PARAM_ACTIVITY_FACTOR)
DAILY_GOAL = round_to_5((1 - PARAM_DEFICIT) * DAILY_MAINTENANCE)
DAILY_DEFICIT = round_to_5(DAILY_MAINTENANCE - DAILY_GOAL)
DAILY_PROTEIN = round_to_5(PARAM_PROTEIN_FACTOR * (1 - PARAM_BODY_FAT) * PARAM_WEIGHT)
DAILY_LIPID = round_to_5(PARAM_LIPID_FACTOR * (1 - PARAM_BODY_FAT) * PARAM_WEIGHT)
DAILY_MIN_LIPID = round_to_5(PARAM_MIN_LIPID_FACTOR * (1 - PARAM_BODY_FAT) * PARAM_WEIGHT)
DAILY_CARBOHYDRATE = round_to_5(
    (DAILY_GOAL - (DAILY_LIPID * CAL_PER_LIPID_GRAM) - (DAILY_PROTEIN * CAL_PER_PROTEIN_GRAM)) /
    CAL_PER_CARBOHYDRATE_GRAM
)

follow_up = pd.read_csv('data/follow_up.csv')

# Calorie mean
data_mean = follow_up.groupby('Week').mean()
calories_in = data_mean['Calorie in'].astype(int)
calories_out = data_mean['Calorie out'].astype(int)
adjusted_goal = calories_out.sub(DAILY_DEFICIT)

df_cal_mean = pd.DataFrame({
    'Week': data_mean.index,
    'Calorie in': calories_in,
    'Calorie out': calories_out,
    'Adjusted goal': adjusted_goal,
    'Estimated goal': [DAILY_GOAL] * len(data_mean.index)
})

ax = df_cal_mean.plot(x='Week', y=['Calorie in', 'Calorie out'], kind='bar', color=['grey', 'royalblue'],
                      figsize=[20, 10])
df_cal_mean.plot(x='Week', y=['Adjusted goal', 'Estimated goal'], kind='line', ax=ax, color=['red', 'gold'])
pp.title('Calorie mean')
pp.savefig('../viz/assets/cal-mean.png', bbox_inches="tight", dpi=100)
pp.show()

# Calorie sum
# A_WEEK = 7
# WEEKLY_MAINTENANCE = DAILY_MAINTENANCE * A_WEEK
# WEEKLY_GOAL = DAILY_GOAL * A_WEEK
# WEEKLY_DEFICIT = DAILY_DEFICIT * A_WEEK
# WEEKLY_PROTEIN = DAILY_PROTEIN * A_WEEK
# WEEKLY_LIPID = DAILY_LIPID * A_WEEK
# WEEKLY_CARBOHYDRATE = DAILY_CARBOHYDRATE * A_WEEK
#
# data_sum = follow_up.groupby('Week').sum()
# calories_in = data_sum['Calorie in'].astype(int)
# calories_out = data_sum['Calorie out'].astype(int)
# adjusted_goal = calories_out.sub(WEEKLY_DEFICIT)
#
# df_cal_sum = pd.DataFrame({
#     'Week': data_sum.index,
#     'Calorie in': calories_in,
#     'Calorie out': calories_out,
#     'Adjusted goal': adjusted_goal,
#     'Estimated goal': [WEEKLY_GOAL] * len(data_sum.index)
# })
#
# ax = df_cal_sum.plot(x='Week', y=['Calorie in', 'Calorie out'], kind='bar', color=['grey', 'royalblue'],
#                      figsize=[20, 10])
# df_cal_sum.plot(x='Week', y=['Adjusted goal', 'Estimated goal'], kind='line', ax=ax, color=['red', 'gold'])
# pp.title('Calorie sum')
# pp.savefig('../viz/assets/cal-sum.png', bbox_inches="tight", dpi=100)
# pp.show()

# Weight
data_weight = follow_up.groupby('Week').mean()
weight = data_weight['Weight']

df_weight = pd.DataFrame({
    'Week': data_weight.index,
    'Weight': weight,
})

df_weight.plot(x='Week', y=['Weight'], kind='line', color=['royalblue'], figsize=[20, 10])
pp.title('Weight')
pp.savefig('../viz/assets/weight.png', bbox_inches="tight", dpi=100)
pp.show()

# Macro mean
protein_mean = data_mean['Protein'].astype(int)
lipid_mean = data_mean['Lipid'].astype(int)
carb_mean = data_mean['Carbohydrate'].astype(int)

df_macro_mean = pd.DataFrame({
    'Week': data_mean.index,
    'Protein': protein_mean,
    'Lipid': lipid_mean,
    'Carbohydrate': carb_mean,
    'Protein goal': [DAILY_PROTEIN] * len(data_mean.index),
    'Lipid goal': [DAILY_LIPID] * len(data_mean.index),
    'Carbohydrate goal': [DAILY_CARBOHYDRATE] * len(data_mean.index),
    'Lipid min': [DAILY_MIN_LIPID] * len(data_mean.index)
})

ax = df_macro_mean.plot(x='Week', y=['Protein', 'Lipid', 'Carbohydrate'], kind='bar',
                        color=['grey', 'royalblue', 'gold'], figsize=[20, 10])
df_macro_mean.plot(x='Week', y=['Protein goal', 'Lipid goal', 'Carbohydrate goal', 'Lipid min'], kind='line', ax=ax,
                   color=['grey', 'royalblue', 'gold', 'royalblue'])
pp.title('Macro mean')
pp.savefig('../viz/assets/macro-mean.png', bbox_inches="tight", dpi=100)
pp.show()

# Macro sum
# protein_sum = data_sum['Protein'].astype(int)
# lipid_sum = data_sum['Lipid'].astype(int)
# carb_sum = data_sum['Carbohydrate'].astype(int)
#
# df_macro_sum = pd.DataFrame({
#     'Week': data_sum.index,
#     'Protein': protein_sum,
#     'Lipid': lipid_sum,
#     'Carbohydrate': carb_sum,
#     'Protein goal': [WEEKLY_PROTEIN] * len(data_sum.index),
#     'Lipid goal': [WEEKLY_LIPID] * len(data_sum.index),
#     'Carbohydrate goal': [WEEKLY_CARBOHYDRATE] * len(data_sum.index)
# })
#
# ax = df_macro_sum.plot(x='Week', y=['Protein', 'Lipid', 'Carbohydrate'], kind='bar',
#                        color=['grey', 'royalblue', 'gold'], figsize=[20, 10])
# df_macro_sum.plot(x='Week', y=['Protein goal', 'Lipid goal', 'Carbohydrate goal'], kind='line', ax=ax,
#                   color=['grey', 'royalblue', 'gold'])
# pp.title('Macro sum')
# pp.savefig('../viz/assets/macro-sum.png', bbox_inches="tight", dpi=100)
# pp.show()
