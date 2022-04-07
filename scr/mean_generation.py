import random
import numpy as np
import pandas as pd

VARIABLES = [
    'Ankle_Moment', 'Knee_Moment', 'Hip_Moment',
    'Ankle_Delta', 'Knee_Delta',
    'Contact_Time', 'Hop_Dist',
    'Ankle_Stiffness', 'Knee_Stiffness', 'Vertical_Stiffness', 'Leg_Stiffness',
    'Peak_vGRF', 'Peak_hGRF', 'Peak_lGRF',
    'Ankle_Power', 'Knee_Power', 'Hip_Power',
    'Rebound_Dist', 'RSI', 'CoM_Delta', 'Leg_Delta'
]
SESSION_KEYS = ['L_1', 'L_2', 'R_1', 'R_2']


def select_random_trials_n_times(var, n=100, cut=.7) -> np.array:
    var = var.to_list()
    n_samples = int(round(len(var) * cut))
    mean_list = []
    for _ in range(0, n):
        mean_list += [np.nanmean(random.choices(var, k=n_samples))]
    return np.nanmean(mean_list)


def mean_nth_trials(var, n) -> np.array:
    var = var.to_list()[:n]
    return np.nanmean(var)


def get_true_mean(df):

    subjects = df.Subject.unique().tolist()
    session_side = SESSION_KEYS
    subject_means = {x: pd.DataFrame(columns=VARIABLES, index=subjects) for x in session_side}

    for subject in subjects:

        subject_mask = df.Subject == subject
        left_mask = df.Side == "'L'"
        session1_mask = df.Session == 1

        sessions = [
            [df[subject_mask & left_mask & session1_mask], 'L_1'],
            [df[subject_mask & left_mask & ~session1_mask], 'L_2'],
            [df[subject_mask & ~left_mask & session1_mask], 'R_1'],
            [df[subject_mask & ~left_mask & ~session1_mask], 'R_2']
        ]

        # select 70 % of data 100 times and mean
        for session_df, session_name in sessions:
            for variable in VARIABLES:
                val = select_random_trials_n_times(session_df[variable], n=100, cut=.7)
                subject_means[session_name].loc[subject, variable] = val

    return subject_means

def get_mean_per_reps(df):

    subjects = df.Subject.unique().tolist()
    session_side = ['L_1', 'L_2', 'R_1', 'R_2']
    means_per_trial = {f'{x}_reps:1to{y}': pd.DataFrame(columns=VARIABLES, index=subjects)
                       for x in session_side
                       for y in range(1, 11)}

    for subject in subjects:

        subject_mask = df.Subject == subject
        left_mask = df.Side == "'L'"
        session1_mask = df.Session == 1

        sessions = [
            [df[subject_mask & left_mask & session1_mask], 'L_1'],
            [df[subject_mask & left_mask & ~session1_mask], 'L_2'],
            [df[subject_mask & ~left_mask & session1_mask], 'R_1'],
            [df[subject_mask & ~left_mask & ~session1_mask], 'R_2']
        ]

        for n_rep in range(1, 11):
            for session_df, session_name in sessions:
                for variable in VARIABLES:
                    val = mean_nth_trials(session_df[variable], n=n_rep)
                    means_per_trial[f'{session_name}_reps:1to{n_rep}'].loc[subject, variable] = val

    return means_per_trial
