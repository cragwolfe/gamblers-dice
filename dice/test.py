import numpy as np
import pytest

from gamblersdice import GenericDie

def test_gambler_weights():
    sides = 6
    gamblers_die = GenericDie(sides=sides, bias='gambler')
    zero_indexed_roll = gamblers_die.roll() -1
    weights = gamblers_die._weights
    for i in range(sides):
        if i == zero_indexed_roll:
            assert gamblers_die._rolls_since_last_hit[i] == 1
            assert weights[i] == 1 / (2 * 5 + 1)
        else:
            assert gamblers_die._rolls_since_last_hit[i] == 2
            assert weights[i] == 2 / (2 * 5 + 1)

    last_weights = weights.copy()
    last_rolls_since_last_hit = gamblers_die._rolls_since_last_hit.copy()
    gamblers_die._last_result = 0
    weights = gamblers_die._weights
    assert gamblers_die._rolls_since_last_hit[0] == 1
    assert weights[0] < last_weights[0]
    for i in range(1,sides):
        assert (gamblers_die._rolls_since_last_hit[i] ==
                last_rolls_since_last_hit[i] + 1)
        assert weights[i] > last_weights[i]


def test_fair_weights():
    sides = 7
    fair_die = GenericDie(sides=sides, bias='random')
    expected_weights = np.ones(sides) / float(sides)
    for i in range(sides):
        assert fair_die._weights[i] == expected_weights[i]
    fair_die.roll()
    fair_die.roll()
    for i in range(sides):
        assert fair_die._weights[i] == expected_weights[i]

def test_total_rolls():
    sides = 12
    gamblers_die = GenericDie(sides=sides, bias='gambler')
    fair_die = GenericDie(sides=sides, bias='random')
    for i in range(10):
        gamblers_die.roll()
        fair_die.roll()
    assert gamblers_die.n == 10
    assert fair_die.n == 10

    assert sum(gamblers_die._total_counts) == 10
    assert sum(fair_die._total_counts) == 10
