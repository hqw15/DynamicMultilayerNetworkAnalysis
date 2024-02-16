import re
import os
import numpy as np
import scipy.stats as stats
from scipy.stats import pearsonr, spearmanr

def extract_p(summary):
    summary = str(summary).replace(' ','')
    f_pattern = r'F-statistic:(\d+\.\d+)'
    p_pattern = r'Prob\(F-statistic\):(\d+\.\d+)'
    f_matches = re.findall(f_pattern, summary)
    p_matches = re.findall(p_pattern, summary)
    return (f_matches, p_matches)

def mkdir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def get_data_by_name(info, header, name):
    data = info[:, header.index(name)]
    data = [int(v) for v in data]
    return data


def filter_data_with_score_less_than_80(data, score):
    assert len(data) == len(score)
    filter_data = list()
    for d, s in zip(data, score):
        if s >= 80:
            filter_data.append(d)
    # print(f'split: remain_num={len(filter_data)}, total_num={len(data)}')
    return np.array(filter_data)


def fdr_correction(pvalues):
    sorted_id = sorted(range(len(pvalues)), key=lambda x: pvalues[x])
    fdr_pvalues = [
        pvalues[i] * len(pvalues) / (len(pvalues) - sorted_id.index(i))
        for i in range(len(pvalues))
    ]
    return fdr_pvalues


def independent_sample_test(da, db, name_a='', name_b=''):
    ta = stats.kstest(da, 'norm', (np.mean(da), np.std(da)))
    tb = stats.kstest(db, 'norm', (np.mean(db), np.std(db)))
    if (ta.pvalue < 0.05 or tb.pvalue < 0.05):
        res = stats.ranksums(da, db)
        method = 'ranksums'
    else:
        lres = stats.levene(da, db)
        res = stats.ttest_ind(a=da, b=db, equal_var=lres.pvalue > 0.05)
        method = 'ttest_ind'

    import pandas as pd
    import statsmodels.formula.api as smf

    # 将数据组合成 DataFrame
    df_a = pd.DataFrame({'group': 'A', 'score': da})
    df_b = pd.DataFrame({'group': 'B', 'score': db})
    df = pd.concat([df_a, df_b], ignore_index=True)

    # 使用公式模型
    model = smf.ols('score ~ group', data=df).fit()
    result = '\n' + str(model.summary()) + '\n'
    print (result)

    return {
        # '(F-统计值 and P(矫正))': extract_p(result),
        'pvalue_fdr': res.pvalue,
        f'{name_a}_mean': np.mean(da),
        f'{name_a}_std': np.std(da),
        f'{name_b}_mean': np.mean(db),
        f'{name_b}_std': np.std(db),
        'method': method,
        'statistic': res.statistic,
    }


def paired_sample_test(da, db, name_a='', name_b=''):
    assert len(da) == len(db)
    res = stats.ttest_rel(da, db)
    return {
        'pvalue': res.pvalue,
        f'{name_a}_mean': np.mean(da),
        f'{name_a}_std': np.std(da),
        f'{name_b}_mean': np.mean(db),
        f'{name_b}_std': np.std(db),
        'method': 'ttest_rel',
        'statistic': res.statistic,
    }


def chi2_contingency_test(da, db, name_a='', name_b=''):
    pvalue = stats.chi2_contingency([da, db], correction=True)[1],
    return {
        'pvalue': pvalue,
        f'{name_a}_(male : female)': da,
        f'{name_b}_(male : female)': db,
        'method': 'chi2_contingency_test',
    }


def correlation(x, y, x_name='', y_name=''):
    assert len(x) == len(y)
    t = stats.kstest(x, 'norm', (np.mean(x), np.std(x)))
    if t.pvalue < 0.05:
        method = 'spearmanr'
        r = spearmanr(x, y)
    else:
        method = 'pearsonr'
        r = pearsonr(x, y)

    return {
        'pvalue': r[1],
        'r': r[0],
        'method': method,
        'X': x_name,
        'Y': y_name,
    }
