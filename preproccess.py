import os
import glob
import numpy as np
import lib.utils as utils
from lib.data_reader import DataReader
from lib.data_writer import DataWriter


class PreProcesser:

    def __init__(self):
        self.res_dir = 'data/result'
        self.save_dir = 'data/preprocess_result'
        self.num_of_exp = 50
        self.node_num = 90

        self.sub_dir = ['H', 'P']

        self.reader = DataReader()
        self.writer = DataWriter()

        utils.mkdir(self.save_dir)

    def _compute_community(self, network_result):
        """
        network_result: N x T: nodes x times
        """
        times = network_result.shape[1]
        assert network_result.shape[0] == self.node_num

        community = network_result.flatten().tolist()
        community_set = set(community)

        community_num = len(community_set)
        community_size = len(community) / len(community_set)

        stationarity_count = dict()
        for c in community_set:
            stationarity_count[c] = list()
        for t in range(times):
            c_set = set(network_result[:, t].tolist())
            for c in c_set:
                node_list = np.where(network_result[:, t] == c)[0].tolist()
                stationarity_count[c].append(node_list)

        all_stationarity = list()
        for c in stationarity_count:
            u_count = 0
            delta_t = len(stationarity_count[c]) - 1
            if delta_t == 0:
                all_stationarity.append(1)
                continue
            for i in range(delta_t):
                node_list_1 = stationarity_count[c][i + 1]
                node_list_2 = stationarity_count[c][i]
                union = set(node_list_1).union(set(node_list_2))
                inter = set(node_list_1).intersection(set(node_list_2))
                u_count += len(inter) / len(union)
            u_count /= delta_t
            all_stationarity.append(u_count)

        stationarity = np.mean(all_stationarity)

        return community_num, community_size, stationarity

    def _compute_cohesion_disjointedness(self, network_result):
        """
        network_result: N x T: nodes x times
        """
        times = network_result.shape[1]
        assert network_result.shape[0] == self.node_num

        node_change_dict = dict()
        for i in range(self.node_num):
            node_change_dict[i] = list()
            for t in range(times - 1):
                if network_result[i, t] != network_result[i, t + 1]:
                    node_change_dict[i].append(t)

        cohesion_mat = np.zeros([self.node_num, self.node_num])
        cohesion_list = list()
        disjointedness_list = list()
        for i in range(self.node_num):
            same_list = list()
            for j in range(self.node_num):
                if i == j:
                    continue
                same_change_times = set(node_change_dict[i]) & set(
                    node_change_dict[j])
                assert same_change_times == set(
                    node_change_dict[i]).intersection(set(node_change_dict[j]))
                m = 0
                for t in same_change_times:
                    if (network_result[i, t] == network_result[j, t]
                            and network_result[i, t + 1]
                            == network_result[j, t + 1]):
                        m += 1
                        same_list.append(t)
                cohesion_mat[i, j] = m

            cohesion_list.append(np.sum(cohesion_mat[i]) / (times - 1))
            disjointedness_list.append(
                len(set(node_change_dict[i]) - set(same_list)) / (times - 1))

        return cohesion_list, disjointedness_list

    def preprocess_modularity(self, file_name='Q_all_subjects.txt'):
        for sd in self.sub_dir:
            path = os.path.join(self.res_dir, sd, file_name)
            self.writer.write_one_dim_list(
                data=self.reader.read_one_dim_data(path),
                path=f'{self.save_dir}/modularity_{sd}.txt')

    def preprocess_flexibility(self,
                               file_name='switching_rates_all_subjects.txt'):
        for sd in self.sub_dir:
            path = os.path.join(self.res_dir, sd, file_name)
            self.writer.write_two_dim_list(
                data=self.reader.read_two_dim_data(path),
                path=f'{self.save_dir}/flexibility_{sd}.txt')

    def preprocess_main_metric(self):
        for sd in self.sub_dir:
            res_dir = os.path.join(self.res_dir, sd, 'result')
            people_list = list(set(os.listdir(res_dir)) - set(['.DS_Store']))
            print(sd, ' people num: ', len(people_list))

            community_num_res = list()
            community_size_res = list()
            stationarity_res = list()

            cohesion_res = list()
            disjointedness_res = list()

            people_list.sort()
            for people in people_list:
                print(people)
                exp_result_list = glob.glob(
                    os.path.join(res_dir, people, '*.txt'))
                assert len(exp_result_list) == self.num_of_exp

                community_num_list = list()
                community_size_list = list()
                stationarity_list = list()

                cohesion_list = list()
                disjointedness_list = list()

                for _, exp_result_file in enumerate(exp_result_list):
                    network_result = self.reader.read_two_dim_data(
                        exp_result_file)
                    assert network_result.shape[0] == self.node_num

                    community_num, community_size, stationarity = self._compute_community(
                        network_result)
                    community_num_list.append(community_num)
                    community_size_list.append(community_size)
                    stationarity_list.append(stationarity)

                    cohesion, disjointedness = self._compute_cohesion_disjointedness(
                        network_result)
                    cohesion_list.append(cohesion)
                    disjointedness_list.append(disjointedness)

                community_num_res.append(np.mean(community_num_list))
                community_size_res.append(np.mean(community_size_list))
                stationarity_res.append(np.mean(stationarity_list))

                cohesion_res.append(np.mean(cohesion_list, axis=0))
                disjointedness_res.append(np.mean(disjointedness_list, axis=0))

            # 存储
            self.writer.write_one_dim_list(
                data=community_num_res,
                path=f'{self.save_dir}/community_num_{sd}.txt')
            self.writer.write_one_dim_list(
                data=community_size_res,
                path=f'{self.save_dir}/community_size_{sd}.txt')
            self.writer.write_one_dim_list(
                data=stationarity_res,
                path=f'{self.save_dir}/stationarity_{sd}.txt')

            self.writer.write_two_dim_list(
                data=cohesion_res, path=f'{self.save_dir}/cohesion_{sd}.txt')
            self.writer.write_two_dim_list(
                data=disjointedness_res,
                path=f'{self.save_dir}/disjointedness_{sd}.txt')


if __name__ == '__main__':

    processer = PreProcesser()

    processer.preprocess_modularity()
    processer.preprocess_flexibility()
    processer.preprocess_main_metric()
