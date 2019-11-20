import utils
import sys
import time
import math
import pandas as pd

EPSILON = 0.0000000001

def zScore(data, sd_filter=None):
    f_data = [d for d in data if d is not None]
    d_len = len(f_data)
    d_sum = sum(f_data)
    mean = d_sum/float(d_len)
    std = math.sqrt(sum([d**2 for d in data if d is not None])/float(d_len) - mean**2)
    ret_data = [(d-mean)/std if d is not None else None for d in data]
    assert(abs(sum([d for d in ret_data if d is not None])/float(d_len)) < EPSILON)
    if (sd_filter is not None):
        for i in range(len(ret_data)):
            if (ret_data[i] < -sd_filter or ret_data[i] > sd_filter):
                ret_data[i] = None
    return ret_data

def filter_outliers(data, k=0, bounds=[-1, 1]):
    ret_d = []
    for d in data:
        if (d[k] > bounds[0] and d[k] < bounds[1]):
            ret_d.append(d)
    return ret_d

def individual_RT_zScore():
    # dataset = pd.read_csv(input("Regression data: "))
    data = utils.load_data(input("Raw RT file: "), expt=4, d_filter=[int, utils.sanitize_lower, utils.sanitize_lower, int])
    data = filter_outliers(data, k=3, bounds=[250, 7000])
    subject_data = dict()
    for d in data:
        if (d[0] not in subject_data):
            subject_data[d[0]] = {'rt': [], 'raw': []}
        subject_data[d[0]]['rt'].append(d[3])
        subject_data[d[0]]['raw'].append(d)
    for si in subject_data.keys():
        subject_data[si]['rt'] = zScore(subject_data[si]['rt'], sd_filter=3)
        subject_data[si]['rt'] = zScore(subject_data[si]['rt'])
    # Reconstruct raw data
    w_raw = []
    si_li = sorted(list(subject_data.keys()))
    for si in si_li:
        for i, d in enumerate(subject_data[si]['raw']):
            w_raw.append([d_ if d_ is not None else "N/A" for d_ in d + [subject_data[si]['rt'][i]]])
    utils.write_data(input("Output File: "), w_raw)

def item_level_mean():
    data = utils.load_data(input("RT Pairs zScored: "), expt=3, d_filter=[utils.sanitize_lower, utils.sanitize_lower, float])
    wp_means = dict()
    for d in data:
        wp_key = tuple(sorted(d[:2]))
        if (wp_key not in wp_means):
            wp_means[wp_key] = []
        wp_means[wp_key].append(d[2])
    for wp_key in wp_means.keys():
        wp_means[wp_key] = sum(wp_means[wp_key])/float(len(wp_means[wp_key]))
    out_data = []
    wp_li = sorted(list(wp_means.keys()))
    for k in wp_li:
        out_data.append([k[0], k[1], wp_means[k]])
        out_data.append([k[1], k[0], wp_means[k]])
    utils.write_data(input("Output File: "), sorted(out_data))

def combine_data():
    utils.write_data(input("Output File: "), utils.join_data([input("file 1: "), input("file 2: ")], expt=[3, 14], 
        d_filter=[[utils.sanitize_lower, utils.sanitize_lower, float], [utils.sanitize_lower, utils.sanitize_lower, float, float, float, int, int, int, int, int, int, int, int, int]]))

def combine_regression_data():
    utils.write_data(input("Output File: "), utils.join_data([input("file 1: "), input("file 2: ")], expt=[5, 3], 
        d_filter=[[utils.sanitize_lower, utils.sanitize_lower, float, float, float], [utils.sanitize_lower, utils.sanitize_lower, float]]))

if (__name__ == "__main__"):
    # individual_RT_zScore()
    # item_level_mean()
    # combine_data()
    print("Hello!")