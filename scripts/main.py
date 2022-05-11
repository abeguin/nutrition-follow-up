import matplotlib.pyplot as pp
import pandas as pd
import datetime


def round_to_5(x):
    return 5 * round(x / 5)


PARAM_WEIGHT = 66

# Estimated body fat percentage
PARAM_BODY_FAT = 0.2

# x1.1 : peu ou pas d’exercice/sport (E/S)
# x1.2 : E/S 1-2 fois par semaine
# x1.35 : E/S 3-5 fois par semaine
# x1.45 : E/S 6-7 fois par semaine
# x1.6-1.8 : E/S 6-7 fois par semaine & travail physique
PARAM_ACTIVITY_FACTOR = 1.35

# Deficit percentage
# Recommended between 10 and 25%
# The higher it is, the higher should the protein factor be
PARAM_DEFICIT = 0.25

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

ax = df_cal_mean.plot(x='Week',
                      y=['Calorie in', 'Calorie out'],
                      kind='bar',
                      colormap='Blues',
                      figsize=[20, 10])

df_cal_mean.plot(x='Week',
                 y=['Adjusted goal', 'Estimated goal'],
                 kind='line',
                 ax=ax,
                 colormap='Blues')

pp.text(10, DAILY_GOAL, DAILY_GOAL)

pp.title('Calorie mean')

pp.savefig('../viz/assets/cal-mean.png', bbox_inches="tight", dpi=100)
pp.show()

# Weight
data_weight = follow_up.groupby('Week').mean()
weight = data_weight['Weight']

df_weight = pd.DataFrame({
    'Week': data_weight.index,
    'Weight': weight,
})

ax = df_weight.plot(x='Week',
                    y=['Weight'],
                    kind='line',
                    color=['royalblue'],
                    figsize=[20, 10])
pp.title('Weight')

# Add bar labels
for container in ax.containers:
    ax.bar_label(container)

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

ax = df_macro_mean.plot(x='Week',
                        y=['Protein', 'Lipid', 'Carbohydrate'],
                        kind='bar',
                        colormap='Blues',
                        figsize=[20, 10])
df_macro_mean.plot(x='Week',
                   y=['Protein goal', 'Lipid goal', 'Carbohydrate goal', 'Lipid min'],
                   kind='line', ax=ax,
                   colormap='Blues')
pp.title('Macro mean')

# Add bar labels
for container in ax.containers:
    ax.bar_label(container)

pp.savefig('../viz/assets/macro-mean.png', bbox_inches="tight", dpi=100)
pp.show()

df_weight_history = pd.DataFrame({
    'Date': [
        datetime.date(2019, 9, 1),
        datetime.date(2020, 3, 1),
        datetime.date(2020, 12, 1),
        datetime.date(2021, 12, 1),
    ],
    'Weight': [
        62.0,
        63.5,
        67.0,
        67.0
    ]
})

df_weight_history.plot(x = 'Date', y= 'Weight', kind='scatter', figsize=[20,10])

pp.title('Weight history')

pp.savefig('../viz/assets/weight-history.png', bbox_inches="tight", dpi=100)

def plot_line(index, serie, serie_min, serie_max, title, filename):
    pp.figure(figsize=[20, 10])
    pp.plot(index, serie)
    pp.fill_between(index, serie_min, serie_max, alpha=0.2)
    pp.title(title)
    pp.savefig('../viz/assets/' + filename + '.png', bbox_inches="tight", dpi=100)
    pp.show()


plot_line(df_cal_mean['Week'], df_cal_mean['Calorie in'], df_cal_mean['Estimated goal'], df_cal_mean['Adjusted goal'],
          'Calories in', 'cal-in')
plot_line(df_cal_mean['Week'], df_cal_mean['Calorie out'], df_cal_mean['Estimated goal'], df_cal_mean['Adjusted goal'],
          'Calories in', 'cal-in')
