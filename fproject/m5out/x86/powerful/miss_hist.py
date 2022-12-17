#!/usr/bin/python

import sys
import re
import numpy as np 
from matplotlib import pyplot as plt

def parse(cprefix = "cpu0", infile=1):
    bin_num = 0
    histo_dict = {}
    if (len(sys.argv) < 4):
        print("Invalid Number of Arguments")
        print("Usage: python histogram.py stats_base.txt stats_flex.txt figure_name")
        return
    with open(sys.argv[infile],'r') as f:
        print("Parsing File " + str(sys.argv[infile]))
        for line in f:
            st_line = line.strip()
            check = re.search(cprefix+"\.dcache\.tags\.set_misses_dist::\d", st_line)
            #check = re.search(cprefix+"\.dcache\.tags\.indexing_policy\.setAccessHist::\d", st_line)
            if check is not None:  
                parsed_line = st_line.split()
                histo_dict[bin_num] = int(parsed_line[1])
                bin_num += 1
    return histo_dict

def plt_hist():
    counted_bins = parse(infile=1)
    print(counted_bins)
    val, weight = zip(*[(k,v) for k,v in counted_bins.items()])
    plt.figure(1)
    plt.grid(True)
    #plt.hist(val, weights=weight)
    plt.hist(counted_bins.keys(), weights=counted_bins.values(), bins=range(64))
    plt.xlabel("Set Index")
    plt.xticks(np.arange(0,64,4))
    plt.ylabel("# of Misses")
    plt.title(str(sys.argv[3]))
    plt.savefig(str(sys.argv[3])+".png")

def plt_2bars():

    counted_bins_base = parse(infile=1)
    counted_bins_flex = parse(infile=2)
    val_base, weight_base = zip(*[(k,v) for k,v in counted_bins_base.items()])
    val_flex, weight_flex = zip(*[(k,v) for k,v in counted_bins_flex.items()])
    print(weight_base)
    print(weight_flex)
    #fig, ax = plt.subplots()
    width = 0.35
    x = np.arange(64)
    plt.bar(x - width/2, weight_base, width, label='Base')
    plt.bar(x + width/2, weight_flex, width, label='Flex')

    #ax.grid(True)
    #plt.hist(val, weights=weight)
    #plt.hist(counted_bins.keys(), weights=counted_bins.values(), bins=range(64))
    plt.xlabel("Set index")
    plt.xticks(np.arange(0,64,4))
    plt.ylabel("# Misses")
    plt.title(str(sys.argv[3]))
    plt.legend()

    #fig.tight_layout()

    plt.savefig(str(sys.argv[3])+".png")

def plt_percent():
    counted_bins_base = parse(infile=1)
    counted_bins_flex = parse(infile=2)
    val_base, weight_base = zip(*[(k,v) for k,v in counted_bins_base.items()])
    val_flex, weight_flex = zip(*[(k,v) for k,v in counted_bins_flex.items()])
    #fig, ax = plt.subplots()
    width = 0.35
    x = np.arange(64)
    change = (np.array(weight_flex) - np.array(weight_base))/np.array(weight_base)
    plt.plot(x, change)

    #ax.grid(True)
    #plt.hist(val, weights=weight)
    #plt.hist(counted_bins.keys(), weights=counted_bins.values(), bins=range(64))
    plt.xlabel("Set index")
    plt.ylabel("# Misses")
    plt.title(str(sys.argv[3]))

    #fig.tight_layout()

    plt.savefig(str(sys.argv[3])+".png")

def main():
    plt_2bars()

if __name__ == "__main__":
    main()