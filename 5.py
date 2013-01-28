eratosthenes = lambda n: sorted(
                            set(xrange(2, n))
                                - set(
                                        (p * f) for p in xrange(2, int(n ** 0.5) + 2)
                                                    for f in xrange(2, (n / p) + 1)
                                                        )
                                                            )

assert eratosthenes(2) == []
assert eratosthenes(3) == [2]
assert eratosthenes(4) == [2,3]
assert eratosthenes(30) == [2,3,5,7,11,13,17,19,23,29]