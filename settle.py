from collections import OrderedDict
import unittest


def settle(balances: dict[str, float]) -> list[tuple[str, str, float]]:
    """
    Settle balances using a minimal number of transactions.
    :param balances: dict[str, float] - dictionary of balances to settle, must sum to zero
    e.g. {'tom': 10, 'jerry': -10, 'spike': 20, 'tyke': -20, 'butch': 0}
    :return: list[tuple[str, str, float]] - list of transactions to settle the balances
    e.g. [('jerry', 'tom', 10), ('tyke', 'spike', 20)]
    """
    neg = {}
    pos = {}

    for member, balance in balances.items():
        if balance < 0:
            neg[member] = - balance
        elif balance > 0:
            pos[member] = balance
    pos = OrderedDict(sorted(pos.items(), key=lambda x: x[0]))
    neg = OrderedDict(sorted(neg.items(), key=lambda x: x[0]))
    return settle_recursive(pos, neg)


def head_rest(balances):
    min_mem = pop_key(balances)
    min_balance = balances[min_mem]
    b = balances.copy()
    del b[min_mem]
    return (min_mem, min_balance), b


def pop_key(d):
    return list(d.keys()).pop(0)


def settle_recursive(pos, neg):
    if len(pos) == 1:
        x = pop_key(pos)
        return [(a, x, b) for a, b in neg.items()]
    if len(neg) == 1:
        x = pop_key(neg)
        return [(x, a, b) for a, b in pos.items()]
    else:
        nm, nr = head_rest(neg)
        pm, pr = head_rest(pos)
        if nm[1] < pm[1]:
            pos[pm[0]] = pm[1] - nm[1]
            transactions = settle_recursive(pos, nr)
            transactions.append((nm[0], pm[0], nm[1]))
            return transactions
        elif nm[1] > pm[1]:
            neg[nm[0]] = nm[1] - pm[1]
            transactions = settle_recursive(pr, neg)
            transactions.append((nm[0], pm[0], pm[1]))
            return transactions
        else:
            transactions = settle_recursive(pr, nr)
            transactions.append((nm[0], pm[0], pm[1]))
            return transactions


class Tests(unittest.TestCase):

    def test_settle_1(self):
        balances = {'A': 10, 'B': -10, 'C': 0}
        self.assertEqual(settle(balances), [('B', 'A', 10)])

    def test_settle_2(self):
        balances = {'A': 10, 'B': -10, 'C': 20, 'D': -20}
        self.assertEqual(set(settle(balances)), {('B', 'A', 10), ('D', 'C', 20)})

    def test_settle_3(self):
        balances = {'A': 10, 'B': -10, 'C': 20, 'D': -30, 'E': 10}
        self.assertEqual(set(settle(balances)), {('B', 'A', 10), ('D', 'C', 20), ('D', 'E', 10)})

    def test_deterministic(self):
        # make 10 random balances whose values sum to zero
        # make sure settle returns the same result for 10 runs
        import random
        for _ in range(10):
            balances = {chr(65 + i): random.randint(-100, 100) for i in range(10)}
            total = sum(balances.values())
            balances[chr(75)] = -total
            for _ in range(10):
                self.assertEqual(settle(balances), settle(balances))
