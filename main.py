import pandas as pd
import scr


def run_code():

    file = 'HopTestDataMATLAB_June2020.xlsx'
    df = pd.read_excel(file)

    simulated_mean = scr.get_true_mean(df)
    mean_per_rep = scr.get_mean_per_reps(df)
    results = scr.correlation_analysis(mean_per_rep, simulated_mean)
    scr.plotting(results)

    hu = 6


if __name__ == '__main__':
    run_code()
