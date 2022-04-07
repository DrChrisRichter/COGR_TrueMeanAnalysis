import numpy as np
import pandas as pd
from .mean_generation import VARIABLES, SESSION_KEYS
from scipy.stats import pearsonr


def correlation_per_nth_trial_mean(mean_per_trial: dict, true_means: dict) -> pd.DataFrame:

    findings = pd.DataFrame(columns=['session', 'variable', 'nreps', 'r', 'n_samples'])
    count = 0
    for var in VARIABLES:
        for session in SESSION_KEYS:
            for n in range(1, 11):
                true = true_means[session].loc[:, var]
                per_trial = mean_per_trial[f'{session}_reps:1to{n}'].loc[true.index.tolist(), var]
                mask = ~np.isnan(true.to_list()) & ~np.isnan(per_trial.to_list())
                r = pearsonr(true[mask], per_trial[mask])
                findings.loc[count] = [session, var, n, r[0], sum(mask)]
                count += 1
    return findings.set_index(['session', 'variable'])