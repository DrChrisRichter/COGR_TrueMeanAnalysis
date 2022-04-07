import matplotlib.pyplot as plt
import numpy as np
import os

import pandas as pd

from .mean_generation import VARIABLES, SESSION_KEYS


LOOKUP_DICT = {
    'L_1': 'Left Limb - Test',
    'L_2': 'Left Limb - Re-Test',
    'R_1': 'Right Limb - Test',
    'R_2': 'Right Limb - Re-Test'
}


def cm2inch(value):
    return value/2.54


def make_plots(findings):

    findings = findings.sort_index()
    mean_df = []

    for variable in VARIABLES:
        fig = plt.figure(figsize=(cm2inch(16), cm2inch(8)))
        ax = fig.add_axes((.15, .15, .84, .82))
        ax.cla()
        curves = []
        for session in SESSION_KEYS:
            ls = '-' if '1' in session else '--'
            c = 'b' if 'L' in session else 'g'
            curve = findings.loc[session, variable]
            ax.plot(curve.r.tolist(), label=LOOKUP_DICT[session], ls=ls, color=c)
            curves += [curve.r.tolist()]
        mean_curve = np.mean(curves, axis=0)
        mean_df += [[variable] + mean_curve.tolist()]
        ax.plot(mean_curve, color='k', marker='o', label='average')
        ax.set_xlabel('mean based on n-trials')
        ax.set_ylabel('pearson r to true mean')
        ax.set_xticks(np.arange(0, 10))
        ax.set_xticklabels(np.arange(1, 11))
        ax.legend()

        if not os.path.exists('findings'):
            os.mkdir('findings')
        fn = os.path.join('findings', variable + '.jpg')
        fig.savefig(fn)
        plt.close(fig)

    df = pd.DataFrame(mean_df, columns=[variable] + [f'corr_{x}' for x in range(1, 11)])
    df.to_csv(os.path.join('findings', 'table.csv'))

