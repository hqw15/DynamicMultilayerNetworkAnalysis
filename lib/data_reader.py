import numpy as np
import csv


class DataReader:

    def __init__(self):
        self.node_num = 90

        self.network_path = 'data/ALL_net.txt'
        self.patient_info_path = 'data/StrokePatients.csv'
        self.healthy_info_path = 'data/HCs.csv'
        self.score_file_path = 'data/StrokePatients.csv'

        self.people_nums = {
            'H': 31,
            'P': 46,
        }

        self._read_score_csv()
        self._read_network_info()
        self._read_base_info()

    def _read_base_info(self):
        self.patient_info = list()
        with open(self.patient_info_path, 'r') as f:
            csv_reader = csv.reader(f)
            for i, row in enumerate(csv_reader):
                if len(row[0].strip()) == 0:
                    continue
                if i == 0:
                    self.patient_info_header = row[1:]
                else:
                    self.patient_info.append(row[1:])
        self.patient_info = np.array(self.patient_info)

        self.healthy_info = list()
        with open(self.healthy_info_path, 'r') as f:
            csv_reader = csv.reader(f)
            for i, row in enumerate(csv_reader):
                if len(row[0].strip()) == 0:
                    continue
                if i == 0:
                    self.healthy_info_header = row[1:]
                else:
                    self.healthy_info.append(row[1:])
        self.healthy_info = np.array(self.healthy_info)

    def _read_score_csv(self):
        self.score_header = None
        self.score_matrix = list()
        with open(self.score_file_path, 'r') as f:
            csv_reader = csv.reader(f)
            for i, row in enumerate(csv_reader):
                if i == 0:
                    self.score_header = row[2:]
                    continue
                row = [float(r) for r in row[2:]]
                self.score_matrix.append(row)
        self.score_matrix = np.array(self.score_matrix)

    def get_score(self, name):
        return self.score_matrix[:, self.score_header.index(name)]

    def get_network_mean_data(self, data_dict):
        for k in data_dict:
            assert data_dict[k].shape[1] == self.node_num
        res_dict = dict()
        for n in self.network:
            res_dict[n] = dict()
            for k in data_dict:
                data = np.zeros_like(data_dict[k][:, 0])
                for node in self.network[n]:
                    data += data_dict[k][:, node - 1]
                res_dict[n][k] = data / len(self.network[n])
        return res_dict

    def _read_numpy(self, path):
        return np.load(path)

    def _read_network_info(self):
        self.network = {
            'Sensorimotor System': [],
            'Visual System': [],
            'Attention System': [],
            'Default Mode System': [],
            'Subcortical  System': []
        }
        lines = open(self.network_path, 'r').readlines()
        curr_network = None
        node_list = list()
        for line in lines:
            line = line.strip()
            if line in self.network:
                curr_network = line
                continue
            node_id = int(line.split(' ')[0])
            self.network[curr_network].append(node_id)
            node_list.append(node_id)
        assert len(node_list) == len(set(node_list))
        assert np.min(node_list) == 1
        assert np.max(node_list) == len(node_list)

    def read_one_dim_data(self, file_path):
        lines = open(file_path, 'r').readlines()
        data = [float(line.strip()) for line in lines]
        return data

    def read_two_dim_data(self, file_path, convert_numpy=True):
        """N x T: N:num of nodes T: times"""
        lines = open(file_path, 'r').readlines()
        data = list()
        for line in lines:
            line = line.strip().split(" ")
            remove_black_line = list()
            for v in line:
                if len(v):
                    remove_black_line.append(float(v))
            data.append(remove_black_line)

        if convert_numpy:
            data = np.array(data)

        return data
