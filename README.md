# DynamicMultilayerNetworkAnalysis

![Image text](https://github.com/hqw15/DynamicMultilayerNetworkAnalysis/blob/main/img/main.png)

## Introduction

This repository serves as a dedicated tool for the processing of results obtained from the [multilayer community network(GenLouvain)](https://github.com/GenLouvain/GenLouvain). It offers a range of metrics and analyses, encompassing modularity, module size, module number, stationarity, flexibility, cohesion, and disjointedness. Moreover, the tool computes the variations in these metrics between Patients and Healthy Controls (HCs) and calculates the correlation of these metrics with clinical medical scores in the Patients.

## Data

To utilize this code, you'll need to download the preprocessed data files to the `/data` directory. You have two options:

1. **Manual Download**: Download the [processed data files](https://1drv.ms/u/s!AiRytlmhzEl-hFIAeB9bNqZMqbpy?e=0mK70I) and save them in the `/data` directory.

2. **Use the Provided Archive**: Alternatively, you can extract the contents of `/data/result.tar`. This archive includes data files related to modularity, flexibility, and the partition matrix for experiments on both healthy individuals and patients.

## Usage

Follow these steps to use the code:

1. Run `python3 preprocessing.py`. This will generate results related to modularity, module size, module count, stability, flexibility, cohesion, and separation for both patients and healthy individuals. The results will be saved in `/data/pre_result`.

2. Run `python3 main.py`. This will calculate the differences in the metrics obtained in step 1 between healthy individuals and patients. It will also examine the correlation between the patient's metrics and clinical medical scores.
