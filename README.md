# DynamicMultilayerNetworkAnalysis

![Image text](https://github.com/hqw15/DynamicMultilayerNetworkAnalysis/blob/main/img/main.png)

## Introduction

This repository serves as a dedicated tool for the processing of results obtained from the [multilayer community network(GenLouvain)](https://github.com/GenLouvain/GenLouvain). It offers a range of metrics and analyses, encompassing modularity, module size, module number, stationarity, flexibility, cohesion, and disjointedness. Moreover, the tool computes the variations in these metrics between Patients and Healthy Controls (HCs) and calculates the correlation of these metrics with clinical medical scores in the Patients.

## Data

To utilize this code, you'll need to download the 
result file for the multilayer community network(GenLouvain) to the `/data` directory. 
This result files related to modularity, flexibility, and the module assignment results of each experiment.
You have two options:

1. **Manual Download**: Download the [result file](https://1drv.ms/u/s!AiRytlmhzEl-hFIAeB9bNqZMqbpy?e=0mK70I) and save them in the `/data` directory.

2. **Use the Provided Archive**: Alternatively, you can extract the contents of `/data/result.zip`. 

## Usage

Follow these steps to use the code:

1. Run `python3 preprocessing.py`. This will generate results related to modularity, module size, module number, stationarity, flexibility, cohesion, and disjointedness for both Patients and HCs. The results will be saved in `/data/preprocess_result`.

2. Run `python3 main.py`. This will calculate the variations in the metrics obtained in step 1 between HCs and Patients. It will calculate the correlation of these metrics with clinical medical scores in the Patients. The results will be saved in `metric.txt`.

