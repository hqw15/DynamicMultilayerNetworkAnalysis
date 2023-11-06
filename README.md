# DynamicMultilayerNetworkAnalysis

![Image text](https://github.com/hqw15/DynamicMultilayerNetworkAnalysis/blob/main/img/main.png)

## Introduction

This repo is a tool designed to process [multilayer community network results](https://github.com/GenLouvain/GenLouvain). It provides various metrics and analyses, including modularity, module size, module count, stability, flexibility, cohesion, and separation. Additionally, it calculates the differences between these metrics for patients and healthy individuals and examines their correlation with clinical medical scores for patients.


## Data

To utilize this code, you'll need to download the preprocessed data files to the `/data` directory. You have two options:

1. **Manual Download**: Download the processed data files and save them in the `/data` directory.

2. **Use the Provided Archive**: Alternatively, you can extract the contents of `/data/result.tar`. This archive includes data files related to modularity, flexibility, and the partition matrix for experiments on both healthy individuals and patients.

## Usage

Follow these steps to use the code:

1. Run `python3 preprocessing.py`. This will generate results related to modularity, module size, module count, stability, flexibility, cohesion, and separation for both patients and healthy individuals. The results will be saved in `/data/pre_result`.

2. Run `python3 main.py`. This will calculate the differences in the metrics obtained in step 1 between healthy individuals and patients. It will also examine the correlation between the patient's metrics and clinical medical scores.



- data: 