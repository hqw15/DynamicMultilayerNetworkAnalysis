import numpy as np


class DataWriter:

    def __init__(self):
        pass

    def write_one_dim_list(self, data, path):
        assert len(np.array(data).shape) == 1
        f = open(path, 'w')
        for d in data:
            f.write(str(d) + '\n')
        f.close()

    def write_two_dim_list(self, data, path):
        assert len(np.array(data).shape) == 2
        f = open(path, 'w')
        for line in data:
            for d in line:
                f.write(str(d) + ' ')
            f.write('\n')
        f.close()
