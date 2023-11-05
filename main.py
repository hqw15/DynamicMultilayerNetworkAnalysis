import os
import numpy as np
import scipy.stats as stats
import lib.utils as utils
from lib.data_reader import DataReader


class Metric:

    def __init__(self):
        self.exp_dir = 'data/preprocess_result'
        self.sub_dir = ['H', 'P']
        self.node_num = 90

        self.reader = DataReader()

        self.logging_writer = open('metric.txt', 'w')

    def compute_basic_info_metric(self):
        self.logging_writer.write(
            "==================== Basic info (HCs and Patients) =======================\n"
        )
        self._basic_info_metric(a_info=self.reader.healthy_info,
                                b_info=self.reader.patient_info,
                                a_header=self.reader.healthy_info_header,
                                b_header=self.reader.patient_info_header,
                                a_name='HCs',
                                b_name='Patients')

    def _basic_info_metric(self, a_info, b_info, a_header, b_header, a_name,
                           b_name):

        # 1. people nums
        a_nums, b_nums = len(a_info), len(b_info)
        # 2. age
        a_ages = utils.get_data_by_name(a_info, a_header, 'Age')
        b_ages = utils.get_data_by_name(b_info, b_header, 'Age')
        age_res = utils.independent_sample_test(a_ages,
                                                b_ages,
                                                name_a=f'{a_name}_Age',
                                                name_b=f'{b_name}_Age')
        # 3. sex
        a_sexs = utils.get_data_by_name(a_info, a_header,
                                        'Sex(1:male;2:Female)')
        b_sexs = utils.get_data_by_name(b_info, b_header,
                                        'Sex(1:male;2:Female)')
        a_sexs = [a_sexs.count(1), a_sexs.count(2)]
        b_sexs = [b_sexs.count(1), b_sexs.count(2)]
        sex_res = utils.chi2_contingency_test(a_sexs,
                                              b_sexs,
                                              name_a=f'{a_name}_Sex',
                                              name_b=f'{b_name}_Sex')

        self.logging_writer.write(
            f'Num of {a_name}:{a_nums},  Num of {b_name}:{b_nums}\n')
        self.logging_writer.write('Age: ' + str(age_res) + '\n')
        self.logging_writer.write('Sex: ' + str(sex_res) + '\n')

    def _correlation_test(self, dp):
        scores = ['FMA-U', 'FMA-L', 'FMA']
        fma_score = self.reader.get_score('FMA')
        new_dp = utils.filter_data_with_score_less_than_80(dp, fma_score)

        correlation_result = list()
        for score in scores:
            new_score = utils.filter_data_with_score_less_than_80(
                self.reader.get_score(score), fma_score)
            correlation_result.append(
                utils.correlation(new_dp,
                                  new_score,
                                  x_name='Patients',
                                  y_name=score))
        return correlation_result

    def _metric(self, dh, dp):
        hp_test_res = utils.independent_sample_test(dh,
                                                    dp,
                                                    name_a='HCs',
                                                    name_b='Patients')

        corr_test_res = self._correlation_test(dp)
        return hp_test_res, corr_test_res

    def measure_metric(self, name):
        self.logging_writer.write(
            f"\n\n==================== {name} =======================\n")
        h_data = self.reader.read_one_dim_data(
            os.path.join(f'{self.exp_dir}', f'{name}_H.txt'))
        p_data = self.reader.read_one_dim_data(
            os.path.join(f'{self.exp_dir}', f'{name}_P.txt'))

        hp_test_res, corr_test_res = self._metric(h_data, p_data)

        self.logging_writer.write(str(hp_test_res) + '\n')
        for res in corr_test_res:
            self.logging_writer.write(str(res) + '\n')

    def measure_other_metric(self, name):
        self.logging_writer.write(
            f"\n\n==================== {name} =======================\n")
        h_data = self.reader.read_two_dim_data(
            os.path.join(f'{self.exp_dir}', f'{name}_H.txt'))
        p_data = self.reader.read_two_dim_data(
            os.path.join(f'{self.exp_dir}', f'{name}_P.txt'))

        # networks
        p_values_before_fdr = list()
        network_res = list()
        network_data_dict = self.reader.get_network_mean_data({
            'H': h_data,
            'P': p_data
        })
        for network in self.reader.network:
            hp_test_res, corr_test_res = self._metric(
                dh=network_data_dict[network]['H'],
                dp=network_data_dict[network]['P'])
            network_res.append([hp_test_res, corr_test_res])
            p_values_before_fdr.append(hp_test_res['pvalue'])

        p_values_after_fdr = utils.fdr_correction(p_values_before_fdr)
        for i in range(len(network_res)):
            network_res[i][0]['pvalue_fdr'] = p_values_after_fdr[i]

        for i, network in enumerate(self.reader.network):
            self.logging_writer.write(f'Network: {network}\n')
            hp_test_res, corr_test_res = network_res[i]
            self.logging_writer.write(str(hp_test_res) + '\n')
            for res in corr_test_res:
                self.logging_writer.write(str(res) + '\n')

        # whole head
        hp_test_res, corr_test_res = self._metric(h_data.mean(1),
                                                  p_data.mean(1))
        self.logging_writer.write(f'Whole Head\n')
        self.logging_writer.write(str(hp_test_res) + '\n')
        for res in corr_test_res:
            self.logging_writer.write(str(res) + '\n')


if __name__ == '__main__':

    metric = Metric()

    metric.compute_basic_info_metric()

    metric.measure_metric('modularity')
    metric.measure_metric('community_num')
    metric.measure_metric('community_size')
    metric.measure_metric('stationarity')

    metric.measure_other_metric('flexibility')
    metric.measure_other_metric('cohesion')
    metric.measure_other_metric('disjointedness')
