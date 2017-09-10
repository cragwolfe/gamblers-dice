import numpy as np


class GenericDie(object):
    """
    A die that respects the Gambler's fallacy. Rolling the die is more likely to
    return a result that has not been seen for a while.
    """
    def __init__(self, sides=6, bias='gambler'):
        assert sides > 0
        assert bias in ('gambler', 'random')
        self.sides = sides
        self._rolls_since_last_hit = np.ones(sides)
        self._total_counts = np.zeros(sides)
        self._total_rolls = 0
        self._last_result = None
        self._bias = bias
        
        if self._bias == 'random':
            self._fair_weights = np.ones(sides) / float(sides)
        
    def __repr__(self):
        return 'GenericDie(sides={0})'.format(self.sides)

    @property
    def bias(self):
        return self._bias

    @property
    def n(self):
        return self._total_rolls

    @property
    def counts_std(self):
        return np.std(self._total_counts)
    
    @property
    def freq(self):
        return self._total_counts / float(self._total_rolls)
    
    @property
    def freq_std(self):
        return np.std(self.freq)
    
    @property
    def _weights(self):
        """If 'gambler', calculate the relative probability of each result
        based on the number of rolls since it last occurred. Otherwise
        a uniform probability distribution for the next roll.
        """
        if self._bias == 'random':
            return self._fair_weights
        
        if self._last_result is not None:
            self._update_roll_counter()
        total_streak_rolls = sum(self._rolls_since_last_hit)
        probs = self._rolls_since_last_hit / float(total_streak_rolls)
        return probs

    def _update_roll_counter(self):
        """
        Increment each side's roll count, except for the most recent roll which
        is set back to 1.
        """
        self._rolls_since_last_hit += 1
        self._rolls_since_last_hit[self._last_result] = 1
        return None

    def roll(self):
        """ Roll the die and return the result. """
        sides = range(self.sides)
        result = np.random.choice(
            sides,
            p=self._weights
        )
        self._last_result = result
        self._total_rolls += 1
        self._total_counts[result] += 1

        result += 1  # Account for zero-indexing
        return result

