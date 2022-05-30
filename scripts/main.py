import matplotlib.pyplot as pp
import pandas as pd
import datetime


def round_to_5(x):
    return 5 * round(x / 5)


def plot_line(index, serie, serie_min, serie_max, title, filename):
    pp.figure(figsize=[20, 10])
    pp.plot(index, serie)
    pp.fill_between(index, serie_min, serie_max, alpha=0.2, color='lightblue')
    # pp.title(title)
    pp.savefig('../viz/assets/' + filename + '.png', bbox_inches="tight", dpi=100)
    pp.show()


PARAMS = {
    # x1.1 : peu ou pas d’exercice/sport (E/S)
    # x1.2 : E/S 1-2 fois par semaine
    # x1.35 : E/S 3-5 fois par semaine
    # x1.45 : E/S 6-7 fois par semaine
    # x1.6-1.8 : E/S 6-7 fois par semaine & travail physique
    "activity": 1.35,
    # Between 1.5 and 2.3
    # the leaner you are and the higher the deficit is
    # the higher this factor should be
    "protein": 2.3,
    # At least 0.7, to stay healthy
    "lipid": 1.5
}

WEEKLY_PARAMS = {
    # "hard": {
    #    "weight": 66,
    # Estimated body fat percentage
    #    "body_fat": 0.2,
    # Deficit percentage
    # Recommended between 10 and 25%
    # The higher it is, the higher should the protein factor be
    #    "deficit": 0.25,
    #    "start_week": 0,
    #    "end_week": 12,
    # },
    "cut": {
        "weight": 66,
        "body_fat": 0.2,
        "deficit": 0.20,
        "start_week": 0,
        "end_week": 13,
    },
    "stabilization": {
        "weight": 63,
        "body_fat": 0.17,
        "deficit": 0.1,
        "start_week": 13,
        "end_week": 19,
    }
}

CAL_PER_PROTEIN_GRAM = 4
CAL_PER_LIPID_GRAM = 9
CAL_PER_CARBOHYDRATE_GRAM = 4
PARAM_MIN_LIPID_FACTOR = 0.7

GOALS = {}

for difficulty_key, params in WEEKLY_PARAMS.items():
    daily_maintenance = round_to_5((370 + 21.6 * (1 - params["body_fat"]) * params["weight"]) * PARAMS["activity"])
    daily_goal = round_to_5((1 - params["deficit"]) * daily_maintenance)
    daily_deficit = round_to_5(daily_maintenance - daily_goal)
    daily_protein = round_to_5(PARAMS["protein"] * (1 - params["body_fat"]) * params["weight"])
    daily_lipid = round_to_5(PARAMS["lipid"] * (1 - params["body_fat"]) * params["weight"])
    daily_min_lipid = round_to_5(PARAM_MIN_LIPID_FACTOR * (1 - params["body_fat"]) * params["weight"])
    daily_carbohydrate = round_to_5(
        (daily_goal - (daily_lipid * CAL_PER_LIPID_GRAM) - (daily_protein * CAL_PER_PROTEIN_GRAM)) /
        CAL_PER_CARBOHYDRATE_GRAM
    )
    GOALS[difficulty_key] = {
        "daily_maintenance": daily_maintenance,
        "daily_goal": daily_goal,
        "daily_deficit": daily_deficit,
        "daily_protein": daily_protein,
        "daily_lipid": daily_lipid,
        "daily_min_lipid": daily_min_lipid,
        "daily_carbohydrate": daily_carbohydrate
    }

follow_up = pd.read_csv('data/follow_up.csv')

# Calorie mean
data_mean = follow_up.groupby('Week').mean()
calories_in = data_mean['Calorie in'].astype(int)
calories_out = data_mean['Calorie out'].astype(int)

for difficulty, params in WEEKLY_PARAMS.items():
    # Calories
    start_week = params["start_week"]
    end_week = params["end_week"]
    daily_goal = GOALS[difficulty]["daily_goal"]
    daily_deficit = GOALS[difficulty]["daily_deficit"]
    daily_maintenance = GOALS[difficulty]["daily_maintenance"]
    daily_protein = GOALS[difficulty]["daily_protein"]
    daily_lipid = GOALS[difficulty]["daily_lipid"]
    daily_carbohydrate = GOALS[difficulty]["daily_carbohydrate"]
    daily_min_lipid = GOALS[difficulty]["daily_min_lipid"]
    adjusted_goal = calories_out.sub(daily_deficit)

    df_cal_mean = pd.DataFrame({
        'Week': data_mean.index[start_week:end_week],
        'Calorie in': calories_in[start_week:end_week],
        'Calorie out': calories_out[start_week:end_week],
        'Adjusted goal': adjusted_goal[start_week:end_week],
        'Estimated goal': [daily_goal] * len(data_mean.index[start_week:end_week])
    })

    ax = df_cal_mean.plot(x='Week',
                          y=['Calorie in', 'Calorie out'],
                          kind='bar',
                          color=['Blue', 'Gray'],
                          figsize=[20, 10])

    df_cal_mean.plot(x='Week',
                     y=['Adjusted goal', 'Estimated goal'],
                     kind='line',
                     ax=ax,
                     color=['Red', 'Black'])

    pp.text(0, daily_goal, daily_goal)

    # pp.title('Calories in/out - ' + difficulty)

    pp.savefig('../viz/assets/cal-in-out-' + difficulty + '.png', bbox_inches="tight", dpi=100)
    pp.show()

    # Weight
    data_weight = follow_up.groupby('Week').mean()
    weight = data_weight['Weight']

    df_weight = pd.DataFrame({
        'Week': data_weight.index[start_week:end_week],
        'Weight': weight[start_week:end_week],
    })

    ax = df_weight.plot(x='Week',
                        y=['Weight'],
                        kind='line',
                        color=['Blue'],
                        figsize=[20, 10])

    # pp.title('Weight - ' + difficulty)

    # Add bar labels
    for container in ax.containers:
        ax.bar_label(container)

    pp.savefig('../viz/assets/weight-' + difficulty + '.png', bbox_inches="tight", dpi=100)
    pp.show()

    # Macro mean
    protein_mean = data_mean['Protein'].astype(int)
    lipid_mean = data_mean['Lipid'].astype(int)
    carb_mean = data_mean['Carbohydrate'].astype(int)

    df_macro_mean = pd.DataFrame({
        'Week': data_mean.index[start_week:end_week],
        'Protein': protein_mean[start_week:end_week],
        'Lipid': lipid_mean[start_week:end_week],
        'Carbohydrate': carb_mean[start_week:end_week],
        'Protein goal': [daily_protein] * len(data_mean.index[start_week:end_week]),
        'Lipid goal': [daily_lipid] * len(data_mean.index[start_week:end_week]),
        'Carbohydrate goal': [daily_carbohydrate] * len(data_mean.index[start_week:end_week]),
        'Lipid min': [daily_min_lipid] * len(data_mean.index[start_week:end_week])
    })

    ax = df_macro_mean.plot(x='Week',
                            y=['Protein', 'Lipid', 'Carbohydrate'],
                            kind='bar',
                            color=['Blue', 'Gray', 'LightBlue'],
                            figsize=[20, 10])

    df_macro_mean.plot(x='Week',
                       y=['Protein goal', 'Lipid min'],
                       kind='line', ax=ax,
                       color=['Blue', 'Gray'])

    # pp.title('Macro mean - ' + difficulty)

    # Add bar labels
    for container in ax.containers:
        ax.bar_label(container)

    pp.savefig('../viz/assets/macro-mean-' + difficulty + '.png', bbox_inches="tight", dpi=100)
    pp.show()

    plot_line(data_mean.index[start_week:end_week],
              calories_in[start_week:end_week],
              adjusted_goal[start_week:end_week],
              [daily_goal] * len(data_mean.index[start_week:end_week]),
              'Calories in - ' + difficulty,
              'cal-in-' + difficulty)

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

df_weight_history.plot(x='Date', y='Weight', kind='scatter', figsize=[20, 10])

# pp.title('Weight history')

pp.savefig('../viz/assets/weight-history.png', bbox_inches="tight", dpi=100)
