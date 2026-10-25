"""Contract operations in the coverage set that no ergonomic method wraps yet.

The coverage set is every operation whose ``x-listeners`` contains ``external`` (the TypeScript
SDK's Q3a predicate); ``tests/test_unit_coverage.py`` holds the clients to it. Both clients wrap
every one of them except the operations named below, each with a comment naming the work that will
wrap it: an operation added to the contract fails the coverage test until a method wraps it or it is
named here.
"""

NOT_YET_WRAPPED: frozenset[str] = frozenset(
    {
        "listMyConnectedApps",
    }
)
