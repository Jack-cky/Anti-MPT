import unittest

import pandas as pd

from antimpt.utils.dataset import get_equity, get_risk_free, get_market_index


class TestDataset(unittest.TestCase):
    def test_get_equity(self):
        df = get_equity(2010, 2020, "WSM")

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2729, 33))

    def test_get_risk_free(self):
        df = get_risk_free("2010-01-04", "2020-12-31", 10_000)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (44, 2))

    def test_get_market_index(self):
        df = get_market_index("2010-01-04", 10_000)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3876, 2))


if __name__ == "__main__":
    unittest.main()
