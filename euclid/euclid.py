from itertools import cycle


class EuclideanSequence(object):
    """
    Wraps a euclidean_rhythm
    """

    def __init__(self, k, n):
        self.k, self.n = k, n
        self.reset()

    @property
    def pattern(self):
        if not hasattr(self, '_pattern'):
            self._pattern = euclidean_rhythm(self.k, self.n)
        return self._pattern

    @pattern.setter
    def pattern(self, e):
        self._pattern = euclidean_rhythm(*e)

    def reset(self):
        self.pattern = (self.k, self.n)

    def rotate(self):
        self.pattern.next()

    def step(self):
        return self.pattern.next()

    def __str__(self):
        e = euclidean_rhythm(self.k, self.n)
        return '{0:9} {1}'.format(
            'E({0}, {1})'.format(self.k, self.n),
            [e.next() for _ in range(self.n)]
        )


# Where n is the length of the sequence's period and k is the number
# of active steps in the sequence
# adapted from https://github.com/danpprince/euclidean-seq
def euclidean_rhythm(k, n):
    """
    >>> n = 16
    >>> for k in range(1, n):
    ...     e = euclidean_rhythm(k, n)
    ...     print tuple(e.next() for _ in range(n)), (k, n)
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) (1, 16)
    (1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0) (2, 16)
    (1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0) (3, 16)
    (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0) (4, 16)
    (1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0) (5, 16)
    (1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0) (6, 16)
    (1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0) (7, 16)
    (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0) (8, 16)
    (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1) (9, 16)
    (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1) (10, 16)
    (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1) (11, 16)
    (1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1) (12, 16)
    (1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) (13, 16)
    (1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) (14, 16)
    (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) (15, 16)
    """
    # If either parameter is zero, our beat is all 0s
    if 0 in (k, n):
        return cycle([0])
    # If k >= n, our beat is all 1s
    if k >= n:
        return cycle([1])

    # Keep track of the number of inactive and active steps
    # remaining to distribute
    inactive, active = [n - k], [k]

    # Compute the Euclidean algorithm recursively
    #    m, k: Parameters describing the current two divisors for
    #          the Euclidean GCD calculation
    #    steps: A list of lists indicating the currently constructed
    #           sequence
    #
    #    [0] represents an inactive step
    #    [1] represents an active step
    def euclid(m, k, steps):
        # If all active steps have been distributed, or if there are
        # no inactive steps to distribute, return the final result with
        # all of the remaining inactive steps being evenly distributed.
        if k == 0 or inactive[0] == 0:
            return map(lambda x: x + [0] * (inactive[0] / active[0]), steps)
        else:
            # Distribute an inactive step to each list
            inactive[0] = inactive[0] - k
            return euclid(
                k, m % k, map(lambda x: x + [0], steps[:k]) + steps[k:]
            )

    # Return a generator that infinitely repeats a cycle of the sequence
    # resulting from the Euclidean algorithm
    return cycle(reduce(
        lambda x, y: x + y,
        euclid(
            max(active[0], inactive[0]),
            min(active[0], inactive[0]),
            [[1]] * k
        )
    ))
