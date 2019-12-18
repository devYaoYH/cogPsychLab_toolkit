import sys
import time
import json
import utils
import pandas as pd
import statsmodels.api as sm

def run_regression():
    dataset = pd.read_csv(input("Regression data: "))
    print(dataset)
    with open(input("Output Results File: "), "w+") as fout:
        fout.write(f"Cosine Netowrks (Dijkstra Decay Search) :\n")
        Y = dataset['zRTTarget_trim']
        X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c", f"decay_28"]]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X)
        results = model.fit()
        print(results.summary())
        fout.write(f"{results.summary()}")
        fout.write("\n")

        # fout.write("Covariates:\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")
        
        # fout.write("Control | Word2vec Cosines\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["word2veccosine", "mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")
        
        # fout.write("Control | LSA\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["LSA", "mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")

        # fout.write("Control | Undirected\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c", "Undirected"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")

        # fout.write("Control | newDirected\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c", "newdirected"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")

        # fout.write("Control | pathlength (ACN?)\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c", "pathlength"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")

        # fout.write("Control | UPMFG_Cat\n")
        # Y = dataset['zRTTarget_trim']
        # X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c", "UPMFG_Cat"]]
        # X = sm.add_constant(X)
        # model = sm.OLS(Y, X)
        # results = model.fit()
        # print(results.summary())
        # fout.write(f"{results.summary()}")
        # fout.write("\n")

        # for cutoff in range(28, 36):
        #     fout.write(f"Cosine Netowrks (Dijkstra Search) | Cosine Cutoff connect edges >{cutoff/100.0} :\n")
        #     X = dataset[["mean_len_c", "mean_logf_c", "mean_ldtz_c", "mean_conc_c", f"dijkstra_{cutoff}"]]
        #     X = sm.add_constant(X)
        #     model = sm.OLS(Y, X)
        #     results = model.fit()
        #     print(results.summary())
        #     fout.write(f"{results.summary()}")
        #     fout.write("\n")

if (__name__ == '__main__'):
    run_regression()