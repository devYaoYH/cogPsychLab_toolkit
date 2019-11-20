import sys
import time
import json
import utils
import pandas as pd
import statsmodels.api as sm

def run_regression():
    dataset = pd.read_csv(input("Regression data: "))
    print(dataset)
    # Y = dataset['zRTTarget_trim']
    # X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c"]]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()

    Y = dataset['Z_RT']
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_25']]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_30']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_35']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_40']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_45']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_50']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_undirected']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_pmfg']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())
    # X = dataset[['LDTZ', 'LENGTH', 'LOG_F', 'PATH_kennet']]
    # X = sm.add_constant(X)
    # model = sm.OLS(Y, X)
    # results = model.fit()
    # print(results.summary())

if (__name__ == '__main__'):
    #utils.write_data(input("Output File: "), utils.join_data([input("Regression Data File: "), input("Pathlengths File: ")], expt=[6, 3], 
    #    d_filter=[[utils.sanitize_lower, utils.sanitize_lower, float, float, float, float], [utils.sanitize_lower, utils.sanitize_lower, int]]))
    run_regression()