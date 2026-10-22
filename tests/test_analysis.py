import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from src.analysis import summarize_country, prepare_clustering_features
from src.data_prep import build_dataset


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/daily-new-confirmed-covid-19-deaths-per-million-people.csv"


class SourceDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(RAW, parse_dates=["Day"])

    def test_required_columns_and_nonempty_source(self):
        self.assertTrue({"Entity", "Day", "New deaths (per 1M)"} <= set(self.data.columns))
        self.assertGreater(len(self.data), 0)

    def test_country_dates_are_present_and_unique(self):
        self.assertFalse(self.data[["Entity", "Day"]].isna().any().any())
        self.assertFalse(self.data.duplicated(["Entity", "Day"]).any())

    def test_country_series_have_daily_spacing(self):
        for country, group in self.data.groupby("Entity"):
            with self.subTest(country=country):
                gaps = group.sort_values("Day")["Day"].diff().dropna()
                self.assertTrue(gaps.eq(pd.Timedelta(days=1)).all())

    def test_mortality_values_are_finite_numbers(self):
        values = pd.to_numeric(self.data["New deaths (per 1M)"], errors="raise")
        self.assertTrue(np.isfinite(values).all())


class CalculationTests(unittest.TestCase):
    def test_rolling_windows_do_not_mix_countries(self):
        source = pd.DataFrame({"Entity": ["B", "A", "B", "A"],
                               "Day": ["2020-01-02", "2020-01-01", "2020-01-01", "2020-01-02"],
                               "New deaths (per 1M)": [30, 2, 10, 4]})
        with tempfile.TemporaryDirectory() as directory:
            input_path, output_path = Path(directory) / "raw.csv", Path(directory) / "result.csv"
            source.to_csv(input_path, index=False)
            result = build_dataset(input_path, output_path)
        self.assertEqual(result["rolling_7d"].tolist(), [2, 3, 10, 20])
        self.assertEqual(result.groupby("Entity")["deaths_per_million"].sum().to_dict(), {"A": 6, "B": 40})

    def test_cumulative_total_and_recovery_threshold(self):
        data = pd.DataFrame({"Day": pd.date_range("2020-01-01", periods=4),
                             "deaths_per_million": [4, 8, 3, 2], "rolling_7d": [4, 8, 3, 2]})
        result = summarize_country(data)
        self.assertEqual(result["cumulative_deaths_per_million"], 17)
        self.assertEqual(result["peak_date"], "2020-01-02")
        self.assertEqual(result["days_to_recover_from_main_peak"], 2)

    def test_recovery_is_missing_if_threshold_is_never_reached(self):
        data = pd.DataFrame({"Day": pd.date_range("2020-01-01", periods=3),
                             "deaths_per_million": [4, 8, 3], "rolling_7d": [4, 8, 3]})
        self.assertTrue(pd.isna(summarize_country(data)["days_to_recover_from_main_peak"]))




class ClusteringInputTests(unittest.TestCase):
    def test_unobserved_recovery_is_imputed_only_for_clustering(self):
        summary = pd.DataFrame({
            "peak_7d_deaths_per_million": [2.0, 4.0, 6.0],
            "cumulative_deaths_per_million": [10.0, 20.0, 30.0],
            "volatility_std": [1.0, 2.0, 3.0],
            "estimated_wave_count": [1, 2, 3],
            "days_to_recover_from_main_peak": [10.0, np.nan, 20.0],
            "zero_share": [0.1, 0.2, 0.3],
        })
        result = prepare_clustering_features(summary, summary.columns.tolist())
        self.assertEqual(result["recovery_not_observed"].tolist(), [0, 1, 0])
        self.assertEqual(result["days_to_recover_from_main_peak"].tolist(), [10.0, 15.0, 20.0])
        self.assertTrue(pd.isna(summary.loc[1, "days_to_recover_from_main_peak"]))
        self.assertTrue(np.isfinite(result.to_numpy()).all())

    def test_all_missing_recovery_causes_clear_error(self):
        summary = pd.DataFrame({"days_to_recover_from_main_peak": [np.nan, np.nan]})
        with self.assertRaisesRegex(ValueError, "No observed clustering values"):
            prepare_clustering_features(summary, summary.columns.tolist())

if __name__ == "__main__":
    unittest.main()
