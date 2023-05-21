#!/usr/bin/env python

import sys
import os
import json
from json import JSONDecoder
import re
import tabulate


def loads_invalid_obj_list(s):
    decoder = JSONDecoder()
    s_len = len(s)
    objs = []
    end = 0
    while end != s_len:
        obj, end = decoder.raw_decode(s, idx=end)
        objs.append(obj)
    return objs


def extract_results_json():
    fin = open('/tmp/perf.out', 'r')
    fout = open('/tmp/results.json', 'w')
    dump = False
    lines = fin.readlines()
    for line in lines:
        if 'Finished Testing.' in line:
            dump = True
        if dump and 'Finished Testing.' not in line:
            fout.write(line)
    return


def analyze_results():
    f = open('/tmp/results.json', 'r')
    json_out = json.load(f)
    results = json_out['results']
    result_table = []
    for result in results:
        # results for a single thread
        thread1 = []
        thread1.append(result['name'])
        thread1.append(1)
        thread1.append(result['results']['1']['ops_per_sec'])

        # results for 2 threads
        thread2 = []
        thread2.append(result['name'])
        thread2.append(2)
        thread2.append(result['results']['2']['ops_per_sec'])
        
        # results for 4 threads
        thread4 = []
        thread4.append(result['name'])
        thread4.append(4)
        thread4.append(result['results']['4']['ops_per_sec'])

        # reconcile
        result_table.append(thread1)
        result_table.append(thread2)
        result_table.append(thread4)

    print(tabulate.tabulate(result_table, headers=['test_name', 'num_threads', 'ops_per_sec']))    


def main():
    # Extract the json portion from the output
    extract_results_json()
    # Load the json to dict and print relevant portions
    analyze_results()

if __name__ == '__main__':
    main()