import pandas as pd
import numpy as np
import sys


def fix_contributions(x):
    if isinstance(x, float | int):
        return [x]
    return [float(x) for x in x.split(';')]


def fix_exchange_rate(x):
    if isinstance(x, float | int):
        return 1
    return float(x.split(' ')[1])


def fix_members(members):
    return [x.split(' ')[0] for x in members]


def fix_split(split_dict):
    if all(x == split_dict['split_weights'][0] for x in split_dict['split_weights']):
        split_dict['split_weights'] = [1 for _ in split_dict['split_weights']]
        split_dict['total'] = len(split_dict['split_weights'])
    return split_dict


def convert_settleup(file):
    tr = pd.read_csv(file, header=1)

    new_cols = ['by', 'contributions', 'currency', 'for', 'weights',
                'name', 'category', 'date', 'exchange_rate',
                'converted_total', 'expense_type', 'receipt']

    tr.columns = new_cols

    tr['by'] = tr.by.map(lambda x: fix_members(x.split(';')))
    tr['for'] = tr['for'].map(lambda x: fix_members(x.split(';')))
    tr['weights'] = tr.weights.map(lambda x: fix_contributions(x))
    tr['weights'] = tr.weights.map(lambda x: fix_split({'total': sum(x), 'split_weights': x}))

    tr['contributions'] = tr.contributions.map(lambda x: fix_contributions(x))
    tr.contributions = tr.contributions.map(lambda x: {'total': sum(x), 'split_values': x})

    for row in tr.iloc:
        row['weights']['split_values'] = [x * row['contributions']['total'] / row['weights']['total'] for x in
                                          row['weights']['split_weights']]
        row['weights']['members'] = row['for']
        row['contributions']['members'] = row['by']

    del tr['by']
    del tr['for']
    # rename weights and contributions to for and by
    tr = tr.rename(columns={'weights': 'for', 'contributions': 'by'})

    tr['date'] = pd.to_datetime(tr.date).dt.date
    tr['category'] = tr.category.replace(np.nan, '')

    del tr['receipt']
    tr['exchange_rate'] = 1 / tr.exchange_rate.map(fix_exchange_rate)
    return tr


def get_members(tr):
    names = set()
    for x, y in zip(tr['by'], tr['for']):
        names.update(x['members'] + y['members'])
    return names


if __name__ == '__main__':
    import json
    from os.path import join, basename

    tr = convert_settleup(sys.argv[1])
    members = get_members(tr)
    tr_path = join('ledgers', ledger := basename(sys.argv[1]).replace('.csv', '.json'))
    i = input(f'Add new ledger {tr_path} and members/{ledger} [y/n]:')
    if i.lower() != 'y':
        sys.exit(0)
    tr.to_json(tr_path, orient='records')
    with open(join('members', ledger), 'w') as f:
        json.dump(list(members), f)
